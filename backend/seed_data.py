import json
from backend.database import get_connection, init_db

def seed():
    init_db()
    conn = get_connection()
    cur = conn.cursor()

    # Check if recruitments already seeded
    cur.execute("SELECT COUNT(*) FROM recruitments")
    count = cur.fetchone()[0]
    if count > 0:
        print(f"Database already contains {count} recruitments. Skipping initial seed.")
        conn.close()
        return

    recruitments = [
        (
            "SSC CGL 2026 Combined Graduate Level Examination",
            "ssc-cgl-2026-online-form",
            "Staff Selection Commission (SSC)",
            "Central",
            17727,
            "Bachelor Degree in Any Stream from Recognized University in India.",
            "18 - 32 Years (Age relaxation as per rules)",
            "General / OBC / EWS: ₹100 | SC / ST / PH / All Female: ₹0",
            "2026-06-24",
            "2026-07-24",
            "September - October 2026",
            "https://ssc.gov.in/portal/login",
            "https://ssc.gov.in/api/pdf/ssc-cgl-2026-notification.pdf",
            "https://ssc.gov.in",
            "Staff Selection Commission (SSC) has released the Combined Graduate Level CGL 2026 recruitment notification for 17,727 vacancies across various Group B & C central government departments.",
            "PUBLISHED"
        ),
        (
            "Railway RRB Technician CEN 02/2026 Online Form",
            "rrb-technician-cen-02-2026",
            "Railway Recruitment Boards (RRB)",
            "Railway",
            9144,
            "10th Matric with ITI / NCVT or 10+2 with Physics & Math or Diploma in Engineering.",
            "18 - 33 Years",
            "General / OBC / EWS: ₹500 | SC / ST / Ex-Servicemen: ₹250 (Refundable upon CBT)",
            "2026-03-09",
            "2026-04-08",
            "October - November 2026",
            "https://www.rrbapply.gov.in/#/auth/home",
            "https://www.rrbapply.gov.in/notices/CEN_02_2026.pdf",
            "https://indianrailways.gov.in",
            "Railway Recruitment Boards invite online applications for 9,144 Technician Grade I Signal and Technician Grade III vacancies in Indian Railways.",
            "PUBLISHED"
        ),
        (
            "UP Police Constable 60,244 Posts Recruitment 2026",
            "up-police-constable-2026",
            "UPPRPB Uttar Pradesh Police",
            "State Police",
            60244,
            "10+2 Intermediate Exam Passed from Any Recognized Board in India.",
            "18 - 25 Years (Male) | 18 - 28 Years (Female)",
            "All Categories: ₹400",
            "2026-01-01",
            "2026-01-16",
            "August 2026",
            "https://ccp123.onlinereg.co.in/",
            "https://uppbpb.gov.in/notice/police_constable_60244.pdf",
            "https://uppbpb.gov.in",
            "Uttar Pradesh Police Recruitment & Promotion Board (UPPRPB) invites online application for 60,244 Constable Civil Police posts.",
            "PUBLISHED"
        ),
        (
            "IBPS PO / MT XIV Recruitment 2026",
            "ibps-po-mt-xiv-2026",
            "Institute of Banking Personnel Selection (IBPS)",
            "Banking",
            4455,
            "Graduation Degree in Any Stream from Recognized University in India.",
            "20 - 30 Years",
            "General / OBC / EWS: ₹850 | SC / ST / PwD: ₹175",
            "2026-08-01",
            "2026-08-28",
            "October 2026",
            "https://ibpsonline.ibps.in/crppo14jul24/",
            "https://ibps.in/notification/cwe-po-mt-xiv.pdf",
            "https://ibps.in",
            "IBPS has invited applications for the recruitment of Probationary Officers (PO) / Management Trainees (MT) in Participating Commercial Banks.",
            "PUBLISHED"
        ),
        (
            "Supreme Court of India Junior Court Assistant Online Form 2026",
            "supreme-court-junior-court-assistant-2026",
            "Supreme Court of India (SCI)",
            "Court / Law",
            210,
            "Bachelor Degree in Any Stream with English Typing 35 wpm & Computer Knowledge.",
            "18 - 30 Years",
            "General / OBC / EWS: ₹500 | SC / ST / PH: ₹250",
            "2026-08-15",
            "2026-09-10",
            "November 2026",
            "https://main.sci.gov.in/recruitment",
            "https://main.sci.gov.in/notices/jca_recruitment_2026.pdf",
            "https://main.sci.gov.in",
            "Supreme Court of India (SCI) invites online applications for the post of Junior Court Assistant (Group B Non-Gazetted).",
            "PUBLISHED"
        )
    ]

    for rec in recruitments:
        cur.execute("""
            INSERT INTO recruitments (
                title, slug, organization, category, total_posts,
                qualification, age_limit, fee_details, start_date,
                last_date, exam_date, apply_url, notification_pdf_url,
                official_website_url, description, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, rec)

    # Seed Updates table across the 6 major SarkariResult columns
    updates = [
        # --- Results ---
        ("RESULT", "MHA IB MTS 2025 Final Result", "New", "https://mha.gov.in/result/ib-mts-2025", False, None),
        ("RESULT", "Railway RRB Ministerial & Isolated CEN 08/2025 Result", "New", "/api/pdf/2", False, None),
        ("RESULT", "UPSSSC Forest Guard 2023 PMT Result 2026 for 709 Post", "Hot", "/api/pdf/3", False, None),
        ("RESULT", "UP Police Home Guard Final Result 2026", "New", "/api/pdf/4", False, None),
        ("RESULT", "RRB Assistant Loco Pilot ALP CEN 01/2025 CBT II Result 2026", "Hot", "https://rrbapply.gov.in/#/auth/home", False, None),
        ("RESULT", "UPSSSC Enforcement Constable 2023 Final Result", "New", "/api/pdf/6", False, None),
        ("RESULT", "UPSSSC Havildar Instructor Result 2026", None, "/api/pdf/7", False, None),
        ("RESULT", "UPSSSC Platoon Commander, Block Organizer Result 2026", None, "/api/pdf/8", False, None),

        # --- Admit Cards ---
        ("ADMIT_CARD", "Delhi High Court HJS Mains Admit Card 2026", "New", "https://delhihighcourt.nic.in/public-notices/recruitment", False, None),
        ("ADMIT_CARD", "Railway RRB Technician CEN 02/2026 Admit Card", "Hot", "https://rrbapply.gov.in/#/auth/home", False, None),
        ("ADMIT_CARD", "Railway RRB Junior Engineer JE Revised Exam Date 2026", None, "/api/pdf/11", False, None),
        ("ADMIT_CARD", "Railway RRB Section Controller Exam City Details 2026", "Live", "https://rrbapply.gov.in/#/auth/home", False, None),
        ("ADMIT_CARD", "IBPS Clerk 16th Admit Card 2026", "New", "https://ibpsonline.ibps.in/", False, None),
        ("ADMIT_CARD", "SSC 10+2 CHSL Tier I Exam Date 2026", "Hot", "/api/pdf/14", False, None),
        ("ADMIT_CARD", "SSC CPO SI 2026 Exam Date", None, "/api/pdf/15", False, None),
        ("ADMIT_CARD", "SSC Junior Engineer JE 2026 Paper I Exam Date", None, "/api/pdf/16", False, None),

        # --- Latest Jobs ---
        ("LATEST_JOB", "Supreme Court of India Junior Court Assistant Online Form 2026", "New", "/jobs/supreme-court-junior-court-assistant-2026", True, "210 Posts"),
        ("LATEST_JOB", "Delhi DSSSB Various Post Online Form 2026", "New", "https://dsssbonline.nic.in/", False, None),
        ("LATEST_JOB", "CSJMU Kanpur Teaching Post Online Form 2026", None, "https://csjmu.ac.in/recruitment/", False, None),
        ("LATEST_JOB", "DAV Staff Various Post Online Form 2026", None, "https://davstaff.org/application/", False, None),
        ("LATEST_JOB", "NWR RRC Jaipur Apprentices Online Form 2026", "Hot", "https://rrcjaipur.in/ActApprentice2026/", False, None),
        ("LATEST_JOB", "MPESB Sub Engineer Online Form 2026 Re-Open", "Hot", "https://esb.mponline.gov.in/", False, None),
        ("LATEST_JOB", "Bihar Library Eligibility Test BLET Online Form 2026", "New", "https://onlinebpsc.bihar.gov.in/", False, None),
        ("LATEST_JOB", "SSC CGL 2026 Combined Graduate Level 17,727 Posts", "Hot", "/jobs/ssc-cgl-2026-online-form", True, "17,727 Posts"),

        # --- Answer Keys ---
        ("ANSWER_KEY", "MPESB Group 2 Sub Group 4 Patwari & Other Post Answer Key 2026", "New", "https://esb.mp.gov.in/tacs/tac_2023/patwari_ans_key/", False, None),
        ("ANSWER_KEY", "Rajasthan State Eligibility Test SET Answer Key 2026", None, "https://rpsc.rajasthan.gov.in/candidateinformation/questionpapers", False, None),
        ("ANSWER_KEY", "Uttarakhand UK TET UTET Answer Key 2026", "New", "https://ukutet.com/", False, None),
        ("ANSWER_KEY", "NBEMS NAT Board Group A B C Various Post Answer Key 2026", None, "/api/pdf/28", False, None),
        ("ANSWER_KEY", "UPSSSC Forest Guard / Wild Life Guard Mains Answer Key 2026", "Hot", "/api/pdf/29", False, None),
        ("ANSWER_KEY", "Indian Airforce Agniveervayu Intake 02/2027 Answer Key 2026", None, "https://agnipathvayu.cdac.in/av-online/", False, None),

        # --- Syllabus ---
        ("SYLLABUS", "UP Assistant Teacher Primary Class 1 to 5 Exam Syllabus 2026", "Hot", "/api/pdf/31", False, None),
        ("SYLLABUS", "SSC 10+2 CHSL Tier I, Tier II Exam Syllabus 2026", None, "/api/pdf/32", False, None),
        ("SYLLABUS", "SSC Junior Engineer JE 2026 Paper I & II Exam Syllabus", None, "/api/pdf/33", False, None),
        ("SYLLABUS", "UPESSC UP Super TET (Assistant Teacher) Primary & Junior Level Syllabus 2026", "Hot", "/api/pdf/34", False, None),
        ("SYLLABUS", "UPSSSC Veterinary Pharmacist Syllabus 2026", None, "/api/pdf/35", False, None),
        ("SYLLABUS", "UPSSSC Livestock Extension Officer Syllabus 2026", None, "/api/pdf/36", False, None),

        # --- Admissions ---
        ("ADMISSION", "IIT GATE 2027 Online Form | Extended", "Hot", "https://gate2027.iitb.ac.in/apply/", False, None),
        ("ADMISSION", "IIT JAM 2027 Online Form", None, "https://jam2027.iitd.ac.in/apply/", False, None),
        ("ADMISSION", "UPRTOU Ph.D Entrance Exam Admission Online Form 2026", None, "https://uprtou.ac.in/admissions/", False, None),
        ("ADMISSION", "UP Scholarship Online Form 2026 (All Course)", "Hot", "https://scholarship.up.gov.in/", False, None),
        ("ADMISSION", "IIM CAT Admission Online Form 2026 Date Extended", None, "https://iimcat.ac.in/", False, None),
        ("ADMISSION", "NTA RIMCEE Class 8th Admissions Online Form 2027", "New", "https://rimc.nta.nic.in/", False, None)
    ]

    for cat, title, tag, url, is_feat, feat_badge in updates:
        cur.execute("""
            INSERT INTO updates (category, title, tag, action_url, is_featured, featured_badge)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (cat, title, tag, url, 1 if is_feat else 0, feat_badge))

    # Seed monitored Watchdogs
    watchdogs = [
        ("Staff Selection Commission (SSC)", "https://ssc.gov.in", "LATEST_JOB"),
        ("Union Public Service Commission (UPSC)", "https://upsc.gov.in", "LATEST_JOB"),
        ("Railway Recruitment Board (RRB)", "https://rrbapply.gov.in", "ADMIT_CARD"),
        ("Uttar Pradesh SSSC (UPSSSC)", "https://upsssc.gov.in", "RESULT"),
        ("National Testing Agency (NTA)", "https://nta.ac.in", "ADMISSION"),
        ("Institute of Banking Personnel (IBPS)", "https://ibps.in", "LATEST_JOB")
    ]
    for name, url, cat in watchdogs:
        cur.execute("""
            INSERT INTO crawler_watchdogs (name, url, category, last_checked, status)
            VALUES (?, ?, ?, datetime('now'), 'ACTIVE')
        """, (name, url, cat))

    # Seed sample items in Staging Queue for Admin review demo
    staging_items = [
        (
            "SSC Portal (ssc.gov.in)",
            "https://ssc.gov.in/notices/chsl-2026-tier1-schedule",
            "SSC Combined Higher Secondary (10+2) Level Tier I Exam 2026 Schedule Released",
            "ADMIT_CARD",
            "https://ssc.gov.in/docs/notice_chsl_2026.pdf",
            "https://ssc.gov.in",
            json.dumps({
                "posts": "4500+",
                "exam_dates": "12-24 November 2026",
                "eligibility": "12th Standard or Equivalent",
                "age": "18-27 Years",
                "notes": "Automated watchdog matched regex on 'CHSL 2026 Examination Notice'"
            }),
            0.92
        ),
        (
            "UP Police Board (uppbpb.gov.in)",
            "https://uppbpb.gov.in/notice/sub-inspector-2026",
            "UP Police Sub Inspector (SI) & Platoon Commander 2026 Recruitment — 4,200 Posts",
            "LATEST_JOB",
            "https://uppbpb.gov.in/pdf/si_advt_2026.pdf",
            "https://uppbpb.gov.in",
            json.dumps({
                "posts": "4200",
                "fee": "₹400 for all",
                "eligibility": "Graduation in Any Stream",
                "age": "21-28 Years",
                "start_date": "2026-11-01",
                "last_date": "2026-11-30"
            }),
            0.88
        )
    ]
    for portal, surl, title, cat, pdf, aurl, raw_data, conf in staging_items:
        cur.execute("""
            INSERT INTO crawler_staging (
                source_portal, source_url, title, category,
                pdf_url, action_url, extracted_data, confidence_score, status
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'PENDING')
        """, (portal, surl, title, cat, pdf, aurl, raw_data, conf))

    conn.commit()
    conn.close()
    print("Database successfully seeded with realistic 2026 recruitment and update records!")

if __name__ == "__main__":
    seed()
