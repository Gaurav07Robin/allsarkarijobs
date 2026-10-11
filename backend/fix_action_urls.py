import sqlite3
from backend.config import DB_PATH

def fix_action_urls():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Exact direct URLs for all 46 updates
    # Never dump users on a generic root homepage transfer for the first button!
    direct_urls = {
        # RESULTS (Direct Result Login / Official Result Portal)
        1: ("https://www.mha.gov.in/en/notifications/vacancies", "https://www.mha.gov.in/en/commoncontent/whats-new"),
        2: ("https://rrbapply.gov.in/#/auth/home", "https://indianrailways.gov.in/railwayboard/view_section.jsp?lang=0&id=0,7,1281"),
        3: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        4: ("https://uppbpb.gov.in/Home/Result", "https://uppbpb.gov.in/Home/Notice"),
        5: ("https://rrbapply.gov.in/#/auth/home", "https://indianrailways.gov.in/railwayboard/view_section.jsp?lang=0&id=0,7,1281"),
        6: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        7: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        8: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        43: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx"),

        # ADMIT CARDS & EXAM DATES (Candidate login / Hall ticket portal or Official Exam Date Notice)
        9: ("https://delhihighcourt.nic.in/public-notices/recruitment", "https://delhihighcourt.nic.in"),
        10: ("https://rrbapply.gov.in/#/auth/home", "https://rrbapply.gov.in"),
        11: ("https://rrbapply.gov.in/#/auth/home", "https://indianrailways.gov.in/railwayboard/view_section.jsp?lang=0&id=0,7,1281"),
        12: ("https://rrbapply.gov.in/#/auth/home", "https://rrbapply.gov.in"),
        13: ("https://ibpsonline.ibps.in/", "https://ibps.in"),
        14: ("https://ssc.gov.in/candidate-portal/admit-card", "https://ssc.gov.in"),
        15: ("https://ssc.gov.in/candidate-portal/admit-card", "https://ssc.gov.in"),
        16: ("https://ssc.gov.in/candidate-portal/admit-card", "https://ssc.gov.in"),

        # LATEST JOBS (Direct Application Form / Registration Portals)
        17: ("https://main.sci.gov.in/recruitment", "https://main.sci.gov.in"),
        18: ("https://dsssbonline.nic.in/", "https://dsssb.delhi.gov.in"),
        19: ("https://csjmu.ac.in/recruitment/", "https://csjmu.ac.in"),
        20: ("https://davstaff.org/application/", "https://davstaff.org"),
        21: ("https://rrcjaipur.in/ActApprentice2026/", "https://rrcjaipur.in"),
        22: ("https://esb.mponline.gov.in/", "https://esb.mp.gov.in"),
        23: ("https://onlinebpsc.bihar.gov.in/", "https://bpsc.bih.nic.in"),
        24: ("https://ssc.gov.in/portal/login", "https://ssc.gov.in"),
        44: ("https://ibpsreg.ibps.in/mpajul26/", "https://ibps.in"),
        45: ("https://rrbapply.gov.in/#/auth/home", "https://rrbapply.gov.in"),
        46: ("https://ibpsreg.ibps.in/nitrjul26/", "https://ibps.in"),

        # ANSWER KEYS (Direct Response Sheet / Answer Key & Objection Portals)
        25: ("https://esb.mp.gov.in/tacs/tac_2023/patwari_ans_key/", "https://esb.mp.gov.in"),
        26: ("https://rpsc.rajasthan.gov.in/candidateinformation/questionpapers", "https://rpsc.rajasthan.gov.in"),
        27: ("https://ukutet.com/", "https://ubse.uk.gov.in"),
        28: ("https://natboard.edu.in/", "https://natboard.edu.in"),
        29: ("https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in"),
        30: ("https://agnipathvayu.cdac.in/av-online/", "https://agnipathvayu.cdac.in"),

        # SYLLABUS (Direct Official Commission Syllabus Page)
        31: ("https://updeled.gov.in/", "https://updeled.gov.in"),
        32: ("https://ssc.gov.in/candidate-portal/syllabus", "https://ssc.gov.in"),
        33: ("https://ssc.gov.in/candidate-portal/syllabus", "https://ssc.gov.in"),
        34: ("https://updeled.gov.in/", "https://updeled.gov.in"),
        35: ("https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in"),
        36: ("https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in"),

        # ADMISSIONS (Direct Admission / Counselling Portals)
        37: ("https://gate2027.iitb.ac.in/apply/", "https://gate2027.iitb.ac.in"),
        38: ("https://jam2027.iitd.ac.in/apply/", "https://jam2027.iitd.ac.in"),
        39: ("https://uprtou.ac.in/admissions/", "https://uprtou.ac.in"),
        40: ("https://scholarship.up.gov.in/", "https://scholarship.up.gov.in"),
        41: ("https://iimcat.ac.in/", "https://iimcat.ac.in"),
        42: ("https://rimc.nta.nic.in/", "https://nta.ac.in"),
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
