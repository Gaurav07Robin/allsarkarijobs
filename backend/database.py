import sqlite3
import json
from datetime import datetime
from backend.config import DB_PATH

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS recruitments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        slug TEXT UNIQUE NOT NULL,
        organization TEXT NOT NULL,
        category TEXT NOT NULL,
        total_posts INTEGER DEFAULT 0,
        qualification TEXT,
        age_limit TEXT,
        fee_details TEXT,
        start_date TEXT,
        last_date TEXT,
        exam_date TEXT,
        apply_url TEXT,
        notification_pdf_url TEXT,
        official_website_url TEXT,
        description TEXT,
        status TEXT DEFAULT 'PUBLISHED',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS updates (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        recruitment_id INTEGER,
        category TEXT NOT NULL,
        title TEXT NOT NULL,
        tag TEXT,
        action_url TEXT NOT NULL,
        is_featured BOOLEAN DEFAULT 0,
        featured_badge TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (recruitment_id) REFERENCES recruitments(id) ON DELETE SET NULL
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS crawler_staging (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source_portal TEXT NOT NULL,
        source_url TEXT NOT NULL,
        title TEXT NOT NULL,
        category TEXT DEFAULT 'LATEST_JOB',
        detected_date TEXT,
        pdf_url TEXT,
        action_url TEXT,
        extracted_data TEXT,
        status TEXT DEFAULT 'PENDING',
        confidence_score REAL DEFAULT 0.85,
        qualification_level TEXT DEFAULT 'All',
        sector TEXT DEFAULT 'Central',
        state TEXT DEFAULT 'All India',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS crawler_watchdogs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        url TEXT NOT NULL,
        category TEXT DEFAULT 'LATEST_JOB',
        last_hash TEXT,
        last_checked TEXT,
        items_found INTEGER DEFAULT 0,
        status TEXT DEFAULT 'ACTIVE'
    );
    """)

    # Auto-migrate any missing columns for smooth backwards compatibility
    def ensure_columns(table, columns):
        cur.execute(f"PRAGMA table_info({table})")
        existing = [r[1] for r in cur.fetchall()]
        for col_name, col_type in columns:
            if col_name not in existing:
                cur.execute(f"ALTER TABLE {table} ADD COLUMN {col_name} {col_type}")

    ensure_columns("updates", [
        ("source_portal", "TEXT"),
        ("source_url", "TEXT"),
        ("pdf_url", "TEXT"),
        ("qualification_level", "TEXT DEFAULT 'All'"),
        ("sector", "TEXT DEFAULT 'Central'"),
        ("state", "TEXT DEFAULT 'All India'")
    ])

    ensure_columns("crawler_staging", [
        ("qualification_level", "TEXT DEFAULT 'All'"),
        ("sector", "TEXT DEFAULT 'Central'"),
        ("state", "TEXT DEFAULT 'All India'")
    ])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database schema initialized and migrated successfully at:", DB_PATH)
