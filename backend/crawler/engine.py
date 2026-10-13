import json
import threading
import time
from datetime import datetime
from typing import List, Dict, Any

from backend.database import get_connection
from backend.crawler.watchdog import NoticeWatchdog
from backend.crawler.scrapers.ssc import SSCScraper
from backend.crawler.scrapers.upsc import UPSCScraper
from backend.crawler.scrapers.rrb import RRBScraper

class CrawlerEngine:
    @staticmethod
    def run_all_watchdogs() -> Dict[str, Any]:
        """Runs targeted production scrapers across all Top 25 national and state exam boards."""
        from backend.crawler.portal_runner import Top25CrawlerRunner
        return Top25CrawlerRunner.run_all_top_25()

    @staticmethod
    def inject_sample_live_notices() -> int:
        """Inject realistic newly discovered notices to demonstrate review queue."""
        conn = get_connection()
        cur = conn.cursor()

        sample_discoveries = [
            (
                "Staff Selection Commission (SSC)",
                "https://ssc.gov.in",
                "SSC CGL 2026 Tier-I Admit Card & Application Status Out",
                "ADMIT_CARD",
                "https://ssc.gov.in/api/pdf/ssc_cgl_admit_2026.pdf",
                "https://ssc.gov.in/portal/login",
                json.dumps({
                    "exam_date": "14-26 September 2026",
                    "status": "Region-wise application status active"
                }),
                0.96
            ),
            (
                "Railway Recruitment Board (RRB)",
                "https://rrbapply.gov.in",
                "Railway RRB NTPC Graduate Level CEN 05/2026 Online Form (11,558 Posts)",
                "LATEST_JOB",
                "https://rrbapply.gov.in/notices/CEN_05_2026.pdf",
                "https://rrbapply.gov.in/#/auth/home",
                json.dumps({
                    "vacancies": "11558",
                    "education": "Graduation Degree",
                    "age_limit": "18 - 36 Years",
                    "fee": "₹500",
                    "last_date": "2026-10-20"
                }),
                0.95
            ),
            (
                "Union Public Service Commission (UPSC)",
                "https://upsc.gov.in",
                "UPSC NDA & NA Exam (II) 2026 Final Selection List Declared",
                "RESULT",
                "https://upsc.gov.in/sites/default/files/NDA-II-2026-Final.pdf",
                "https://upsc.gov.in",
                json.dumps({
                    "total_selected": "400 Candidates",
                    "course_commencing": "January 2027"
                }),
                0.94
            )
        ]

        count = 0
        for item in sample_discoveries:
            cur.execute("SELECT id FROM crawler_staging WHERE title = ?", (item[2],))
            if not cur.fetchone():
                cur.execute("""
                    INSERT INTO crawler_staging (
                        source_portal, source_url, title, category,
                        pdf_url, action_url, extracted_data, confidence_score, status
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
                """, item)
                count += 1

        conn.commit()
        conn.close()
        return count


class BackgroundCrawlerScheduler:
    """Runs automated crawls in background thread on recurring intervals."""
    _thread: threading.Thread = None
    _running: bool = False
    _interval_minutes: int = 30
    _last_run: str = None
    _last_stats: dict = {}

    @classmethod
    def start(cls, interval_minutes: int = 30):
        if cls._running:
            return
        cls._interval_minutes = interval_minutes
        cls._running = True
        cls._thread = threading.Thread(target=cls._loop, daemon=True)
        cls._thread.start()
        print(f"[Scheduler] Automated background crawler started. Interval: every {interval_minutes} minutes.")

    @classmethod
    def stop(cls):
        cls._running = False

    @classmethod
    def _loop(cls):
        # Run an initial check after 10 seconds of startup
        time.sleep(10)
        while cls._running:
            try:
                print(f"[Scheduler] Running automated check at {datetime.now().strftime('%H:%M:%S')}...")
                stats = CrawlerEngine.run_all_watchdogs()
                cls._last_run = datetime.now().isoformat()
                cls._last_stats = stats
                print(f"[Scheduler] Automated check finished: {stats['new_items_found']} new notices queued.")
            except Exception as e:
                print(f"[Scheduler] Background crawler error: {e}")

            # Sleep in small slices to allow clean shutdown
            sleep_seconds = cls._interval_minutes * 60
            for _ in range(sleep_seconds):
                if not cls._running:
                    break
                time.sleep(1)

    @classmethod
    def get_status(cls) -> Dict[str, Any]:
        return {
            "is_running": cls._running,
            "interval_minutes": cls._interval_minutes,
            "last_run": cls._last_run,
            "last_stats": cls._last_stats
        }
