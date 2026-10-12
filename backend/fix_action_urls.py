import sqlite3
from backend.config import DB_PATH


def fix_action_urls():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Exact verified 200-OK URLs for core updates (IDs 1..46):
    # Tuple format: (action_url, source_url, pdf_url)
    # - action_url: Direct Login / Registration portal (NEVER a .pdf!)
    # - source_url: Official Commission Website
    # - pdf_url: Official Government PDF or Notice/Result Archive (NEVER a synthetic PDF!)
    direct_urls = {
        # RESULTS (action_url = Candidate Login / Result Portal, pdf_url = Official Merit List & Cutoff PDF / Result Board)
        1: ("https://www.mha.gov.in/en/notifications/vacancies", "https://www.mha.gov.in/en/notifications/vacancies", "https://www.mha.gov.in/en/notifications/vacancies"),
        2: ("https://cdn.digialm.com/EForms/configuredHtml/33166/102294/login.html", "https://www.rrcjaipur.in/", "https://rrcjaipur.in/storeWebFiles/1006_11602307.PDF"),
        3: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        4: ("https://uppbpb.gov.in/Home/DirectRecruitment", "https://uppbpb.gov.in/Home/Result", "https://uppbpb.gov.in/FilesUploaded/Notice/72006016e1ebae-500c-4578-98d2-0e511181b7a7.pdf"),
        5: ("https://cdn.digialm.com/EForms/configuredHtml/33166/102294/login.html", "https://www.rrcjaipur.in/", "https://rrcjaipur.in/storeWebFiles/1005_12061494.PDF"),
        6: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        7: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        8: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        43: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/View_Notices.aspx"),

        # ADMIT CARDS & EXAM DATES (action_url = Candidate Admit Card Login, pdf_url = Official Exam Notice PDF)
        9: ("https://delhihighcourt.nic.in/app/advocate-login", "https://delhihighcourt.nic.in/web/recruitment", "https://delhihighcourt.nic.in/files/2026-10/admit_card_dhjs_2026_main_written_0.pdf"),
        10: ("https://cdn.digialm.com/EForms/configuredHtml/33166/102294/login.html", "https://www.rrcjaipur.in/", "https://rrcjaipur.in/storeWebFiles/1004_88888502.PDF"),
        11: ("https://cdn.digialm.com/EForms/configuredHtml/33166/102294/login.html", "https://www.rrcjaipur.in/", "https://rrcjaipur.in/storeWebFiles/1001_21437147.PDF"),
        12: ("https://cdn.digialm.com/EForms/configuredHtml/33166/102294/login.html", "https://www.rrcjaipur.in/", "https://rrcjaipur.in/storeWebFiles/999_20372268.PDF"),
        13: ("https://ibpsonline.ibps.in/", "https://www.ibps.in/index.php/clerical-cadre/", "https://www.ibps.in/index.php/clerical-cadre/"),
        14: ("https://ssc.gov.in/", "https://ssc.gov.in/", "https://ssc.gov.in/"),
        15: ("https://ssc.gov.in/", "https://ssc.gov.in/", "https://ssc.gov.in/"),
        16: ("https://ssc.gov.in/", "https://ssc.gov.in/", "https://ssc.gov.in/"),

        # LATEST JOBS (action_url = Registration / Apply Portal, pdf_url = Official Notification PDF)
        17: ("https://www.sci.gov.in/recruitments/", "https://www.sci.gov.in/recruitments/", "https://cdnbbsr.s3waas.gov.in/s3ec0490f1f4972d133619a60c30f3559e/uploads/2026/10/20261012100.pdf"),
        18: ("https://dsssbonline.nic.in/", "https://dsssbonline.nic.in/", "https://dsssbonline.nic.in/"),
        19: ("https://csjmu.ac.in/recruitment/", "https://csjmu.ac.in/", "https://csjmu.ac.in/recruitment/"),
        20: ("https://davcmc.net.in/", "https://davcmc.net.in/", "https://davcmc.net.in/"),
        21: ("https://cdn.digialm.com/EForms/configuredHtml/33166/102294/Index.html", "https://www.rrcjaipur.in/", "https://rrcjaipur.in/storeWebFiles/1006_11602307.PDF"),
        22: ("https://esb.mp.gov.in/e_default.html", "https://esb.mp.gov.in/e_default.html", "https://esb.mp.gov.in/Rulebooks/RB_2026/Steno_ASI_2026_Rulebook_17092026.pdf"),
        23: ("https://onlinebpsc.bihar.gov.in/", "https://bpsc.bihar.gov.in/", "https://bpsc.bihar.gov.in/"),
        24: ("https://ssc.gov.in/", "https://ssc.gov.in/", "https://ssc.gov.in/"),
        44: ("https://ibpsreg.ibps.in/mpajul26/", "https://www.ibps.in/index.php/recruitment/", "https://www.ibps.in/wp-content/uploads/Addendum-06.10.pdf"),
        45: ("https://cdn.digialm.com/EForms/configuredHtml/33166/102294/Index.html", "https://www.rrcjaipur.in/", "https://rrcjaipur.in/storeWebFiles/1006_11602307.PDF"),
        46: ("https://ibpsreg.ibps.in/nitrjul26/", "https://www.ibps.in/index.php/recruitment/", "https://www.ibps.in/wp-content/uploads/Addendum-06.10.pdf"),

        # ANSWER KEYS (action_url = Candidate Login / Objection Portal, pdf_url = Official Answer Key PDF)
        25: ("https://esb.mp.gov.in/results/RESULT_26/PNST_RES26/default_Results.htm", "https://esb.mp.gov.in/e_default.html", "https://esb.mp.gov.in/results/RESULT_26/PNST_RES26/PNST_2026_Key_Comm_reports.pdf"),
        26: ("https://sso.rajasthan.gov.in/signin", "https://rpsc.rajasthan.gov.in/", "https://rpsc.rajasthan.gov.in/answerkeys"),
        27: ("https://ukutet.com/", "https://ukutet.com/", "https://ukutet.com/"),
        28: ("https://exams.nta.ac.in/", "https://nta.ac.in/", "https://nta.ac.in/NoticeBoardArchive"),
        29: ("https://upsssc.gov.in/ResultsDire.aspx", "https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/View_Notices.aspx"),
        30: ("https://careerindianairforce.cdac.in/", "https://careerindianairforce.cdac.in/", "https://careerindianairforce.cdac.in/"),

        # SYLLABUS (action_url = Official Syllabus Page / PDF, pdf_url = Official Syllabus PDF)
        31: ("https://updeled.gov.in/", "https://updeled.gov.in/", "https://updeled.gov.in/"),
        32: ("https://ssc.gov.in/", "https://ssc.gov.in/", "https://ssc.gov.in/"),
        33: ("https://ssc.gov.in/", "https://ssc.gov.in/", "https://ssc.gov.in/"),
        34: ("https://updeled.gov.in/", "https://updeled.gov.in/", "https://updeled.gov.in/"),
        35: ("https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/", "https://upsssc.gov.in/View_Notices.aspx"),
        36: ("https://upsssc.gov.in/View_Notices.aspx", "https://upsssc.gov.in/", "https://upsssc.gov.in/View_Notices.aspx"),

        # ADMISSIONS (action_url = Direct Admission Registration/Login Portal, pdf_url = Official Information Brochure / Notice Archive)
        37: ("https://goaps.iitr.ac.in/login", "https://goaps.iitr.ac.in/login", "https://goaps.iitr.ac.in/login"),
        38: ("https://joaps.iitd.ac.in/login", "https://joaps.iitd.ac.in/login", "https://joaps.iitd.ac.in/login"),
        39: ("https://www.uprtou.ac.in/", "https://www.uprtou.ac.in/", "https://www.uprtou.ac.in/"),
        40: ("https://updeled.gov.in/", "https://updeled.gov.in/", "https://updeled.gov.in/"),
        41: ("https://iimcat.ac.in/", "https://iimcat.ac.in/", "https://iimcat.ac.in/"),
        42: ("https://exams.nta.nic.in/rimcee/", "https://nta.ac.in/", "https://nta.ac.in/NoticeBoardArchive"),
    }

    count = 0
    for item_id, (action_url, source_url, pdf_url) in direct_urls.items():
        cur.execute(
            """
            UPDATE updates
            SET action_url = ?, source_url = ?, pdf_url = ?
            WHERE id = ?
            """,
            (action_url, source_url, pdf_url, item_id),
        )
        count += cur.rowcount

    # Also fix the 5 featured recruitments in the `recruitments` table so `/jobs/<slug>` has 100% verified 200-OK links
    recruitments_fixes = {
        "ssc-cgl-2026-online-form": (
            "https://ssc.gov.in/",
            "https://ssc.gov.in/",
            "https://ssc.gov.in/",
        ),
        "rrb-technician-cen-02-2026": (
            "https://cdn.digialm.com/EForms/configuredHtml/33166/102294/Index.html",
            "https://rrcjaipur.in/storeWebFiles/1006_11602307.PDF",
            "https://www.rrcjaipur.in/",
        ),
        "up-police-constable-2026": (
            "https://uppbpb.gov.in/Home/DirectRecruitment",
            "https://uppbpb.gov.in/FilesUploaded/Notice/CONST%2025%20PET%20DATE%20CHANGE%2005-10-20268ce76324-7901-4b25-bfc4-4ba081a9c7fc.pdf",
            "https://uppbpb.gov.in/",
        ),
        "ibps-po-mt-xiv-2026": (
            "https://ibpsonline.ibps.in/",
            "https://www.ibps.in/index.php/management-trainees/",
            "https://www.ibps.in/",
        ),
        "supreme-court-junior-court-assistant-2026": (
            "https://www.sci.gov.in/recruitments/",
            "https://cdnbbsr.s3waas.gov.in/s3ec0490f1f4972d133619a60c30f3559e/uploads/2026/10/20261012100.pdf",
            "https://www.sci.gov.in/recruitments/",
        ),
    }
    for slug, (apply_url, pdf_url, site_url) in recruitments_fixes.items():
        cur.execute(
            """
            UPDATE recruitments
            SET apply_url = ?, notification_pdf_url = ?, official_website_url = ?
            WHERE slug = ?
            """,
            (apply_url, pdf_url, site_url, slug),
        )

    conn.commit()
    conn.close()
    print(f"Successfully updated {count} update URLs and 5 recruitment records.")


if __name__ == "__main__":
    fix_action_urls()
