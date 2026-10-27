"""
Generates the complete, production-ready sitemap.xml for AllSarkariJobs
containing:
1. Homepage (/)
2. The 6 dedicated category pillar pages (/latest-jobs, /results, /admit-cards, /answer-keys, /syllabus, /admission)
3. All active individual notice pages (/detail?id=...)
4. Dedicated job postings (/jobs/:slug)
"""
import re
import sqlite3
import xml.etree.ElementTree as ET
from datetime import datetime
from backend.config import DB_PATH, BASE_DIR

PRIMARY_DOMAIN = "https://www.allsarkarijobs.online"

CATEGORIES = [
    ("/latest-jobs", "daily", "0.9"),
    ("/results", "daily", "0.9"),
    ("/admit-cards", "daily", "0.9"),
    ("/answer-keys", "daily", "0.8"),
    ("/syllabus", "weekly", "0.8"),
    ("/admission", "daily", "0.9"),
    ("/counselling", "daily", "0.9"),
    ("/jee-main-marks-vs-percentile", "daily", "0.9"),
    ("/counselling/neet-marks-vs-rank", "daily", "0.9"),
    ("/counselling/college-predictor", "daily", "0.9"),
    ("/josaa-college-predictor", "daily", "0.9"),
]


def generate_sitemap():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    c.execute("SELECT id, title, created_at FROM updates ORDER BY id DESC")
    updates = [dict(r) for r in c.fetchall()]

    c.execute("SELECT slug, updated_at, created_at FROM recruitments WHERE status = 'PUBLISHED' ORDER BY id DESC")
    recruitments = [dict(r) for r in c.fetchall()]
    conn.close()

    today_str = datetime.now().strftime("%Y-%m-%d")

    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    # 1. Homepage
    url_el = ET.SubElement(urlset, "url")
    ET.SubElement(url_el, "loc").text = f"{PRIMARY_DOMAIN}/"
    ET.SubElement(url_el, "lastmod").text = today_str
    ET.SubElement(url_el, "changefreq").text = "daily"
    ET.SubElement(url_el, "priority").text = "1.0"

    # 2. Pillar Category Pages
    for path, freq, prio in CATEGORIES:
        url_el = ET.SubElement(urlset, "url")
        ET.SubElement(url_el, "loc").text = f"{PRIMARY_DOMAIN}{path}"
        ET.SubElement(url_el, "lastmod").text = today_str
        ET.SubElement(url_el, "changefreq").text = freq
        ET.SubElement(url_el, "priority").text = prio

    # 2b. Programmatic SEO Landing Pages (/jobs/:slug)
    try:
        from backend.generate_programmatic_seo import LANDING_PAGES
        for p in LANDING_PAGES:
            url_el = ET.SubElement(urlset, "url")
            ET.SubElement(url_el, "loc").text = f"{PRIMARY_DOMAIN}/jobs/{p['slug']}"
            ET.SubElement(url_el, "lastmod").text = today_str
            ET.SubElement(url_el, "changefreq").text = "daily"
            ET.SubElement(url_el, "priority").text = "0.9"
    except Exception as e:
        print(f"Warning adding programmatic pages to sitemap: {e}")

    # 3. Individual Job Postings (/jobs/:slug)
    for r in recruitments:
        slug = r.get("slug")
        if not slug:
            continue
        dt = (r.get("updated_at") or r.get("created_at") or today_str)[:10]
        url_el = ET.SubElement(urlset, "url")
        ET.SubElement(url_el, "loc").text = f"{PRIMARY_DOMAIN}/jobs/{slug}"
        ET.SubElement(url_el, "lastmod").text = dt
        ET.SubElement(url_el, "changefreq").text = "weekly"
        ET.SubElement(url_el, "priority").text = "0.8"

    def make_slug(title: str) -> str:
        s = re.sub(r'[^a-zA-Z0-9]+', '-', (title or '').lower()).strip('-')
        return s[:70].rstrip('-')

    # 4. Individual Notice Detail Pages (/detail/:id-:slug)
    for u in updates:
        item_id = u["id"]
        slug = make_slug(u.get("title") or "")
        dt = today_str
        url_el = ET.SubElement(urlset, "url")
        loc_url = f"{PRIMARY_DOMAIN}/detail/{item_id}-{slug}" if slug else f"{PRIMARY_DOMAIN}/detail?id={item_id}"
        ET.SubElement(url_el, "loc").text = loc_url
        ET.SubElement(url_el, "lastmod").text = dt
        ET.SubElement(url_el, "changefreq").text = "weekly"
        ET.SubElement(url_el, "priority").text = "0.7"

    sitemap_path = BASE_DIR / "sitemap.xml"
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space="  ", level=0)
    tree.write(sitemap_path, encoding="utf-8", xml_declaration=True)

    # Safely ensure sitemap directive in robots.txt without wiping rules
    robots_path = BASE_DIR / "robots.txt"
    if robots_path.exists():
        content = robots_path.read_text(encoding="utf-8")
        sitemap_line = f"Sitemap: {PRIMARY_DOMAIN}/sitemap.xml"
        if sitemap_line not in content:
            content = re.sub(r"Sitemap:\s*https?://[^\s]+", sitemap_line, content)
            if sitemap_line not in content:
                content += f"\n{sitemap_line}\n"
            robots_path.write_text(content, encoding="utf-8")
    else:
        with open(robots_path, "w", encoding="utf-8") as f:
            f.write("User-agent: *\nAllow: /\n\n")
            f.write(f"Sitemap: {PRIMARY_DOMAIN}/sitemap.xml\n")

    total_urls = len(urlset)
    print(f"Generated {sitemap_path} with {total_urls} URLs and updated {robots_path}.")
    return total_urls


if __name__ == "__main__":
    generate_sitemap()
