import json
from datetime import datetime
from typing import Optional, List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query, Body, status, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from backend.config import BASE_DIR
from backend.database import get_connection, init_db
from backend.seed_data import seed
from backend.migrate_db import migrate
from backend.migrate_filters import migrate_filters
from backend.publish_crawled import export_portal_data_js
from backend.crawler.engine import CrawlerEngine, BackgroundCrawlerScheduler

# Ensure database is created, migrated, and synced with sarkariresult.com dataset
init_db()
migrate()
migrate_filters()

def _ensure_sarkariresult_seeded():
    conn = get_connection()
    cur = conn.cursor()
    cols = {r[1] for r in cur.execute("PRAGMA table_info(updates)").fetchall()}
    has_sr = False
    if "meta_json" in cols:
        cnt = cur.execute("SELECT COUNT(*) FROM updates WHERE meta_json IS NOT NULL AND meta_json != ''").fetchone()[0]
        has_sr = cnt > 0
    conn.close()
    if not has_sr:
        from backend.scrape_sarkariresult import scrape_all_from_sarkariresult
        scrape_all_from_sarkariresult()
    else:
        export_portal_data_js()

_ensure_sarkariresult_seeded()

# Start background crawler scheduler (runs every 30 mins)
BackgroundCrawlerScheduler.start(interval_minutes=30)

app = FastAPI(
    title="All Sarkari Jobs API",
    description="Backend API and aggregation engine for AllSarkariJobs.online — Latest Government Jobs, Sarkari Results, Admit Cards & Exam Updates",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Models -----------------
class ManualUpdateItem(BaseModel):
    category: str  # LATEST_JOB, RESULT, ADMIT_CARD, ANSWER_KEY, SYLLABUS, ADMISSION
    title: str
    action_url: str
    tag: Optional[str] = "New"
    is_featured: bool = False
    featured_badge: Optional[str] = None

class PublishStagingRequest(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    action_url: Optional[str] = None
    tag: Optional[str] = "New"
    is_featured: bool = False

# ----------------- Public API Endpoints -----------------

@app.get("/api/updates")
def get_all_updates():
    """Return categorized updates for the 6 primary portal columns and top highlight strip."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT *
        FROM updates
        ORDER BY id DESC
    """)
    rows = cur.fetchall()
    conn.close()

    categories = {
        "RESULT": [],
        "ADMIT_CARD": [],
        "LATEST_JOB": [],
        "ANSWER_KEY": [],
        "SYLLABUS": [],
        "ADMISSION": []
    }
    featured = []

    for row in rows:
        item = {
            "id": row["id"],
            "recruitment_id": row["recruitment_id"],
            "category": row["category"],
            "title": row["title"],
            "tag": row["tag"],
            "action_url": row["action_url"],
            "is_featured": bool(row["is_featured"]),
            "featured_badge": row["featured_badge"],
            "created_at": row["created_at"],
            "qualification": row["qualification_level"] if "qualification_level" in row.keys() else "All",
            "sector": row["sector"] if "sector" in row.keys() else "Central",
            "state": row["state"] if "state" in row.keys() else "All India"
        }
        if item["category"] in categories:
            categories[item["category"]].append(item)
        if item["is_featured"]:
            featured.append(item)

    return {
        "status": "success",
        "data": categories,
        "featured": featured
    }

@app.get("/api/jobs")
def get_jobs(q: Optional[str] = None, category: Optional[str] = None, limit: int = 50):
    """List detailed job recruitments."""
    conn = get_connection()
    cur = conn.cursor()

    query = "SELECT * FROM recruitments WHERE status = 'PUBLISHED'"
    params = []

    if q:
        query += " AND (title LIKE ? OR organization LIKE ? OR description LIKE ?)"
        wildcard = f"%{q}%"
        params.extend([wildcard, wildcard, wildcard])

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)

    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    return {
        "status": "success",
        "total": len(rows),
        "jobs": [dict(r) for r in rows]
    }

@app.get("/api/jobs/{slug}")
def get_job_detail(slug: str):
    """Retrieve full details of a specific recruitment by slug."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recruitments WHERE slug = ?", (slug,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise HTTPException(status_code=404, detail="Job posting not found")

    return {
        "status": "success",
        "job": dict(row)
    }

@app.get("/api/detail/{item_id}")
def get_update_detail(item_id: int):
    """Retrieve details of a specific update notice by ID."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM updates WHERE id = ?", (item_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Notice not found")
    update_data = dict(row)
    conn.close()
    if isinstance(update_data.get("meta_json"), str) and update_data.get("meta_json"):
        try:
            update_data["meta"] = json.loads(update_data["meta_json"])
        except Exception:
            update_data["meta"] = {}
    update_data.pop("meta_json", None)
    return {
        "status": "success",
        "update": update_data
    }

@app.get("/api/pdf/{item_id}")
def view_notice_pdf(item_id: int):
    """Directly stream or display the official notice PDF."""
    from backend.pdf_service import get_pdf_for_update
    try:
        pdf_bytes = get_pdf_for_update(item_id)
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f'inline; filename="official_notice_{item_id}.pdf"',
                "Cache-Control": "public, max-age=3600"
            }
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Notice not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate notice PDF: {str(e)}")

@app.get("/api/pdf/job/{slug}")
def view_job_pdf(slug: str):
    """Directly stream or display the official notification PDF for a recruitment."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recruitments WHERE slug = ?", (slug,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")
    
    item = dict(row)
    pdf_url = item.get("notification_pdf_url")
    if pdf_url and pdf_url.startswith("http"):
        try:
            import requests
            headers = {"User-Agent": "Mozilla/5.0"}
            resp = requests.get(pdf_url, headers=headers, timeout=4.0, stream=True)
            if resp.status_code == 200 and (resp.content.startswith(b"%PDF-") or len(resp.content) > 1000):
                return Response(
                    content=resp.content,
                    media_type="application/pdf",
                    headers={"Content-Disposition": f'inline; filename="{slug}.pdf"'}
                )
        except Exception:
            pass
    
    from backend.pdf_service import generate_official_notice_pdf
    notice_dict = {
        "id": item["id"],
        "title": item["title"],
        "category": item.get("category", "LATEST_JOB"),
        "source_portal": item.get("organization", "Central / State Govt"),
        "state": "All India",
        "sector": "Recruitment",
        "qualification_level": item.get("qualification", "Refer to Advertisement"),
        "action_url": item.get("apply_url"),
        "created_at": item.get("created_at")
    }
    pdf_bytes = generate_official_notice_pdf(notice_dict)
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'inline; filename="{slug}.pdf"'}
    )

@app.get("/api/search")
def search_everything(q: str = Query(..., min_length=2)):
    """Global instant search across updates and recruitments."""
    conn = get_connection()
    cur = conn.cursor()
    wildcard = f"%{q}%"

    cur.execute("""
        SELECT id, category, title, tag, action_url, 'update' as type
        FROM updates
        WHERE title LIKE ?
        ORDER BY id DESC LIMIT 15
    """, (wildcard,))
    update_matches = [dict(r) for r in cur.fetchall()]

    cur.execute("""
        SELECT id, 'LATEST_JOB' as category, title, 'Featured' as tag,
               ('/jobs/' || slug) as action_url, 'recruitment' as type
        FROM recruitments
        WHERE title LIKE ? OR organization LIKE ?
        ORDER BY id DESC LIMIT 15
    """, (wildcard, wildcard))
    job_matches = [dict(r) for r in cur.fetchall()]

    conn.close()
    return {
        "status": "success",
        "query": q,
        "results": update_matches + job_matches
    }

# ----------------- Admin CMS & Review Endpoints -----------------

@app.get("/api/admin/stats")
def get_admin_stats():
    """Summary stats for dashboard."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM updates")
    total_updates = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM recruitments")
    total_recruitments = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM crawler_staging WHERE status = 'PENDING'")
    pending_staging = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM crawler_watchdogs WHERE status = 'ACTIVE'")
    active_watchdogs = cur.fetchone()[0]

    conn.close()
    return {
        "total_updates": total_updates,
        "total_recruitments": total_recruitments,
        "pending_staging": pending_staging,
        "active_watchdogs": active_watchdogs,
        "scheduler": BackgroundCrawlerScheduler.get_status()
    }

@app.get("/api/admin/scheduler/status")
def get_scheduler_status():
    return {
        "status": "success",
        "scheduler": BackgroundCrawlerScheduler.get_status()
    }

@app.get("/api/admin/staging")
def get_staging_queue(status_filter: str = "PENDING"):
    """Review queue of scraped notices awaiting editorial approval."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT id, source_portal, source_url, title, category,
               pdf_url, action_url, extracted_data, confidence_score, status, created_at
        FROM crawler_staging
        WHERE status = ?
        ORDER BY id DESC
    """, (status_filter,))
    rows = cur.fetchall()
    conn.close()

    items = []
    for r in rows:
        item = dict(r)
        if item.get("extracted_data"):
            try:
                item["extracted_data"] = json.loads(item["extracted_data"])
            except Exception:
                pass
        items.append(item)

    return {
        "status": "success",
        "items": items
    }

@app.post("/api/admin/publish/{staging_id}")
def publish_staging_item(staging_id: int, payload: Optional[PublishStagingRequest] = None):
    """1-Click Approve and publish a pending notice into the public portal."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM crawler_staging WHERE id = ?", (staging_id,))
    item = cur.fetchone()
    if not item:
        conn.close()
        raise HTTPException(status_code=404, detail="Staging item not found")

    title = payload.title if (payload and payload.title) else item["title"]
    category = payload.category if (payload and payload.category) else item["category"]
    action_url = payload.action_url if (payload and payload.action_url) else item["action_url"]
    tag = payload.tag if (payload and payload.tag) else "New"
    is_featured = payload.is_featured if (payload and payload.is_featured) else False

    qual = item["qualification_level"] if "qualification_level" in item.keys() and item["qualification_level"] else "All"
    sec = item["sector"] if "sector" in item.keys() and item["sector"] else "Central"
    st = item["state"] if "state" in item.keys() and item["state"] else "All India"

    # Insert into live updates table
    cur.execute("""
        INSERT INTO updates (
            category, title, tag, action_url, is_featured,
            source_portal, source_url, pdf_url, qualification_level, sector, state
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        category,
        title,
        tag,
        action_url,
        1 if is_featured else 0,
        item["source_portal"],
        item["source_url"],
        item["pdf_url"],
        qual,
        sec,
        st
    ))

    # Mark staging item approved
    cur.execute("UPDATE crawler_staging SET status = 'APPROVED' WHERE id = ?", (staging_id,))

    conn.commit()
    conn.close()
    export_portal_data_js()

    return {"status": "success", "message": f"Successfully published notice: '{title}'"}

@app.post("/api/admin/reject/{staging_id}")
def reject_staging_item(staging_id: int):
    """Reject an irrelevant or duplicate scraped item."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE crawler_staging SET status = 'REJECTED' WHERE id = ?", (staging_id,))
    conn.commit()
    conn.close()
    return {"status": "success", "message": "Item rejected"}

@app.post("/api/admin/manual-update")
def create_manual_update(item: ManualUpdateItem):
    """Manually add a new update directly without scraping."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO updates (category, title, tag, action_url, is_featured, featured_badge)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (item.category, item.title, item.tag, item.action_url, 1 if item.is_featured else 0, item.featured_badge))
    conn.commit()
    conn.close()
    export_portal_data_js()
    return {"status": "success", "message": "Update posted live"}

@app.post("/api/admin/crawl/run")
def run_crawler():
    """Trigger background scan across monitored portals."""
    stats = CrawlerEngine.run_all_watchdogs()
    return {"status": "success", "stats": stats}

@app.post("/api/admin/crawl/run-all-india")
def run_all_india_crawler(limit: Optional[int] = None):
    """Trigger scan across all 89+ national and state exam boards in India."""
    from backend.crawler.portal_runner import Top25CrawlerRunner
    stats = Top25CrawlerRunner.run_all_national(max_portals=limit)
    return {"status": "success", "stats": stats}

@app.post("/api/admin/crawl/simulate")
def simulate_crawler_findings():
    """Inject realistic test notices into staging queue to demonstrate 1-click review."""
    injected_count = CrawlerEngine.inject_sample_live_notices()
    return {
        "status": "success",
        "injected_count": injected_count,
        "message": f"{injected_count} new government notices queued in review dashboard."
    }

@app.post("/api/admin/backup/run")
def trigger_backup():
    """Trigger an on-demand atomic database snapshot and cloud sync."""
    from backend.backup import DatabaseBackupService
    snapshot = DatabaseBackupService.run_backup()
    return {
        "status": "success",
        "file_name": snapshot.name,
        "size_kb": round(snapshot.stat().st_size / 1024, 1),
        "message": f"Backup snapshot created successfully: {snapshot.name}"
    }

@app.get("/api/admin/backups")
def list_backups():
    """List available local compressed database snapshots."""
    from backend.backup import BACKUP_DIR
    backups = []
    for f in sorted(BACKUP_DIR.glob("allsarkarijobs_*.db.gz"), key=os.path.getmtime, reverse=True):
        backups.append({
            "name": f.name,
            "size_kb": round(f.stat().st_size / 1024, 1),
            "created_at": datetime.fromtimestamp(f.stat().st_mtime).isoformat()
        })
    return {"status": "success", "backups": backups}

# ----------------- Frontend & Static Routes -----------------

NO_CACHE_HEADERS = {"Cache-Control": "no-store, no-cache, must-revalidate, max-age=0"}

@app.get("/")
def serve_index():
    index_file = BASE_DIR / "index.html"
    return FileResponse(index_file, headers=NO_CACHE_HEADERS)

@app.get("/admin")
def serve_admin():
    admin_file = BASE_DIR / "admin.html"
    return FileResponse(admin_file, headers=NO_CACHE_HEADERS)

@app.get("/jobs/{slug}")
def serve_job_page(slug: str):
    landing_index = BASE_DIR / "jobs" / slug / "index.html"
    if landing_index.exists():
        return FileResponse(landing_index, headers=NO_CACHE_HEADERS)
    job_file = BASE_DIR / "job.html"
    return FileResponse(job_file, headers=NO_CACHE_HEADERS)

@app.get("/job.html")
def serve_job_html():
    job_file = BASE_DIR / "job.html"
    return FileResponse(job_file, headers=NO_CACHE_HEADERS)

@app.get("/detail")
def serve_detail_page():
    detail_file = BASE_DIR / "detail.html"
    return FileResponse(detail_file, headers=NO_CACHE_HEADERS)

@app.get("/detail.html")
def serve_detail_html():
    detail_file = BASE_DIR / "detail.html"
    return FileResponse(detail_file, headers=NO_CACHE_HEADERS)

@app.get("/detail/{item_id}")
def serve_detail_by_id(item_id: int):
    detail_file = BASE_DIR / "detail.html"
    return FileResponse(detail_file, headers=NO_CACHE_HEADERS)

@app.get("/portal_data.js")
def serve_portal_data_js():
    js_file = BASE_DIR / "portal_data.js"
    return FileResponse(js_file, media_type="application/javascript", headers=NO_CACHE_HEADERS)

@app.get("/category.html")
@app.get("/results")
@app.get("/latest-jobs")
@app.get("/jobs")
@app.get("/admit-cards")
@app.get("/admit-card")
@app.get("/answer-keys")
@app.get("/syllabus")
@app.get("/admission")
@app.get("/categories")
def serve_category_page():
    category_file = BASE_DIR / "category.html"
    return FileResponse(category_file, headers=NO_CACHE_HEADERS)

@app.get("/sitemap.xml")
def serve_sitemap():
    sitemap_file = BASE_DIR / "sitemap.xml"
    return FileResponse(sitemap_file, media_type="application/xml", headers=NO_CACHE_HEADERS)

@app.get("/robots.txt")
def serve_robots():
    robots_file = BASE_DIR / "robots.txt"
    return FileResponse(robots_file, media_type="text/plain", headers=NO_CACHE_HEADERS)

# Serve local PDFs
PDFS_DIR = BASE_DIR / "pdfs"
PDFS_DIR.mkdir(exist_ok=True)
app.mount("/pdfs", StaticFiles(directory=PDFS_DIR), name="pdfs")





