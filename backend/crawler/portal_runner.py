import time
import json
from datetime import datetime
from typing import List, Dict, Any
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from backend.database import get_connection
from backend.crawler.base import BaseCrawler
from backend.crawler.pdf_parser import PDFNoticeParser
from backend.crawler.registry import TOP_25_PORTALS
from backend.crawler.national_directory import NATIONAL_EXAM_DIRECTORY

CATEGORY_MAPPING = {
    "RESULT": ["result", "merit", "cutoff", "score", "marks", "selected"],
    "ADMIT_CARD": ["admit card", "hall ticket", "call letter", "city slip", "exam date", "schedule"],
    "ANSWER_KEY": ["answer key", "response sheet", "objection"],
    "SYLLABUS": ["syllabus", "exam pattern", "scheme"],
    "ADMISSION": ["admission", "entrance", "counselling", "gate", "jam", "phd", "seat allotment"]
}

def classify_category(title: str, default_cat: str = "LATEST_JOB") -> str:
    t_lower = title.lower()
    for cat, kws in CATEGORY_MAPPING.items():
        if any(kw in t_lower for kw in kws):
            return cat
    return default_cat

class Top25CrawlerRunner:
    @staticmethod
    def sync_watchdogs_to_db():
        """Ensure all registered national and state portals exist in crawler_watchdogs."""
        conn = get_connection()
        cur = conn.cursor()

        # Combine Top 25 and full National Exam Directory
        all_portals = {p["name"]: p for p in TOP_25_PORTALS}
        for p in NATIONAL_EXAM_DIRECTORY:
            if p["name"] not in all_portals:
                all_portals[p["name"]] = p

        for name, portal in all_portals.items():
            cur.execute("SELECT id FROM crawler_watchdogs WHERE name = ?", (name,))
            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO crawler_watchdogs (name, url, category, status)
                    VALUES (?, ?, ?, 'ACTIVE')
                """, (name, portal["url"], portal.get("default_category", "LATEST_JOB")))

        conn.commit()
        conn.close()

    @classmethod
    def scan_single_portal(cls, portal_cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Politely scrapes a single portal respecting timeouts and rate limits."""
        crawler = BaseCrawler(name=portal_cfg["name"], base_url=portal_cfg["url"])
        discovered = []

        try:
            # Respect rate limit with polite pause before each request
            delay = portal_cfg.get("rate_limit_delay", 1.2)
            time.sleep(delay)

            html = crawler.fetch_page(retries=2, delay=0.8)
            if html:
                soup = BeautifulSoup(html, "html.parser")
                for a in soup.find_all("a", href=True):
                    text = a.get_text(strip=True)
                    href = a["href"].strip()

                    if not text or len(text) < 10:
                        continue

                    # Filter relevant keywords
                    keywords = portal_cfg.get("keywords", [])
                    matches_kw = any(k in text.lower() for k in keywords)
                    is_recruitment_term = any(
                        term in text.lower()
                        for term_list in CATEGORY_MAPPING.values()
                        for term in term_list
                    ) or "recruitment" in text.lower() or "online" in text.lower()

                    if not matches_kw and not is_recruitment_term and not href.lower().endswith(".pdf"):
                        continue

                    base = portal_cfg.get("base_url", portal_cfg["url"])
                    full_url = urljoin(base, href)
                    is_pdf = full_url.lower().endswith(".pdf") or "pdf" in full_url.lower()
                    cat = classify_category(text, portal_cfg.get("default_category", "LATEST_JOB"))

                    extracted_data = {}
                    if is_pdf:
                        extracted_data = PDFNoticeParser.parse_notice_text(text)

                    discovered.append({
                        "source_portal": portal_cfg["name"],
                        "source_url": base,
                        "title": text[:240],
                        "category": cat,
                        "action_url": full_url,
                        "pdf_url": full_url if is_pdf else None,
                        "extracted_data": extracted_data,
                        "confidence_score": 0.90 if matches_kw else 0.75,
                        "qualification_level": portal_cfg.get("qualification", "All"),
                        "sector": portal_cfg.get("sector", "Central"),
                        "state": portal_cfg.get("state", "All India")
                    })

        except Exception as e:
            print(f"[Top25Runner] Notice scan warning on {portal_cfg['name']}: {e}")

        return discovered

    @classmethod
    def run_portal_list(cls, portal_list: List[Dict[str, Any]], label: str = "National") -> Dict[str, Any]:
        """Generic runner that scrapes a list of portals with polite delays and staging deduplication."""
        cls.sync_watchdogs_to_db()

        conn = get_connection()
        cur = conn.cursor()

        stats = {
            "label": label,
            "total_configured_portals": len(portal_list),
            "scanned_portals": 0,
            "new_items_queued": 0,
            "errors": 0,
            "timestamp": datetime.now().isoformat()
        }

        print(f"[{label}Runner] Starting sequential scan of {len(portal_list)} portals with polite rate limits...")

        for idx, portal in enumerate(portal_list, 1):
            try:
                items = cls.scan_single_portal(portal)
                stats["scanned_portals"] += 1

                new_for_portal = 0
                for item in items[:8]:  # Process top 8 most recent updates per portal
                    # Deduplication check
                    cur.execute(
                        "SELECT id FROM crawler_staging WHERE title = ? OR action_url = ?",
                        (item["title"], item["action_url"])
                    )
                    if cur.fetchone():
                        continue

                    cur.execute(
                        "SELECT id FROM updates WHERE title = ? OR action_url = ?",
                        (item["title"], item["action_url"])
                    )
                    if cur.fetchone():
                        continue

                    cur.execute("""
                        INSERT INTO crawler_staging (
                            source_portal, source_url, title, category,
                            pdf_url, action_url, extracted_data, confidence_score, status,
                            qualification_level, sector, state
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING', ?, ?, ?)
                    """, (
                        item["source_portal"],
                        item["source_url"],
                        item["title"],
                        item["category"],
                        item["pdf_url"],
                        item["action_url"],
                        json.dumps(item["extracted_data"]),
                        item["confidence_score"],
                        item.get("qualification_level", "All"),
                        item.get("sector", "Central"),
                        item.get("state", "All India")
                    ))
                    new_for_portal += 1

                stats["new_items_queued"] += new_for_portal

                # Update audit log in watchdogs table
                cur.execute("""
                    UPDATE crawler_watchdogs
                    SET last_checked = datetime('now'),
                        items_found = items_found + ?
                    WHERE name = ?
                """, (new_for_portal, portal["name"]))
                conn.commit()

            except Exception as e:
                print(f"[{label}Runner] Error on {portal['name']}: {e}")
                stats["errors"] += 1

        conn.close()
        print(f"[{label}Runner] Scan finished. Portals scanned: {stats['scanned_portals']}, New items: {stats['new_items_queued']}")
        return stats

    @classmethod
    def run_all_top_25(cls) -> Dict[str, Any]:
        """Runs through all Top 25 portals sequentially with polite spacing."""
        return cls.run_portal_list(TOP_25_PORTALS, label="Top25")

    @classmethod
    def run_all_national(cls, max_portals: int = None) -> Dict[str, Any]:
        """Runs through all national & state exam boards across India."""
        portals = NATIONAL_EXAM_DIRECTORY[:max_portals] if max_portals else NATIONAL_EXAM_DIRECTORY
        return cls.run_portal_list(portals, label="AllIndiaExams")
