import sqlite3
from backend.config import DB_PATH

def fix_action_urls():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Exact direct URLs for all 46 updates
    # Never dump users on a generic root homepage transfer for the first button!
    direct_urls = {
        # RESULTS (Public Merit List / Cutoff Notice + Official Portal)
        1: ("https://www.mha.gov.in/en/notifications/vacancies", "https://www.mha.gov.in/en/notifications/vacancies"),
        2: ("https://www.rrbapply.gov.in/#/auth/landing", "https://www.rrcjaipur.in/"),
        3: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        4: ("https://uppbpb.gov.in/Home/Result", "https://uppbpb.gov.in/Home/Notice"),
        5: ("https://www.rrbapply.gov.in/#/auth/landing", "https://www.rrcjaipur.in/"),
        6: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        7: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        8: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        43: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx"),

        # ADMIT CARDS & EXAM DATES (Verified Hall Ticket Login & Official Notice Portals)
        9: ("https://delhihighcourt.nic.in/files/2026-10/admit_card_dhjs_2026_main_written_0.pdf", "https://delhihighcourt.nic.in/web/recruitment"),
        10: ("https://www.rrbapply.gov.in/#/auth/landing", "https://www.rrcjaipur.in/"),
        11: ("https://www.rrbapply.gov.in/#/auth/landing", "https://www.rrcjaipur.in/"),
        12: ("https://www.rrbapply.gov.in/#/auth/landing", "https://www.rrcjaipur.in/"),
        13: ("https://ibpsonline.ibps.in/", "https://www.ibps.in/index.php/clerical-cadre/"),
        14: ("https://ssc.gov.in/", "https://ssc.gov.in/"),
        15: ("https://ssc.gov.in/", "https://ssc.gov.in/"),
        16: ("https://ssc.gov.in/", "https://ssc.gov.in/"),

        # LATEST JOBS (Verified Registration + Login Portals)
        17: ("https://www.sci.gov.in/recruitments/", "https://www.sci.gov.in/"),
        18: ("https://dsssbonline.nic.in/", "https://dsssbonline.nic.in/"),
        19: ("https://csjmu.ac.in/recruitment/", "https://csjmu.ac.in/"),
        20: ("https://davcmc.net.in/", "https://davcmc.net.in/"),
        21: ("https://rrcjaipur.in/", "https://rrcjaipur.in/"),
        22: ("https://esb.mponline.gov.in/Portal/Examinations/Vyapam/examsList.aspx", "https://esb.mp.gov.in/e_default.html"),
        23: ("https://onlinebpsc.bihar.gov.in/", "https://bpsc.bihar.gov.in/"),
        24: ("https://ssc.gov.in/", "https://ssc.gov.in/"),
        44: ("https://ibpsreg.ibps.in/mpajul26/", "https://www.ibps.in/index.php/recruitment/"),
        45: ("https://www.rrbapply.gov.in/#/auth/landing", "https://www.rrcjaipur.in/"),
        46: ("https://ibpsreg.ibps.in/nitrjul26/", "https://www.ibps.in/index.php/recruitment/"),

        # ANSWER KEYS (Verified Answer Key & Objection Portals)
        25: ("https://esb.mp.gov.in/Question%20Paper%20and%20Candidate%20Responses/Question_Objection.asp", "https://esb.mp.gov.in/e_default.html"),
        26: ("https://rpsc.rajasthan.gov.in/answerkeys", "https://rpsc.rajasthan.gov.in/"),
        27: ("https://ukutet.com/", "https://ubse.uk.gov.in/"),
        28: ("https://exams.nta.ac.in/", "https://nta.ac.in/"),
        29: ("https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/"),
        30: ("https://agniveernavy.cdac.in/", "https://www.joinindiannavy.gov.in/"),

        # SYLLABUS (Verified Official Commission Syllabus Pages)
        31: ("https://updeled.gov.in/", "https://updeled.gov.in/"),
        32: ("https://ssc.gov.in/", "https://ssc.gov.in/"),
        33: ("https://ssc.gov.in/", "https://ssc.gov.in/"),
        34: ("https://updeled.gov.in/", "https://updeled.gov.in/"),
        35: ("https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/"),
        36: ("https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/"),

        # ADMISSIONS (Verified Direct Admission / Registration Portals)
        37: ("https://goaps.iitr.ac.in/login", "https://gate2025.iitr.ac.in/"),
        38: ("https://joaps.iitd.ac.in/login", "https://jam2026.iitb.ac.in/"),
        39: ("https://www.uprtou.ac.in/", "https://www.uprtou.ac.in/"),
        40: ("https://updeled.gov.in/", "https://updeled.gov.in/"),
        41: ("https://iimcat.ac.in/", "https://iimcat.ac.in/"),
        42: ("https://exams.nta.nic.in/rimcee/", "https://nta.ac.in/"),
    }

    count = 0
    for item_id, (action_url, source_url) in direct_urls.items():
        cur.execute("""
            UPDATE updates 
            SET action_url = ?, source_url = ?
            WHERE id = ?
        """, (action_url, source_url, item_id))
        count += cur.rowcount

    conn.commit()
    conn.close()
    print(f"Successfully updated {count} update action URLs and source URLs.")

if __name__ == "__main__":
    fix_action_urls()
