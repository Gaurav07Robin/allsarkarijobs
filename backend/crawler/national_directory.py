"""
Comprehensive National Directory of All Indian Government Recruitment Commissions,
State PSCs, Subordinate Boards, Defence Wings, and National Gazettes.
"""

NATIONAL_EXAM_DIRECTORY = [
    # ==========================================
    # 1. CENTRAL COMMISSIONS & ALL-INDIA BODIES
    # ==========================================
    {
        "id": "ssc",
        "name": "Staff Selection Commission (SSC)",
        "url": "https://ssc.gov.in/notices",
        "base_url": "https://ssc.gov.in",
        "sector": "Central",
        "state": "All India",
        "qualification": "10th/12th/Graduate",
        "keywords": ["cgl", "chsl", "mts", "cpo", "je", "stenographer", "selection post", "gd constable"]
    },
    {
        "id": "upsc",
        "name": "Union Public Service Commission (UPSC)",
        "url": "https://upsc.gov.in/whats-new",
        "base_url": "https://upsc.gov.in",
        "sector": "Central",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["civil services", "cse", "nda", "cds", "capf", "engineering services", "cms", "ies"]
    },
    {
        "id": "rrb",
        "name": "Railway Recruitment Boards (RRB / RRC)",
        "url": "https://rrbapply.gov.in",
        "base_url": "https://rrbapply.gov.in",
        "sector": "Railway",
        "state": "All India",
        "qualification": "10th/12th/Graduate",
        "keywords": ["cen", "ntpc", "alp", "technician", "group d", "junior engineer", "paramedical", "rrc"]
    },
    {
        "id": "employment_news",
        "name": "Official Employment News (Rozgar Samachar)",
        "url": "https://employmentnews.gov.in",
        "base_url": "https://employmentnews.gov.in",
        "sector": "Central",
        "state": "All India",
        "qualification": "All",
        "keywords": ["vacancy", "advertisement", "recruitment", "gazette", "notice"]
    },

    # ==========================================
    # 2. BANKING & INSURANCE RECRUITMENT
    # ==========================================
    {
        "id": "ibps",
        "name": "Institute of Banking Personnel Selection (IBPS)",
        "url": "https://ibps.in",
        "base_url": "https://ibps.in",
        "sector": "Bank",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["po", "clerk", "specialist officer", "rrb office assistant", "cwe", "crp"]
    },
    {
        "id": "sbi",
        "name": "State Bank of India (SBI Careers)",
        "url": "https://sbi.co.in/web/careers",
        "base_url": "https://sbi.co.in",
        "sector": "Bank",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["probationary officer", "junior associate", "specialist cadre officer", "circle based officer"]
    },
    {
        "id": "rbi",
        "name": "Reserve Bank of India (RBI Careers)",
        "url": "https://opportunities.rbi.org.in",
        "base_url": "https://rbi.org.in",
        "sector": "Bank",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["grade b officer", "assistant", "manager", "legal officer"]
    },
    {
        "id": "lic",
        "name": "Life Insurance Corporation of India (LIC)",
        "url": "https://licindia.in/careers",
        "base_url": "https://licindia.in",
        "sector": "Bank",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["ado", "aao", "assistant", "hfl"]
    },

    # ==========================================
    # 3. NATIONAL TESTING & ENTRANCE BOARDS
    # ==========================================
    {
        "id": "nta",
        "name": "National Testing Agency (NTA)",
        "url": "https://nta.ac.in",
        "base_url": "https://nta.ac.in",
        "sector": "Admission",
        "state": "All India",
        "qualification": "12th/Graduate",
        "keywords": ["jee main", "neet ug", "cuet ug", "cuet pg", "ugc net", "csir net", "cmat", "gpat"]
    },
    {
        "id": "gate_jam",
        "name": "IIT GATE / JAM Admission Cell",
        "url": "https://gate2026.iit.ac.in",
        "base_url": "https://gate.iit.ac.in",
        "sector": "Admission",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["gate", "jam", "postgraduate", "phd", "mtech admission"]
    },
    {
        "id": "cbse_ctet",
        "name": "CBSE Central Teacher Eligibility Test (CTET)",
        "url": "https://ctet.nic.in",
        "base_url": "https://ctet.nic.in",
        "sector": "Teaching",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["ctet", "eligibility", "paper 1", "paper 2", "admit card", "result"]
    },

    # ==========================================
    # 4. DEFENCE & PARAMILITARY FORCES
    # ==========================================
    {
        "id": "army",
        "name": "Indian Army (Join Indian Army)",
        "url": "https://joinindianarmy.nic.in",
        "base_url": "https://joinindianarmy.nic.in",
        "sector": "Defence",
        "state": "All India",
        "qualification": "10th/12th/Graduate",
        "keywords": ["agniveer general duty", "technical", "clerk", "tgc", "tes", "officer", "rally"]
    },
    {
        "id": "airforce",
        "name": "Indian Air Force (IAF Agnipath / AFCAT)",
        "url": "https://agnipathvayu.cdac.in",
        "base_url": "https://agnipathvayu.cdac.in",
        "sector": "Defence",
        "state": "All India",
        "qualification": "10th/12th/Graduate",
        "keywords": ["agniveervayu", "afcat", "airmen group x", "airmen group y", "intake"]
    },
    {
        "id": "navy",
        "name": "Indian Navy (Join Indian Navy)",
        "url": "https://joinindiannavy.gov.in",
        "base_url": "https://joinindiannavy.gov.in",
        "sector": "Defence",
        "state": "All India",
        "qualification": "10th/12th/Graduate",
        "keywords": ["agniveer ssr", "agniveer mr", "inet", "officers entry", "apprentice"]
    },
    {
        "id": "coastguard",
        "name": "Indian Coast Guard (ICG)",
        "url": "https://joinindiancoastguard.cdac.in",
        "base_url": "https://joinindiancoastguard.cdac.in",
        "sector": "Defence",
        "state": "All India",
        "qualification": "10th/12th",
        "keywords": ["navik gd", "navik db", "yantrik", "assistant commandant"]
    },
    {
        "id": "capf",
        "name": "Central Armed Police Forces (CRPF, BSF, CISF, ITBP, SSB)",
        "url": "https://rect.crpf.gov.in",
        "base_url": "https://rect.crpf.gov.in",
        "sector": "Defence",
        "state": "All India",
        "qualification": "10th/12th",
        "keywords": ["constable gd", "head constable", "tradesman", "asi steno", "sub inspector"]
    },

    # ==========================================
    # 5. UTTAR PRADESH STATE BOARDS
    # ==========================================
    {
        "id": "uppsc",
        "name": "Uttar Pradesh Public Service Commission (UPPSC)",
        "url": "https://uppsc.up.nic.in",
        "base_url": "https://uppsc.up.nic.in",
        "sector": "State",
        "state": "Uttar Pradesh",
        "qualification": "Graduate",
        "keywords": ["pcs", "ro aro", "staff nurse", "combined state civil", "gdc", "apo"]
    },
    {
        "id": "upsssc",
        "name": "Uttar Pradesh Subordinate Services (UPSSSC)",
        "url": "https://upsssc.gov.in",
        "base_url": "https://upsssc.gov.in",
        "sector": "State",
        "state": "Uttar Pradesh",
        "qualification": "10th/12th/Graduate",
        "keywords": ["pet", "lekhpal", "vdo", "forest guard", "junior assistant", "tubewell operator"]
    },
    {
        "id": "upprpb",
        "name": "UP Police Recruitment & Promotion Board (UPPRPB)",
        "url": "https://uppbpb.gov.in",
        "base_url": "https://uppbpb.gov.in",
        "sector": "Police",
        "state": "Uttar Pradesh",
        "qualification": "12th/Graduate",
        "keywords": ["constable civil", "sub inspector si", "radio operator", "pet", "fireman"]
    },
    {
        "id": "up_teacher",
        "name": "UP Basic & Secondary Education Board (UPTET / Super TET)",
        "url": "https://updeled.gov.in",
        "base_url": "https://updeled.gov.in",
        "sector": "Teaching",
        "state": "Uttar Pradesh",
        "qualification": "Graduate",
        "keywords": ["super tet", "uptet", "assistant teacher", "pgt", "tgt", "prt"]
    },

    # ==========================================
    # 6. BIHAR STATE BOARDS
    # ==========================================
    {
        "id": "bpsc",
        "name": "Bihar Public Service Commission (BPSC)",
        "url": "https://bpsc.bih.nic.in",
        "base_url": "https://bpsc.bih.nic.in",
        "sector": "State",
        "state": "Bihar",
        "qualification": "Graduate",
        "keywords": ["tre school teacher", "bpsc cce prelims", "bpsc 70th", "headmaster", "assistant engineer"]
    },
    {
        "id": "bssc",
        "name": "Bihar Staff Selection Commission (BSSC)",
        "url": "https://bssc.bihar.gov.in",
        "base_url": "https://bssc.bihar.gov.in",
        "sector": "State",
        "state": "Bihar",
        "qualification": "12th/Graduate",
        "keywords": ["inter level", "cgl graduate level", "stenographer", "laboratory assistant"]
    },
    {
        "id": "bpssc",
        "name": "Bihar Police Subordinate Services (BPSSC / CSBC)",
        "url": "https://bpssc.bih.nic.in",
        "base_url": "https://bpssc.bih.nic.in",
        "sector": "Police",
        "state": "Bihar",
        "qualification": "12th/Graduate",
        "keywords": ["police sub inspector", "daroga", "constable", "prohibition constable", "fireman"]
    },

    # ==========================================
    # 7. MADHYA PRADESH STATE BOARDS
    # ==========================================
    {
        "id": "mpesb",
        "name": "MP Employees Selection Board (MPESB / Vyapam)",
        "url": "https://esb.mp.gov.in",
        "base_url": "https://esb.mp.gov.in",
        "sector": "State",
        "state": "Madhya Pradesh",
        "qualification": "10th/12th/Graduate",
        "keywords": ["patwari", "sub engineer", "police constable", "vanrakshak", "group 2", "group 4", "samvida"]
    },
    {
        "id": "mppsc",
        "name": "Madhya Pradesh Public Service Commission (MPPSC)",
        "url": "https://mppsc.mp.gov.in",
        "base_url": "https://mppsc.mp.gov.in",
        "sector": "State",
        "state": "Madhya Pradesh",
        "qualification": "Graduate",
        "keywords": ["state service examination", "state forest service", "set", "assistant professor"]
    },

    # ==========================================
    # 8. RAJASTHAN STATE BOARDS
    # ==========================================
    {
        "id": "rpsc",
        "name": "Rajasthan Public Service Commission (RPSC)",
        "url": "https://rpsc.rajasthan.gov.in",
        "base_url": "https://rpsc.rajasthan.gov.in",
        "sector": "State",
        "state": "Rajasthan",
        "qualification": "Graduate",
        "keywords": ["ras rts", "1st grade teacher", "2nd grade senior teacher", "sub inspector", "college lecturer"]
    },
    {
        "id": "rsmssb",
        "name": "Rajasthan Staff Selection Board (RSMSSB)",
        "url": "https://rsmssb.rajasthan.gov.in",
        "base_url": "https://rsmssb.rajasthan.gov.in",
        "sector": "State",
        "state": "Rajasthan",
        "qualification": "12th/Graduate",
        "keywords": ["cet senior secondary", "cet graduate", "patwar", "vdo", "junior accountant", "cho"]
    },

    # ==========================================
    # 9. DELHI, HARYANA & UTTARAKHAND BOARDS
    # ==========================================
    {
        "id": "dsssb",
        "name": "Delhi Subordinate Services Selection Board (DSSSB)",
        "url": "https://dsssbonline.nic.in",
        "base_url": "https://dsssbonline.nic.in",
        "sector": "State",
        "state": "Delhi",
        "qualification": "10th/12th/Graduate",
        "keywords": ["tgt", "pgt", "prt primary teacher", "warder", "junior judicial assistant", "das grade"]
    },
    {
        "id": "delhi_high_court",
        "name": "Delhi High Court Examination Cell",
        "url": "https://delhihighcourt.nic.in",
        "base_url": "https://delhihighcourt.nic.in",
        "sector": "State",
        "state": "Delhi",
        "qualification": "Graduate",
        "keywords": ["higher judicial service hjs", "judicial service djs", "senior personal assistant", "jja"]
    },
    {
        "id": "hssc",
        "name": "Haryana Staff Selection Commission (HSSC)",
        "url": "https://hssc.gov.in",
        "base_url": "https://hssc.gov.in",
        "sector": "State",
        "state": "Haryana",
        "qualification": "10th/12th/Graduate",
        "keywords": ["cet group c", "cet group d", "police constable", "patwari", "gram sachiv"]
    },
    {
        "id": "ukpsc",
        "name": "Uttarakhand Public Service Commission (UKPSC)",
        "url": "https://psc.uk.gov.in",
        "base_url": "https://psc.uk.gov.in",
        "sector": "State",
        "state": "Uttarakhand",
        "qualification": "12th/Graduate",
        "keywords": ["combined state civil", "ro aro", "patwari", "lekhpal", "forest guard", "constable"]
    },

    # ==========================================
    # 10. JUDICIARY & HIGH COURTS
    # ==========================================
    {
        "id": "sci",
        "name": "Supreme Court of India (SCI)",
        "url": "https://main.sci.gov.in/recruitment",
        "base_url": "https://main.sci.gov.in",
        "sector": "Central",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["junior court assistant", "court attendant", "chamber attendant", "law clerk"]
    },
    {
        "id": "allahabad_hc",
        "name": "Allahabad High Court Recruitment Cell",
        "url": "https://allahabadhighcourt.in",
        "base_url": "https://allahabadhighcourt.in",
        "sector": "State",
        "state": "Uttar Pradesh",
        "qualification": "10th/12th/Graduate",
        "keywords": ["group c", "group d", "ro aro review officer", "stenographer", "driver", "peon"]
    },

    # ==========================================
    # 11. NATIONAL PSUs & RESEARCH ORGANIZATIONS
    # ==========================================
    {
        "id": "drdo",
        "name": "Defence Research & Development Organisation (DRDO)",
        "url": "https://drdo.gov.in/careers",
        "base_url": "https://drdo.gov.in",
        "sector": "Central",
        "state": "All India",
        "qualification": "Diploma/Graduate",
        "keywords": ["ceptam", "scientist b", "senior technical assistant", "technician a"]
    },
    {
        "id": "isro",
        "name": "Indian Space Research Organisation (ISRO)",
        "url": "https://isro.gov.in/careers",
        "base_url": "https://isro.gov.in",
        "sector": "Central",
        "state": "All India",
        "qualification": "Diploma/Graduate",
        "keywords": ["icrb", "scientist engineer", "technical assistant", "draughtsman", "technician"]
    },

    # ==========================================
    # 12. CENTRAL TEACHING & NATIONAL ELIGIBILITY
    # ==========================================
    {
        "id": "kvs",
        "name": "Kendriya Vidyalaya Sangathan (KVS)",
        "url": "https://kvsangathan.nic.in/employment-notice",
        "base_url": "https://kvsangathan.nic.in",
        "sector": "Teaching",
        "state": "All India",
        "qualification": "Graduate/B.Ed",
        "keywords": ["prt", "tgt", "pgt", "principal", "assistant commissioner", "librarian"]
    },
    {
        "id": "nvs",
        "name": "Navodaya Vidyalaya Samiti (NVS)",
        "url": "https://navodaya.gov.in/nvs/en/recruitment",
        "base_url": "https://navodaya.gov.in",
        "sector": "Teaching",
        "state": "All India",
        "qualification": "Graduate/B.Ed",
        "keywords": ["tgt", "pgt", "music teacher", "art teacher", "pet", "warden", "junior secretarial"]
    },
    {
        "id": "emrs",
        "name": "Eklavya Model Residential Schools (EMRS / NESTS)",
        "url": "https://emrs.tribal.gov.in",
        "base_url": "https://emrs.tribal.gov.in",
        "sector": "Teaching",
        "state": "All India",
        "qualification": "Graduate/B.Ed",
        "keywords": ["teaching staff", "hostel warden", "accountant", "lab attendant", "pgt", "tgt"]
    },
    {
        "id": "ugc_net",
        "name": "NTA UGC National Eligibility Test (UGC NET)",
        "url": "https://ugcnet.nta.ac.in",
        "base_url": "https://ugcnet.nta.ac.in",
        "sector": "Teaching",
        "state": "All India",
        "qualification": "Post Graduate",
        "keywords": ["jrf", "assistant professor", "phd admission", "admit card", "answer key", "scorecard"]
    },
    {
        "id": "csir_net",
        "name": "Joint CSIR-UGC NET for Science",
        "url": "https://csirnet.nta.ac.in",
        "base_url": "https://csirnet.nta.ac.in",
        "sector": "Teaching",
        "state": "All India",
        "qualification": "Post Graduate",
        "keywords": ["csir net", "junior research fellowship", "lectureship", "chemical sciences", "physical"]
    },

    # ==========================================
    # 13. MAHARATNA & NAVRATNA PSUs
    # ==========================================
    {
        "id": "barc",
        "name": "Bhabha Atomic Research Centre (BARC / DAE)",
        "url": "https://barc.gov.in/careers",
        "base_url": "https://barc.gov.in",
        "sector": "PSU",
        "state": "All India",
        "qualification": "Diploma/Graduate",
        "keywords": ["stipendiary trainee", "scientific assistant", "technician", "ocss", "dges"]
    },
    {
        "id": "aai",
        "name": "Airports Authority of India (AAI Careers)",
        "url": "https://aai.aero/en/careers/recruitment",
        "base_url": "https://aai.aero",
        "sector": "PSU",
        "state": "All India",
        "qualification": "Graduate/Engg",
        "keywords": ["junior executive atc", "air traffic control", "airport operations", "apprentice"]
    },
    {
        "id": "ongc",
        "name": "Oil and Natural Gas Corporation (ONGC)",
        "url": "https://ongcindia.com/web/eng/career",
        "base_url": "https://ongcindia.com",
        "sector": "PSU",
        "state": "All India",
        "qualification": "Diploma/Graduate",
        "keywords": ["graduate trainee", "apprentice", "non executive", "gate score", "engineer"]
    },
    {
        "id": "iocl",
        "name": "Indian Oil Corporation Limited (IOCL)",
        "url": "https://iocl.com/latest-job-opening",
        "base_url": "https://iocl.com",
        "sector": "PSU",
        "state": "All India",
        "qualification": "10th/ITI/Diploma/Graduate",
        "keywords": ["trade apprentice", "technician apprentice", "junior engineering assistant", "officers"]
    },
    {
        "id": "ntpc",
        "name": "National Thermal Power Corporation (NTPC)",
        "url": "https://careers.ntpc.co.in",
        "base_url": "https://careers.ntpc.co.in",
        "sector": "PSU",
        "state": "All India",
        "qualification": "Engg/Graduate",
        "keywords": ["executive trainee", "engineering executive trainee", "diploma trainee", "et"]
    },
    {
        "id": "bhel",
        "name": "Bharat Heavy Electricals Limited (BHEL)",
        "url": "https://careers.bhel.in",
        "base_url": "https://careers.bhel.in",
        "sector": "PSU",
        "state": "All India",
        "qualification": "Diploma/Graduate",
        "keywords": ["engineer trainee", "supervisor trainee", "artisan", "trade apprentice"]
    },
    {
        "id": "sail",
        "name": "Steel Authority of India Limited (SAIL)",
        "url": "https://sailcareers.com",
        "base_url": "https://sailcareers.com",
        "sector": "PSU",
        "state": "All India",
        "qualification": "ITI/Diploma/Graduate",
        "keywords": ["management trainee", "octt operator cum technician", "actt attendant", "bokaro", "bhilai", "rourkela"]
    },
    {
        "id": "coalindia",
        "name": "Coal India Limited (CIL)",
        "url": "https://coalindia.in/careers",
        "base_url": "https://coalindia.in",
        "sector": "PSU",
        "state": "All India",
        "qualification": "Graduate/Engg",
        "keywords": ["management trainee mt", "mining", "electrical", "mechanical", "civil", "systems"]
    },
    {
        "id": "powergrid",
        "name": "Power Grid Corporation of India (PGCIL)",
        "url": "https://powergrid.in/job-opportunities",
        "base_url": "https://powergrid.in",
        "sector": "PSU",
        "state": "All India",
        "qualification": "Diploma/Graduate",
        "keywords": ["diploma trainee", "engineer trainee", "field engineer", "junior officer trainee"]
    },
    {
        "id": "bel",
        "name": "Bharat Electronics Limited (BEL)",
        "url": "https://bel-india.in/careers",
        "base_url": "https://bel-india.in",
        "sector": "PSU",
        "state": "All India",
        "qualification": "Engg/Graduate",
        "keywords": ["project engineer", "trainee engineer", "deputy manager", "probationary engineer"]
    },
    {
        "id": "hal",
        "name": "Hindustan Aeronautics Limited (HAL)",
        "url": "https://hal-india.co.in/Career",
        "base_url": "https://hal-india.co.in",
        "sector": "PSU",
        "state": "All India",
        "qualification": "Diploma/Engg",
        "keywords": ["management trainee", "design trainee", "technician", "diploma apprentice"]
    },

    # ==========================================
    # 14. REGULATORY, FINANCE & APEX BODIES
    # ==========================================
    {
        "id": "nabard",
        "name": "National Bank for Agriculture & Rural Development (NABARD)",
        "url": "https://nabard.org/careers-notices",
        "base_url": "https://nabard.org",
        "sector": "Bank",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["assistant manager grade a", "manager grade b", "development assistant"]
    },
    {
        "id": "sebi",
        "name": "Securities and Exchange Board of India (SEBI)",
        "url": "https://sebi.gov.in/sebiweb/other/career.jsp",
        "base_url": "https://sebi.gov.in",
        "sector": "Bank",
        "state": "All India",
        "qualification": "Graduate/Post Graduate",
        "keywords": ["officer grade a assistant manager", "general stream", "legal stream", "information technology"]
    },
    {
        "id": "sidbi",
        "name": "Small Industries Development Bank of India (SIDBI)",
        "url": "https://sidbi.in/en/careers",
        "base_url": "https://sidbi.in",
        "sector": "Bank",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["grade a assistant manager", "generalist", "specialist officer"]
    },
    {
        "id": "niacl",
        "name": "New India Assurance Co. Ltd. (NIACL)",
        "url": "https://newindia.co.in/portal/careers",
        "base_url": "https://newindia.co.in",
        "sector": "Bank",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["administrative officer ao", "assistant recruitment", "scale 1"]
    },
    {
        "id": "uiic",
        "name": "United India Insurance Company (UIIC)",
        "url": "https://uiic.co.in/careers",
        "base_url": "https://uiic.co.in",
        "sector": "Bank",
        "state": "All India",
        "qualification": "Graduate",
        "keywords": ["administrative officer", "assistant", "ao recruitment"]
    },

    # ==========================================
    # 15. WEST BENGAL STATE BOARDS
    # ==========================================
    {
        "id": "wbpsc",
        "name": "West Bengal Public Service Commission (WBPSC)",
        "url": "https://psc.wb.gov.in",
        "base_url": "https://psc.wb.gov.in",
        "sector": "State",
        "state": "West Bengal",
        "qualification": "10th/12th/Graduate",
        "keywords": ["wbcs civil service", "miscellaneous", "clerkship", "food si", "audit & accounts"]
    },
    {
        "id": "wbprb",
        "name": "West Bengal Police Recruitment Board (WBPRB)",
        "url": "https://prb.wb.gov.in",
        "base_url": "https://prb.wb.gov.in",
        "sector": "Police",
        "state": "West Bengal",
        "qualification": "10th/12th/Graduate",
        "keywords": ["constable", "lady constable", "sub inspector", "kolkata police", "wireless operator"]
    },

    # ==========================================
    # 16. JHARKHAND & ODISHA BOARDS
    # ==========================================
    {
        "id": "jpsc",
        "name": "Jharkhand Public Service Commission (JPSC)",
        "url": "https://jpsc.gov.in",
        "base_url": "https://jpsc.gov.in",
        "sector": "State",
        "state": "Jharkhand",
        "qualification": "Graduate",
        "keywords": ["combined civil services", "cdpo", "medical officer", "veterinary officer"]
    },
    {
        "id": "jssc",
        "name": "Jharkhand Staff Selection Commission (JSSC)",
        "url": "https://jssc.nic.in",
        "base_url": "https://jssc.nic.in",
        "sector": "State",
        "state": "Jharkhand",
        "qualification": "10th/12th/Graduate",
        "keywords": ["jssc cgl", "jcce constable", "lady supervisor", "pgttce", "lab assistant"]
    },
    {
        "id": "opsc",
        "name": "Odisha Public Service Commission (OPSC)",
        "url": "https://opsc.gov.in",
        "base_url": "https://opsc.gov.in",
        "sector": "State",
        "state": "Odisha",
        "qualification": "Graduate",
        "keywords": ["oas civil services", "medical officer", "assistant professor", "aso assistant section officer"]
    },
    {
        "id": "osssc",
        "name": "Odisha Sub-ordinate Employee Selection (OSSSC)",
        "url": "https://osssc.gov.in",
        "base_url": "https://osssc.gov.in",
        "sector": "State",
        "state": "Odisha",
        "qualification": "10th/12th/Graduate",
        "keywords": ["cre combined recruitment", "ri revenue inspector", "ari", "amin", "peo panchayat"]
    },
    {
        "id": "ossc",
        "name": "Odisha Staff Selection Commission (OSSC)",
        "url": "https://ossc.gov.in",
        "base_url": "https://ossc.gov.in",
        "sector": "State",
        "state": "Odisha",
        "qualification": "Graduate",
        "keywords": ["cgl combined graduate level", "ctsre", "traffic constable", "accountant"]
    },

    # ==========================================
    # 17. CHHATTISGARH BOARDS
    # ==========================================
    {
        "id": "cgpsc",
        "name": "Chhattisgarh Public Service Commission (CGPSC)",
        "url": "https://psc.cg.gov.in",
        "base_url": "https://psc.cg.gov.in",
        "sector": "State",
        "state": "Chhattisgarh",
        "qualification": "Graduate",
        "keywords": ["state service examination sse", "civil judge", "assistant professor", "veterinary"]
    },
    {
        "id": "cgvyapam",
        "name": "Chhattisgarh Professional Examination Board (CG Vyapam)",
        "url": "https://vyapam.cgstate.gov.in",
        "base_url": "https://vyapam.cgstate.gov.in",
        "sector": "State",
        "state": "Chhattisgarh",
        "qualification": "12th/Graduate",
        "keywords": ["hostel warden", "shikshak teacher", "patwari", "mandi inspector", "constable"]
    },

    # ==========================================
    # 18. GUJARAT & MAHARASHTRA BOARDS
    # ==========================================
    {
        "id": "gpsc",
        "name": "Gujarat Public Service Commission (GPSC)",
        "url": "https://gpsc.gujarat.gov.in",
        "base_url": "https://gpsc.gujarat.gov.in",
        "sector": "State",
        "state": "Gujarat",
        "qualification": "Graduate",
        "keywords": ["class 1 2 administrative", "taluka development officer", "deputy collector", "pi"]
    },
    {
        "id": "gsssb",
        "name": "Gujarat Subordinate Service Selection (GSSSB)",
        "url": "https://gsssb.gujarat.gov.in",
        "base_url": "https://gsssb.gujarat.gov.in",
        "sector": "State",
        "state": "Gujarat",
        "qualification": "12th/Graduate",
        "keywords": ["cce combined competitive", "junior clerk", "senior clerk", "head clerk", "bin sachivalay"]
    },
    {
        "id": "mpsc",
        "name": "Maharashtra Public Service Commission (MPSC)",
        "url": "https://mpsc.gov.in",
        "base_url": "https://mpsc.gov.in",
        "sector": "State",
        "state": "Maharashtra",
        "qualification": "Graduate",
        "keywords": ["rajyaseva civil service", "combine group b group c", "psi", "sti", "aso", "mes"]
    },

    # ==========================================
    # 19. PUNJAB & HIMACHAL PRADESH BOARDS
    # ==========================================
    {
        "id": "ppsc",
        "name": "Punjab Public Service Commission (PPSC)",
        "url": "https://ppsc.gov.in",
        "base_url": "https://ppsc.gov.in",
        "sector": "State",
        "state": "Punjab",
        "qualification": "Graduate",
        "keywords": ["punjab civil services", "naib tehsildar", "section officer", "veterinary officer"]
    },
    {
        "id": "psssb",
        "name": "Punjab Subordinate Services Selection Board (PSSSB)",
        "url": "https://sssb.punjab.gov.in",
        "base_url": "https://sssb.punjab.gov.in",
        "sector": "State",
        "state": "Punjab",
        "qualification": "10th/12th/Graduate",
        "keywords": ["clerk", "patwari", "senior assistant", "fireman", "vet inspector"]
    },
    {
        "id": "hppsc",
        "name": "Himachal Pradesh Public Service Commission (HPPSC)",
        "url": "https://hppsc.hp.gov.in",
        "base_url": "https://hppsc.hp.gov.in",
        "sector": "State",
        "state": "Himachal Pradesh",
        "qualification": "Graduate",
        "keywords": ["hpas administrative service", "naib tehsildar", "assistant engineer", "lecturer"]
    },

    # ==========================================
    # 20. ANDHRA PRADESH & TELANGANA BOARDS
    # ==========================================
    {
        "id": "appsc",
        "name": "Andhra Pradesh Public Service Commission (APPSC)",
        "url": "https://psc.ap.gov.in",
        "base_url": "https://psc.ap.gov.in",
        "sector": "State",
        "state": "South India",
        "qualification": "Graduate",
        "keywords": ["group 1 services", "group 2 services", "degree college lecturers", "polytechnic"]
    },
    {
        "id": "tgpsc",
        "name": "Telangana Public Service Commission (TGPSC / TSPSC)",
        "url": "https://tspsc.gov.in",
        "base_url": "https://tspsc.gov.in",
        "sector": "State",
        "state": "South India",
        "qualification": "Graduate",
        "keywords": ["group 1", "group 2", "group 3", "group 4", "assistant executive engineer"]
    },
    {
        "id": "tslprb",
        "name": "Telangana State Police Recruitment Board (TSLPRB)",
        "url": "https://tslprb.in",
        "base_url": "https://tslprb.in",
        "sector": "Police",
        "state": "South India",
        "qualification": "12th/Graduate",
        "keywords": ["police constable", "sub inspector si", "communication constable", "transport"]
    },

    # ==========================================
    # 21. TAMIL NADU, KARNATAKA & KERALA BOARDS
    # ==========================================
    {
        "id": "tnpsc",
        "name": "Tamil Nadu Public Service Commission (TNPSC)",
        "url": "https://tnpsc.gov.in",
        "base_url": "https://tnpsc.gov.in",
        "sector": "State",
        "state": "South India",
        "qualification": "10th/12th/Graduate",
        "keywords": ["group 1", "group 2", "group 2a", "group 4 vao", "combined civil services"]
    },
    {
        "id": "tnusrb",
        "name": "Tamil Nadu Uniformed Services (TNUSRB)",
        "url": "https://tnusrb.tn.gov.in",
        "base_url": "https://tnusrb.tn.gov.in",
        "sector": "Police",
        "state": "South India",
        "qualification": "10th/12th/Graduate",
        "keywords": ["constable grade ii", "sub inspector si", "jail warder", "fireman"]
    },
    {
        "id": "kpsc_kar",
        "name": "Karnataka Public Service Commission (KPSC)",
        "url": "https://kpsc.kar.nic.in",
        "base_url": "https://kpsc.kar.nic.in",
        "sector": "State",
        "state": "South India",
        "qualification": "Graduate",
        "keywords": ["kas gazetted probationers", "fda first division assistant", "sda", "group c"]
    },
    {
        "id": "kerala_psc",
        "name": "Kerala Public Service Commission (Kerala PSC)",
        "url": "https://keralapsc.gov.in",
        "base_url": "https://keralapsc.gov.in",
        "sector": "State",
        "state": "South India",
        "qualification": "10th/12th/Graduate",
        "keywords": ["thulasi", "kas kerala administrative", "ldc lower division clerk", "secretariat assistant", "cpo"]
    },

    # ==========================================
    # 22. ASSAM, NORTH EAST & JAMMU & KASHMIR
    # ==========================================
    {
        "id": "apsc_assam",
        "name": "Assam Public Service Commission (APSC)",
        "url": "https://apsc.nic.in",
        "base_url": "https://apsc.nic.in",
        "sector": "State",
        "state": "Assam / NE",
        "qualification": "Graduate",
        "keywords": ["cce combined competitive", "assistant engineer", "inspector of schools", "finance service"]
    },
    {
        "id": "adre_assam",
        "name": "Assam Direct Recruitment Commission (ADRE Grade 3 & 4)",
        "url": "https://slprbassam.in",
        "base_url": "https://slprbassam.in",
        "sector": "State",
        "state": "Assam / NE",
        "qualification": "10th/12th/Graduate",
        "keywords": ["grade iii", "grade iv", "police constable", "sub inspector", "adre result"]
    },
    {
        "id": "jkpsc",
        "name": "J&K Public Service Commission (JKPSC)",
        "url": "https://jkpsc.nic.in",
        "base_url": "https://jkpsc.nic.in",
        "sector": "State",
        "state": "J&K",
        "qualification": "Graduate",
        "keywords": ["cce combined competitive", "medical officer", "assistant professor", "prosecuting officer"]
    },
    {
        "id": "jkssb",
        "name": "J&K Services Selection Board (JKSSB)",
        "url": "https://jkssb.nic.in",
        "base_url": "https://jkssb.nic.in",
        "sector": "State",
        "state": "J&K",
        "qualification": "10th/12th/Graduate",
        "keywords": ["panchayat secretary", "police sub inspector", "accounts assistant", "junior assistant"]
    },

    # ==========================================
    # 23. HIGH COURTS OF INDIA
    # ==========================================
    {
        "id": "patna_hc",
        "name": "Patna High Court Recruitment Cell",
        "url": "https://patnahighcourt.gov.in",
        "base_url": "https://patnahighcourt.gov.in",
        "sector": "Judiciary",
        "state": "Bihar",
        "qualification": "12th/Graduate",
        "keywords": ["assistant", "stenographer", "district judge", "computer operator", "translator"]
    },
    {
        "id": "bombay_hc",
        "name": "Bombay High Court Examination Cell",
        "url": "https://bombayhighcourt.nic.in",
        "base_url": "https://bombayhighcourt.nic.in",
        "sector": "Judiciary",
        "state": "Maharashtra",
        "qualification": "10th/12th/Graduate",
        "keywords": ["stenographer", "junior clerk", "peon hamal", "system officer", "civil judge"]
    },
    {
        "id": "rajasthan_hc",
        "name": "Rajasthan High Court Recruitment",
        "url": "https://hcraj.nic.in",
        "base_url": "https://hcraj.nic.in",
        "sector": "Judiciary",
        "state": "Rajasthan",
        "qualification": "12th/Graduate",
        "keywords": ["ldc clerk grade ii", "junior judicial assistant", "stenographer", "civil judge rjs"]
    },
    {
        "id": "mphc",
        "name": "Madhya Pradesh High Court",
        "url": "https://mphc.gov.in",
        "base_url": "https://mphc.gov.in",
        "sector": "Judiciary",
        "state": "Madhya Pradesh",
        "qualification": "12th/Graduate",
        "keywords": ["jja junior judicial assistant", "stenographer grade 2", "assistant grade 3", "civil judge"]
    },
    {
        "id": "highcourtchd",
        "name": "Punjab and Haryana High Court",
        "url": "https://highcourtchd.gov.in",
        "base_url": "https://highcourtchd.gov.in",
        "sector": "Judiciary",
        "state": "Haryana",
        "qualification": "Graduate",
        "keywords": ["clerk subordinate courts", "stenographer", "driver", "restorer", "hcs judicial"]
    },
    {
        "id": "calcutta_hc",
        "name": "Calcutta High Court Recruitment Cell",
        "url": "https://calcuttahighcourt.gov.in",
        "base_url": "https://calcuttahighcourt.gov.in",
        "sector": "Judiciary",
        "state": "West Bengal",
        "qualification": "10th/12th/Graduate",
        "keywords": ["lower division assistant lda", "stenographer", "group d", "data entry operator"]
    },
    {
        "id": "madras_hc",
        "name": "Madras High Court Judicial Recruitment",
        "url": "https://hcmadras.tn.gov.in",
        "base_url": "https://hcmadras.tn.gov.in",
        "sector": "Judiciary",
        "state": "South India",
        "qualification": "8th/10th/Graduate",
        "keywords": ["examiner", "reader", "senior bailiff", "junior bailiff", "xerox operator", "civil judge"]
    }
]
