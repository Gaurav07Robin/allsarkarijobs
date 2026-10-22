import re
import json
from pathlib import Path
from backend.config import BASE_DIR

LANDING_PAGES = [
    # Qualifications
    {
        "slug": "10th-pass",
        "title": "10th Pass Govt Jobs 2026–2027 – Post Office GDS, Railway Group D, MTS & Constable | All Sarkari Jobs",
        "desc": "Find active 10th pass government job vacancies 2026–2027. Apply online for India Post GDS, SSC MTS, Railway Group D, and State Police Constable with eligibility criteria and direct links.",
        "keywords": "10th pass govt jobs 2026 2027, 10th pass sarkari naukri, india post gds apply online, ssc mts vacancy, railway group d 10th pass, police constable 10th pass, All Sarkari Jobs",
        "heading": "10th Pass Government Jobs 2026–2027",
        "filter_pill": "10th",
        "search_term": ""
    },
    {
        "slug": "12th-pass",
        "title": "12th Pass Sarkari Naukri 2026–2027 – SSC CHSL, Police Constable, Clerk & Defence | All Sarkari Jobs",
        "desc": "Latest 12th pass government vacancies 2026–2027. Check SSC CHSL, State Police Constable, Army Agniveer, and Clerk jobs with direct apply portals.",
        "keywords": "12th pass govt jobs 2026 2027, 12th pass sarkari vacancy, ssc chsl apply online, up police constable 12th pass, clerk recruitment, defence 12th pass, All Sarkari Jobs",
        "heading": "12th Pass Government Jobs 2026–2027",
        "filter_pill": "10th",
        "search_term": "12th"
    },
    {
        "slug": "graduate",
        "title": "Graduate Govt Jobs 2026–2027 – SSC CGL, UPSC IAS, Bank PO & Sub-Inspector | All Sarkari Jobs",
        "desc": "Find central and state government jobs for graduates 2026–2027. Apply online for SSC CGL, Bank PO, UPSC Civil Services, and State SI vacancies.",
        "keywords": "graduate govt jobs 2026 2027, govt jobs for graduates, ssc cgl recruitment, bank po vacancy, upsc civil services, state sub inspector, All Sarkari Jobs",
        "heading": "Graduate Government Jobs 2026–2027",
        "filter_pill": "graduate",
        "search_term": ""
    },
    {
        "slug": "engineering-iti",
        "title": "Engineering, Diploma & ITI Govt Jobs 2026–2027 – Railway JE, BHEL & Apprentice | All Sarkari Jobs",
        "desc": "Latest government vacancies for B.Tech, Diploma, and ITI pass aspirants. Check Railway JE, BHEL Artisan, PSUs, and Trade Apprentice recruitment notices.",
        "keywords": "engineering govt jobs 2026 2027, iti sarkari naukri, diploma apprentice vacancies, railway je recruitment, bhel artisan online form, psu engineering jobs, All Sarkari Jobs",
        "heading": "Engineering, Diploma & ITI Jobs 2026–2027",
        "filter_pill": "all",
        "search_term": "apprentice"
    },
    {
        "slug": "teaching",
        "title": "Teaching Govt Jobs 2026–2027 – CTET, UPTET, Super TET, KVS & Assistant Teacher | All Sarkari Jobs",
        "desc": "Find active government teacher vacancies 2026–2027. Check CTET, UPTET, Super TET, KVS, NVS, and state assistant teacher recruitment notices and eligibility.",
        "keywords": "teaching govt jobs 2026 2027, teacher recruitment 2026, ctet exam apply online, uptet notification, super tet vacancy, kvs teacher recruitment, All Sarkari Jobs",
        "heading": "Teaching & Education Jobs 2026–2027",
        "filter_pill": "teaching",
        "search_term": ""
    },

    # Major Recruitment Boards
    {
        "slug": "ssc",
        "title": "SSC Recruitment 2026–2027 – SSC CGL, CHSL, GD Constable & MTS Notification | All Sarkari Jobs",
        "desc": "Latest Staff Selection Commission (SSC) job notifications 2026–2027. Download exam calendar, syllabus PDFs, and candidate login links for CGL, CHSL, GD, and MTS.",
        "keywords": "ssc recruitment 2026 2027, ssc cgl apply online, ssc chsl notification, ssc gd constable, ssc mts exam date, ssc syllabus pdf, ssc login, All Sarkari Jobs",
        "heading": "Staff Selection Commission (SSC) 2026–2027",
        "filter_pill": "railway",
        "search_term": "ssc"
    },
    {
        "slug": "railway",
        "title": "Railway RRB Recruitment 2026–2027 – RRB NTPC, ALP, Technician & Group D | All Sarkari Jobs",
        "desc": "Complete list of Railway Recruitment Board (RRB & RRC) vacancies 2026–2027. Download notification PDFs, check exam dates, and apply online.",
        "keywords": "railway rrb recruitment 2026 2027, rrb ntpc apply online, rrb alp vacancy, rrb technician form, railway group d notification, rrb exam city slip, All Sarkari Jobs",
        "heading": "Railway Recruitment Boards (RRB) 2026–2027",
        "filter_pill": "railway",
        "search_term": "rrb"
    },
    {
        "slug": "upsc",
        "title": "UPSC Recruitment 2026–2027 – Civil Services IAS, IFS, NDA, CDS & CMS | All Sarkari Jobs",
        "desc": "Union Public Service Commission (UPSC) recruitment notices 2026–2027. Check IAS exam dates, NDA selection lists, CDS results, and download official notifications.",
        "keywords": "upsc recruitment 2026 2027, upsc civil services ias, upsc nda exam, upsc cds result, upsc otr registration, upsc notification pdf, All Sarkari Jobs",
        "heading": "Union Public Service Commission (UPSC) 2026–2027",
        "filter_pill": "all",
        "search_term": "upsc"
    },
    {
        "slug": "banking",
        "title": "Bank Jobs 2026–2027 – IBPS PO, Clerk, SO, SBI & RBI Bank Recruitment | All Sarkari Jobs",
        "desc": "Latest banking and insurance vacancies 2026–2027. Apply online for IBPS PO, SBI Clerk, RBI Grade B, UIIC, and LIC recruitment notices.",
        "keywords": "bank jobs 2026 2027, ibps po apply online, sbi clerk notification, ibps rrb clerk, rbi grade b recruitment, uiic ao exam, bank sarkari naukri, All Sarkari Jobs",
        "heading": "Banking & Insurance Recruitment 2026–2027",
        "filter_pill": "all",
        "search_term": "bank"
    },
    {
        "slug": "police-defence",
        "title": "Police & Defence Jobs 2026–2027 – State Police Constable, SI, Army & Navy | All Sarkari Jobs",
        "desc": "Find active Police and Defence force vacancies 2026–2027. Check UP Police, Bihar Police, Indian Army Agniveer, Air Force, and Navy recruitment.",
        "keywords": "police jobs 2026 2027, defence recruitment, up police constable form, bihar police si vacancy, indian army agniveer, navy recruitment, All Sarkari Jobs",
        "heading": "Police & Defence Forces 2026–2027",
        "filter_pill": "police",
        "search_term": ""
    },

    # States & Regions
    {
        "slug": "uttar-pradesh",
        "title": "UP Govt Jobs 2026–2027 – Uttar Pradesh Sarkari Naukri, UPSSSC & Police | All Sarkari Jobs",
        "desc": "Find latest UP Govt Jobs 2026–2027. Apply online for UPSSSC, UP Police, UPPSC, and Assistant Teacher vacancies in Uttar Pradesh on All Sarkari Jobs.",
        "keywords": "up govt jobs 2026 2027, uttar pradesh sarkari naukri, upsssc apply online, up police vacancy, uppsc assistant teacher, up jobs direct link, All Sarkari Jobs",
        "heading": "Uttar Pradesh (UP) Govt Jobs 2026–2027",
        "filter_pill": "up",
        "search_term": ""
    },
    {
        "slug": "bihar",
        "title": "Bihar Govt Jobs 2026–2027 – BPSC, BSSC, Bihar Police Vacancy & STET | All Sarkari Jobs",
        "desc": "Latest Bihar Sarkari Naukri 2026–2027. Check active BPSC, BSSC, Bihar Police Constable/SI, and STET teacher vacancies with direct apply links.",
        "keywords": "bihar govt jobs 2026 2027, bihar sarkari naukri, bpsc apply online, bssc vacancy, bihar police constable, bihar stet admit card, All Sarkari Jobs",
        "heading": "Bihar Government Vacancies 2026–2027",
        "filter_pill": "bihar",
        "search_term": ""
    },
    {
        "slug": "telangana",
        "title": "Telangana Govt Jobs 2026–2027 – TSPSC, Police & Forest Department Recruitment | All Sarkari Jobs",
        "desc": "Explore Telangana State government job notifications 2026–2027. Check TSPSC Group 1, 2, 3, 4, Police, and Singareni Collieries vacancies.",
        "keywords": "telangana govt jobs 2026 2027, tspsc apply online, telangana police recruitment, tspsc group vacancy, singareni recruitment, telangana sarkari job, All Sarkari Jobs",
        "heading": "Telangana State Govt Jobs 2026–2027",
        "filter_pill": "all",
        "search_term": "telangana"
    },
    {
        "slug": "central",
        "title": "Central Govt Jobs 2026–2027 – All India Vacancies, MHA, Defence & Railways | All Sarkari Jobs",
        "desc": "Active Central Government job vacancies across India 2026–2027. Check MHA, Intelligence Bureau, Railways, Supreme Court, and Central PSU recruitments.",
        "keywords": "central govt jobs 2026 2027, all india govt vacancies, mha ib recruitment, railway jobs central, supreme court jobs, central sarkari naukri, All Sarkari Jobs",
        "heading": "Central Govt / All India Jobs 2026–2027",
        "filter_pill": "all",
        "search_term": "central"
    },
    {
        "slug": "delhi",
        "title": "Delhi Govt Jobs 2026–2027 – DSSSB, Delhi High Court & DDA Vacancies | All Sarkari Jobs",
        "desc": "Latest government vacancies in Delhi NCR 2026–2027. Apply online for DSSSB TGT/PGT, Delhi Judicial Service, and MCD recruitment.",
        "keywords": "delhi govt jobs 2026 2027, dsssb apply online, delhi high court vacancy, dda recruitment, delhi sarkari naukri, dsssb admit card, All Sarkari Jobs",
        "heading": "Delhi & NCR Vacancies 2026–2027",
        "filter_pill": "all",
        "search_term": "delhi"
    },
    {
        "slug": "rajasthan",
        "title": "Rajasthan & MP Govt Jobs 2026–2027 – RPSC, RSMSSB & MPESB Vacancies | All Sarkari Jobs",
        "desc": "Find government job recruitments in Rajasthan and Madhya Pradesh 2026–2027. Check RPSC, RSMSSB Patwari, and MPESB notifications.",
        "keywords": "rajasthan govt jobs 2026 2027, rpsc apply online, rsmssb patwari vacancy, mpesb admit card, mp police jobs, rajasthan sarkari naukri, All Sarkari Jobs",
        "heading": "Rajasthan & MP Recruitment 2026–2027",
        "filter_pill": "all",
        "search_term": "rajasthan"
    }
]

def generate_programmatic_landing_pages():
    template_path = BASE_DIR / "category.html"
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    generated_count = 0
    clean_urls = []

    for item in LANDING_PAGES:
        slug = item["slug"]
        out_dir = BASE_DIR / "jobs" / slug
        out_dir.mkdir(parents=True, exist_ok=True)
        out_file = out_dir / "index.html"
        clean_url = f"https://www.allsarkarijobs.online/jobs/{slug}"
        clean_urls.append(clean_url)

        page_html = template

        # Replace Title
        page_html = re.sub(r'<title[^>]*>.*?</title>', f'<title id="metaTitle">{item["title"]}</title>', page_html)
        # Replace Meta Description
        page_html = re.sub(r'<meta[^>]*name="description"[^>]*>', f'<meta name="description" id="metaDesc" content="{item["desc"]}">', page_html)
        # Replace Meta Keywords
        page_html = re.sub(r'<meta[^>]*name="keywords"[^>]*>', f'<meta name="keywords" id="metaKeywords" content="{item["keywords"]}">', page_html)
        # Replace Canonical
        page_html = re.sub(r'<link[^>]*rel="canonical"[^>]*>', f'<link rel="canonical" id="canonicalLink" href="{clean_url}">', page_html)
        # Replace OG Tags
        page_html = re.sub(r'<meta[^>]*property="og:title"[^>]*>', f'<meta property="og:title" id="ogTitle" content="{item["title"]}">', page_html)
        page_html = re.sub(r'<meta[^>]*property="og:description"[^>]*>', f'<meta property="og:description" id="ogDesc" content="{item["desc"]}">', page_html)
        page_html = re.sub(r'<meta[^>]*property="og:url"[^>]*>', f'<meta property="og:url" content="{clean_url}">', page_html)

        # Replace H1 heading and breadcrumb text in initial HTML
        page_html = page_html.replace('Loading Category...', item["heading"])
        page_html = page_html.replace('Official government notices, direct links, and verified application portals.', item["desc"])

        # Inject default filter state script right before </head>
        preset_script = f"""
  <script>
    window.INITIAL_PAGE_CONFIG = {{
      category: 'LATEST_JOB',
      filterPill: '{item["filter_pill"]}',
      searchTerm: '{item["search_term"]}',
      pageTitle: {json.dumps(item["title"])},
      pageDesc: {json.dumps(item["desc"])},
      heading: {json.dumps(item["heading"])},
      canonical: '{clean_url}'
    }};
  </script>
</head>"""
        page_html = page_html.replace('</head>', preset_script, 1)

        with open(out_file, "w", encoding="utf-8") as f:
            f.write(page_html)

        generated_count += 1

    print(f"Generated {generated_count} pre-rendered programmatic SEO landing pages in jobs/*/")
    return clean_urls

if __name__ == "__main__":
    generate_programmatic_landing_pages()
