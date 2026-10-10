"""
Top 25 Government Recruitment and Examination Portals in India.
Configured with polite request intervals, specific notice board targets, and domain rules.
"""

TOP_25_PORTALS = [
    # 1. Central Recruitment Commissions
    {
        "id": "ssc",
        "name": "Staff Selection Commission (SSC)",
        "url": "https://ssc.gov.in/notices",
        "base_url": "https://ssc.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["cgl", "chsl", "mts", "cpo", "je", "stenographer", "selection post"],
        "rate_limit_delay": 1.2
    },
    {
        "id": "upsc",
        "name": "Union Public Service Commission (UPSC)",
        "url": "https://upsc.gov.in/whats-new",
        "base_url": "https://upsc.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["civil services", "cse", "nda", "cds", "capf", "engineering services"],
        "rate_limit_delay": 1.2
    },
    {
        "id": "rrb",
        "name": "Railway Recruitment Boards (RRB)",
        "url": "https://rrbapply.gov.in",
        "base_url": "https://rrbapply.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["cen", "ntpc", "alp", "technician", "group d", "junior engineer"],
        "rate_limit_delay": 1.2
    },
    # 2. Banking & Financial Recruitment
    {
        "id": "ibps",
        "name": "Institute of Banking Personnel Selection (IBPS)",
        "url": "https://ibps.in",
        "base_url": "https://ibps.in",
        "default_category": "LATEST_JOB",
        "keywords": ["po", "clerk", "specialist officer", "rrb", "cwe", "crp"],
        "rate_limit_delay": 1.0
    },
    {
        "id": "sbi",
        "name": "State Bank of India (SBI Careers)",
        "url": "https://sbi.co.in/web/careers",
        "base_url": "https://sbi.co.in",
        "default_category": "LATEST_JOB",
        "keywords": ["probationary officer", "junior associate", "specialist cadre officer"],
        "rate_limit_delay": 1.0
    },
    # 3. National Testing & Admissions
    {
        "id": "nta",
        "name": "National Testing Agency (NTA)",
        "url": "https://nta.ac.in",
        "base_url": "https://nta.ac.in",
        "default_category": "ADMISSION",
        "keywords": ["jee", "neet", "cuet", "ugc net", "csir net", "cmat", "gpat"],
        "rate_limit_delay": 1.0
    },
    # 4. Uttar Pradesh State Boards (Top Traffic)
    {
        "id": "uppsc",
        "name": "Uttar Pradesh Public Service Commission (UPPSC)",
        "url": "https://uppsc.up.nic.in",
        "base_url": "https://uppsc.up.nic.in",
        "default_category": "LATEST_JOB",
        "keywords": ["pcs", "ro", "aro", "staff nurse", "combined state"],
        "rate_limit_delay": 1.5
    },
    {
        "id": "upsssc",
        "name": "Uttar Pradesh Subordinate Services (UPSSSC)",
        "url": "https://upsssc.gov.in",
        "base_url": "https://upsssc.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["pet", "lekhpal", "vdo", "forest guard", "junior assistant"],
        "rate_limit_delay": 1.5
    },
    {
        "id": "upprpb",
        "name": "UP Police Recruitment & Promotion Board (UPPRPB)",
        "url": "https://uppbpb.gov.in",
        "base_url": "https://uppbpb.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["constable", "sub inspector", "si", "assistant operator", "pet"],
        "rate_limit_delay": 1.5
    },
    # 5. Bihar State Boards
    {
        "id": "bpsc",
        "name": "Bihar Public Service Commission (BPSC)",
        "url": "https://bpsc.bih.nic.in",
        "base_url": "https://bpsc.bih.nic.in",
        "default_category": "LATEST_JOB",
        "keywords": ["tre", "school teacher", "bpsc cce", "assistant professor"],
        "rate_limit_delay": 1.5
    },
    {
        "id": "bssc",
        "name": "Bihar Staff Selection Commission (BSSC)",
        "url": "https://bssc.bihar.gov.in",
        "base_url": "https://bssc.bihar.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["cgl", "inter level", "stenographer", "instructor"],
        "rate_limit_delay": 1.5
    },
    {
        "id": "bpssc",
        "name": "Bihar Police Subordinate Services (BPSSC)",
        "url": "https://bpssc.bih.nic.in",
        "base_url": "https://bpssc.bih.nic.in",
        "default_category": "ADMIT_CARD",
        "keywords": ["sub inspector", "daroga", "sergeant", "fire service"],
        "rate_limit_delay": 1.5
    },
    # 6. Madhya Pradesh Boards
    {
        "id": "mpesb",
        "name": "MP Employees Selection Board (MPESB / Vyapam)",
        "url": "https://esb.mp.gov.in",
        "base_url": "https://esb.mp.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["patwari", "sub engineer", "police constable", "vanrakshak", "samvida"],
        "rate_limit_delay": 1.2
    },
    {
        "id": "mppsc",
        "name": "Madhya Pradesh Public Service Commission (MPPSC)",
        "url": "https://mppsc.mp.gov.in",
        "base_url": "https://mppsc.mp.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["state service", "forest service", "set", "assistant professor"],
        "rate_limit_delay": 1.2
    },
    # 7. Rajasthan State Boards
    {
        "id": "rpsc",
        "name": "Rajasthan Public Service Commission (RPSC)",
        "url": "https://rpsc.rajasthan.gov.in",
        "base_url": "https://rpsc.rajasthan.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["ras", "rts", "1st grade teacher", "2nd grade teacher", "sub inspector"],
        "rate_limit_delay": 1.2
    },
    {
        "id": "rsmssb",
        "name": "Rajasthan Staff Selection Board (RSMSSB)",
        "url": "https://rsmssb.rajasthan.gov.in",
        "base_url": "https://rsmssb.rajasthan.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["cet", "patwar", "vdo", "junior accountant", "cho"],
        "rate_limit_delay": 1.2
    },
    # 8. Delhi Government
    {
        "id": "dsssb",
        "name": "Delhi Subordinate Services Selection Board (DSSSB)",
        "url": "https://dsssbonline.nic.in",
        "base_url": "https://dsssbonline.nic.in",
        "default_category": "LATEST_JOB",
        "keywords": ["tgt", "pgt", "prt", "das", "warder", "special educator"],
        "rate_limit_delay": 1.2
    },
    # 9. Haryana & Uttarakhand
    {
        "id": "hssc",
        "name": "Haryana Staff Selection Commission (HSSC)",
        "url": "https://hssc.gov.in",
        "base_url": "https://hssc.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["cet group c", "cet group d", "police constable", "pgt"],
        "rate_limit_delay": 1.2
    },
    {
        "id": "ukpsc",
        "name": "Uttarakhand Public Service Commission (UKPSC)",
        "url": "https://psc.uk.gov.in",
        "base_url": "https://psc.uk.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["combined state civil", "ro aro", "patwari", "lekhpal", "forest guard"],
        "rate_limit_delay": 1.2
    },
    # 10. Defence & Paramilitary Forces
    {
        "id": "army",
        "name": "Indian Army (Join Indian Army)",
        "url": "https://joinindianarmy.nic.in",
        "base_url": "https://joinindianarmy.nic.in",
        "default_category": "LATEST_JOB",
        "keywords": ["agniveer", "tgc", "tes", "officer", "rally"],
        "rate_limit_delay": 1.5
    },
    {
        "id": "airforce",
        "name": "Indian Air Force (IAF Agnipath / AFCAT)",
        "url": "https://agnipathvayu.cdac.in",
        "base_url": "https://agnipathvayu.cdac.in",
        "default_category": "LATEST_JOB",
        "keywords": ["agniveervayu", "afcat", "intake", "airmen"],
        "rate_limit_delay": 1.5
    },
    {
        "id": "navy",
        "name": "Indian Navy (Join Indian Navy)",
        "url": "https://joinindiannavy.gov.in",
        "base_url": "https://joinindiannavy.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["agniveer ssr", "agniveer mr", "inet", "officers"],
        "rate_limit_delay": 1.5
    },
    {
        "id": "capf",
        "name": "Central Armed Police Forces (CRPF / CISF / BSF)",
        "url": "https://rect.crpf.gov.in",
        "base_url": "https://rect.crpf.gov.in",
        "default_category": "LATEST_JOB",
        "keywords": ["constable gd", "head constable", "tradesman", "asi steno"],
        "rate_limit_delay": 1.5
    },
    # 11. National Examinations & High Courts
    {
        "id": "gate",
        "name": "IIT GATE / JAM Admission Cell",
        "url": "https://gate2026.iit.ac.in",
        "base_url": "https://gate.iit.ac.in",
        "default_category": "ADMISSION",
        "keywords": ["gate", "jam", "postgraduate", "phd", "extended"],
        "rate_limit_delay": 1.0
    },
    {
        "id": "highcourt_allahabad",
        "name": "Allahabad High Court Recruitment Cell",
        "url": "https://allahabadhighcourt.in",
        "base_url": "https://allahabadhighcourt.in",
        "default_category": "LATEST_JOB",
        "keywords": ["ro aro", "hjs", "group c", "group d", "stenographer", "driver"],
        "rate_limit_delay": 1.2
    }
]
