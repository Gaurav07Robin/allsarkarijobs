import sqlite3
from backend.config import DB_PATH

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Check columns in updates
    cur.execute("PRAGMA table_info(updates)")
    columns = [row[1] for row in cur.fetchall()]

    if "source_portal" not in columns:
        cur.execute("ALTER TABLE updates ADD COLUMN source_portal TEXT")
    if "source_url" not in columns:
        cur.execute("ALTER TABLE updates ADD COLUMN source_url TEXT")
    if "pdf_url" not in columns:
        cur.execute("ALTER TABLE updates ADD COLUMN pdf_url TEXT")

    # Update row 46 specifically (and any other rows matched to staging)
    cur.execute("""
        UPDATE updates
        SET source_portal = 'Institute of Banking Personnel Selection (IBPS)',
            source_url = 'https://ibps.in',
            pdf_url = 'https://ibps.in'
        WHERE id = 46
    """)

    # Sync any updates that were published from staging
    cur.execute("""
        UPDATE updates
        SET source_portal = (SELECT s.source_portal FROM crawler_staging s WHERE s.title = updates.title LIMIT 1),
            source_url = (SELECT s.source_url FROM crawler_staging s WHERE s.title = updates.title LIMIT 1),
            pdf_url = (SELECT s.pdf_url FROM crawler_staging s WHERE s.title = updates.title LIMIT 1)
        WHERE source_portal IS NULL
    """)

    conn.commit()
    conn.close()
    print("Database migration completed: updates table enriched with source_portal, source_url, pdf_url.")

if __name__ == "__main__":
    migrate()
