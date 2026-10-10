import sqlite3
from backend.config import DB_PATH

def migrate_filters():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(updates)")
    columns = [row[1] for row in cur.fetchall()]

    if "qualification_level" not in columns:
        cur.execute("ALTER TABLE updates ADD COLUMN qualification_level TEXT DEFAULT 'All'")
    if "sector" not in columns:
        cur.execute("ALTER TABLE updates ADD COLUMN sector TEXT DEFAULT 'Central'")
    if "state" not in columns:
        cur.execute("ALTER TABLE updates ADD COLUMN state TEXT DEFAULT 'All India'")

    # Tag existing records intelligently
    cur.execute("""
        UPDATE updates
        SET sector = 'Railway', state = 'All India', qualification_level = '10th/12th/Graduate'
        WHERE title LIKE '%Railway%' OR title LIKE '%RRB%'
    """)

    cur.execute("""
        UPDATE updates
        SET sector = 'Central', state = 'All India', qualification_level = 'Graduate'
        WHERE title LIKE '%SSC CGL%' OR title LIKE '%UPSC%'
    """)

    cur.execute("""
        UPDATE updates
        SET sector = 'Central', state = 'All India', qualification_level = '12th'
        WHERE title LIKE '%SSC 10+2%' OR title LIKE '%CHSL%' OR title LIKE '%MTS%'
    """)

    cur.execute("""
        UPDATE updates
        SET sector = 'Police', state = 'Uttar Pradesh', qualification_level = '12th'
        WHERE title LIKE '%UP Police%'
    """)

    cur.execute("""
        UPDATE updates
        SET sector = 'State', state = 'Uttar Pradesh', qualification_level = 'Graduate'
        WHERE title LIKE '%UPSSSC%' OR title LIKE '%UPPSC%' OR title LIKE '%Super TET%'
    """)

    cur.execute("""
        UPDATE updates
        SET sector = 'State', state = 'Bihar', qualification_level = 'Graduate'
        WHERE title LIKE '%Bihar%' OR title LIKE '%BPSC%' OR title LIKE '%BSSC%'
    """)

    cur.execute("""
        UPDATE updates
        SET sector = 'Bank', state = 'All India', qualification_level = 'Graduate'
        WHERE title LIKE '%IBPS%' OR title LIKE '%Bank%' OR title LIKE '%SBI%'
    """)

    cur.execute("""
        UPDATE updates
        SET sector = 'State', state = 'Madhya Pradesh', qualification_level = '12th/Graduate'
        WHERE title LIKE '%MPESB%' OR title LIKE '%MPPSC%'
    """)

    cur.execute("""
        UPDATE updates
        SET sector = 'Defence', state = 'All India', qualification_level = '10th/12th'
        WHERE title LIKE '%Airforce%' OR title LIKE '%Army%' OR title LIKE '%Navy%' OR title LIKE '%Agniveer%'
    """)

    conn.commit()
    conn.close()
    print("Filter metadata migrated into updates successfully!")

if __name__ == "__main__":
    migrate_filters()
