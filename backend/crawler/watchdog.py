import hashlib
import json
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from typing import List, Dict, Any
from backend.crawler.base import BaseCrawler
from backend.crawler.pdf_parser import PDFNoticeParser

CATEGORY_KEYWORDS = {
    "RESULT": ["result", "merit list", "selected candidates", "marks", "cutoff", "score card"],
    "ADMIT_CARD": ["admit card", "hall ticket", "call letter", "exam city", "examination date", "intimation slip"],
    "ANSWER_KEY": ["answer key", "objection", "response sheet", "tentative key"],
    "SYLLABUS": ["syllabus", "scheme of exam", "curriculum"],
    "ADMISSION": ["admission", "entrance", "counselling", "allotment", "phd", "gate", "jee", "neet"],
    "LATEST_JOB": ["recruitment", "notification", "online form", "apply", "vacanc", "advertisement", "engagement"]
}

def detect_category(title: str) -> str:
    title_lower = title.lower()
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in title_lower for kw in keywords):
            return cat
    return "LATEST_JOB"

class NoticeWatchdog(BaseCrawler):
    def __init__(self, name: str, url: str):
        super().__init__(name, url)

    def scan_for_updates(self) -> List[Dict[str, Any]]:
        html = self.fetch_page()
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        discovered_items = []

        # Find all anchor tags with meaningful text or PDF targets
        for a in soup.find_all("a", href=True):
            text = a.get_text(strip=True)
            href = a["href"].strip()

            if not text or len(text) < 10:
                continue

            # Must contain relevant recruitment terminology
            is_relevant = any(
                kw in text.lower()
                for cat_kws in CATEGORY_KEYWORDS.values()
                for kw in cat_kws
            )

            if not is_relevant and not href.lower().endswith(".pdf"):
                continue

            full_url = urljoin(self.base_url, href)
            category = detect_category(text)
            is_pdf = full_url.lower().endswith(".pdf") or "pdf" in full_url.lower()

            item = {
                "source_portal": self.name,
                "source_url": self.base_url,
                "title": text,
                "category": category,
                "action_url": full_url,
                "pdf_url": full_url if is_pdf else None,
                "extracted_data": {
                    "is_pdf": is_pdf,
                    "length": len(text)
                },
                "confidence_score": 0.85 if is_relevant else 0.65
            }

            discovered_items.append(item)

        return discovered_items
