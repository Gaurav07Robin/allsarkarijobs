from backend.database import get_connection

def update_direct_links():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE recruitments SET apply_url = 'https://ssc.gov.in/portal/login' WHERE slug = 'ssc-cgl-2026-online-form'")
    cur.execute("UPDATE recruitments SET apply_url = 'https://www.rrbapply.gov.in/#/auth/home' WHERE slug = 'rrb-technician-cen-02-2026'")
    cur.execute("UPDATE recruitments SET apply_url = 'https://ccp123.onlinereg.co.in/' WHERE slug = 'up-police-constable-2026'")
    cur.execute("UPDATE recruitments SET apply_url = 'https://ibpsonline.ibps.in/crppo14jul24/' WHERE slug = 'ibps-po-mt-xiv-2026'")
    cur.execute("UPDATE recruitments SET apply_url = 'https://main.sci.gov.in/recruitment' WHERE slug = 'supreme-court-junior-court-assistant-2026'")
    conn.commit()
    conn.close()
    print("Direct apply URLs updated successfully!")

if __name__ == "__main__":
    update_direct_links()
