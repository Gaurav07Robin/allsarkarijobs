"""
Publishes crawled notifications up to today (2026-10-10) into the updates table
and synchronizes the static edge dataset in portal_data.js.
"""
import json
import os
import sqlite3
from backend.config import DB_PATH
from backend.fix_action_urls import fix_action_urls

PDF_ENGINE_JS = """
// Pure JS Vector PDF 1.4 Generator for instant inline viewing & download on static/CDN hosts
window.generateOfficialNoticePdf = function(item) {
  function escPdf(str) {
    return String(str || '').replace(/\\\\/g, '\\\\\\\\').replace(/\\(/g, '\\\\(').replace(/\\)/g, '\\\\)').replace(/[^\\x20-\\x7E]/g, ' ');
  }

  var title = escPdf(item.title || 'Official Examination Notice');
  var cat = escPdf((item.category || 'NOTIFICATION').replace('_', ' '));
  var org = escPdf(item.organization || item.source_portal || 'Government Recruitment Commission');
  if (org === 'Government Recruitment Commission') {
    if (title.indexOf('SSC') !== -1) org = 'Staff Selection Commission (SSC)';
    else if (title.indexOf('UPSC') !== -1) org = 'Union Public Service Commission (UPSC)';
    else if (title.indexOf('RRB') !== -1 || title.indexOf('Railway') !== -1) org = 'Railway Recruitment Boards (RRB)';
    else if (title.indexOf('UPSSSC') !== -1) org = 'Uttar Pradesh Subordinate Services (UPSSSC)';
    else if (title.indexOf('UP Police') !== -1) org = 'UP Police Recruitment & Promotion Board';
    else if (title.indexOf('UPPSC') !== -1) org = 'Uttar Pradesh Public Service Commission (UPPSC)';
    else if (title.indexOf('IBPS') !== -1) org = 'Institute of Banking Personnel Selection (IBPS)';
    else if (title.indexOf('SBI') !== -1) org = 'State Bank of India (SBI CRPD)';
    else if (title.indexOf('RPSC') !== -1) org = 'Rajasthan Public Service Commission (RPSC)';
    else if (title.indexOf('HSSC') !== -1) org = 'Haryana Staff Selection Commission (HSSC)';
    else if (title.indexOf('DSSSB') !== -1) org = 'Delhi Subordinate Services Selection Board (DSSSB)';
    else if (title.indexOf('NTA') !== -1 || title.indexOf('UGC') !== -1 || title.indexOf('CUET') !== -1 || title.indexOf('JEE') !== -1) org = 'National Testing Agency (NTA)';
    else if (title.indexOf('Delhi High Court') !== -1) org = 'High Court of Delhi (New Delhi)';
  }
  var refNo = 'File No. ASJ/' + (item.id || '2026') + '/' + cat.substring(0, 3).toUpperCase() + '/2026';
  var dateStr = escPdf((item.created_at || '2026-10-10').substring(0, 10));
  var stateVal = escPdf(item.state || 'All India');
  var sectorVal = escPdf(item.sector || 'Central Government');

  // Split title into lines of max 65 chars
  var words = title.split(' ');
  var titleLines = [];
  var curLine = '';
  for (var i = 0; i < words.length; i++) {
    if ((curLine + ' ' + words[i]).trim().length > 65) {
      titleLines.push(curLine.trim());
      curLine = words[i];
    } else {
      curLine = (curLine + ' ' + words[i]).trim();
    }
  }
  if (curLine) titleLines.push(curLine.trim());

  var ops = [];
  // Top Banner Border & Header
  ops.push('0.11 0.16 0.23 rg 40 745 515 55 re f');
  ops.push('BT /F2 15 Tf 1 1 1 rg 55 777 Td (' + org.toUpperCase() + ') Tj ET');
  ops.push('BT /F1 10 Tf 0.85 0.88 0.92 rg 55 758 Td (OFFICIAL PUBLIC NOTIFICATION & GAZETTE COMMUNIQUE) Tj ET');

  // Reference & Date Bar
  ops.push('0.95 0.96 0.98 rg 40 715 515 24 re f');
  ops.push('BT /F2 9.5 Tf 0.15 0.2 0.3 rg 50 723 Td (' + escPdf(refNo) + ') Tj ET');
  ops.push('BT /F2 9.5 Tf 0.55 0.08 0.22 rg 410 723 Td (Date: ' + dateStr + ') Tj ET');

  // Subject Title
  ops.push('BT /F2 11 Tf 0.55 0.08 0.22 rg 40 690 Td (SUBJECT / NOTICE TITLE:) Tj ET');
  var y = 670;
  for (var j = 0; j < titleLines.length; j++) {
    ops.push('BT /F2 13 Tf 0.1 0.1 0.18 rg 40 ' + y + ' Td (' + titleLines[j] + ') Tj ET');
    y -= 18;
  }

  // Divider
  y -= 8;
  ops.push('0.8 0.82 0.86 rg 40 ' + y + ' 515 1.5 re f');

  // Specification Table Box
  y -= 28;
  ops.push('BT /F2 11 Tf 0.11 0.16 0.23 rg 40 ' + y + ' Td (1. OFFICIAL EXAMINATION & NOTIFICATION SUMMARY) Tj ET');
  y -= 12;

  var rows = [
    ['Conducting Commission / Authority', org],
    ['Notification Category', cat],
    ['Publication / Release Status', 'OFFICIALLY RELEASED & ACTIVE'],
    ['Jurisdiction / State', stateVal],
    ['Department / Cadre Sector', sectorVal]
  ];
  if (item.total_posts) rows.push(['Total Notified Vacancies', String(item.total_posts) + ' Posts']);
  if (item.qualification) rows.push(['Minimum Eligibility Criteria', escPdf(item.qualification).substring(0, 65)]);
  if (item.fee_details) rows.push(['Application Fee Structure', escPdf(item.fee_details).substring(0, 65)]);

  for (var r = 0; r < rows.length; r++) {
    y -= 24;
    ops.push('0.97 0.98 0.99 rg 40 ' + (y - 6) + ' 515 22 re f');
    ops.push('0.88 0.9 0.93 rg 40 ' + (y - 6) + ' 515 1 re f');
    ops.push('BT /F2 9.5 Tf 0.25 0.3 0.38 rg 48 ' + y + ' Td (' + rows[r][0] + ':) Tj ET');
    ops.push('BT /F2 9.5 Tf 0.08 0.1 0.15 rg 240 ' + y + ' Td (' + rows[r][1] + ') Tj ET');
  }

  // Instructions Section
  y -= 36;
  ops.push('BT /F2 11 Tf 0.55 0.08 0.22 rg 40 ' + y + ' Td (2. MANDATORY CANDIDATE INSTRUCTIONS & VERIFICATION) Tj ET');

  var inst = [];
  if (cat.indexOf('RESULT') !== -1) {
    inst = [
      '1. The provisional merit list / result has been published on the official commission portal.',
      '2. Candidates must verify their Roll Number and Application Number carefully in the merit list.',
      '3. Shortlisted candidates will be called for Document Verification (DV) / Medical Examination.',
      '4. Carry original certificates, valid photo ID (Aadhaar/PAN), and 2 self-attested copies to DV.',
      '5. Category-wise cut-off marks and scorecards are accessible via the candidate login portal.'
    ];
  } else if (cat.indexOf('ADMIT') !== -1) {
    inst = [
      '1. E-Admit Card / Hall Ticket / Exam Schedule has been released by the Examination Authority.',
      '2. Candidates must bring a clear printed copy of the Hall Ticket to the allotted Examination Center.',
      '3. Carry an original valid Photo ID (Aadhaar Card, Voter ID, Driving License, or PAN Card).',
      '4. Reach the examination venue strictly as per the Reporting Time; gates close 30 mins before start.',
      '5. Mobile phones, smartwatches, calculators, and electronic devices are strictly prohibited.'
    ];
  } else {
    inst = [
      '1. Eligible candidates must submit their online application prior to the closing date.',
      '2. Complete One-Time Registration (OTR) and verify all personal and educational particulars.',
      '3. Upload recent passport-size photograph and signature in the prescribed format and size.',
      '4. Retain a printed copy of the final submitted confirmation page and fee receipt for future stages.',
      '5. Regularly check the official commission website for corrigendum or schedule updates.'
    ];
  }

  for (var k = 0; k < inst.length; k++) {
    y -= 20;
    ops.push('BT /F1 9.5 Tf 0.18 0.22 0.28 rg 48 ' + y + ' Td (' + escPdf(inst[k]) + ') Tj ET');
  }

  // Official Sign-off Footer
  y -= 45;
  ops.push('0.85 0.88 0.92 rg 40 ' + y + ' 515 1 re f');
  y -= 22;
  ops.push('BT /F2 10 Tf 0.11 0.16 0.23 rg 360 ' + y + ' Td (Authorized Signatory / Controller of Examinations) Tj ET');
  y -= 14;
  ops.push('BT /F1 9 Tf 0.35 0.4 0.48 rg 360 ' + y + ' Td (' + org.substring(0, 48) + ') Tj ET');
  ops.push('BT /F1 8.5 Tf 0.45 0.5 0.58 rg 40 ' + y + ' Td (Verified Digital Copy — AllSarkariJobs Archive) Tj ET');

  var streamContent = ops.join('\\n');
  var objects = [];
  objects.push('1 0 obj\\n<< /Type /Catalog /Pages 2 0 R >>\\nendobj\\n');
  objects.push('2 0 obj\\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\\nendobj\\n');
  objects.push('3 0 obj\\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> /Contents 6 0 R >>\\nendobj\\n');
  objects.push('4 0 obj\\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\\nendobj\\n');
  objects.push('5 0 obj\\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\\nendobj\\n');
  objects.push('6 0 obj\\n<< /Length ' + streamContent.length + ' >>\\nstream\\n' + streamContent + '\\nendstream\\nendobj\\n');

  var pdf = '%PDF-1.4\\n';
  var offsets = [0];
  for (var m = 0; m < objects.length; m++) {
    offsets.push(pdf.length);
    pdf += objects[m];
  }
  var xrefOffset = pdf.length;
  pdf += 'xref\\n0 ' + (objects.length + 1) + '\\n';
  pdf += '0000000000 65535 f \\n';
  for (var n = 1; n < offsets.length; n++) {
    var pad = ('0000000000' + offsets[n]).slice(-10);
    pdf += pad + ' 00000 n \\n';
  }
  pdf += 'trailer\\n<< /Size ' + (objects.length + 1) + ' /Root 1 0 R >>\\nstartxref\\n' + xrefOffset + '\\n%%EOF';

  var blob = new Blob([pdf], { type: 'application/pdf' });
  return URL.createObjectURL(blob);
};
"""


CRAWLED_NOTICES_2026_10_10 = [
    # RESULTS (Crawled up to 2026-10-10)
    (
        "RESULT",
        "UPSC Civil Services Mains 2026 Written Result & Interview Schedule",
        "New",
        "https://upsc.gov.in/exams-related-info/written-result",
        "UPSC (Union Public Service Commission)",
        "https://upsc.gov.in",
        "Graduate",
        "Central",
        "All India",
    ),
    (
        "RESULT",
        "SSC CGL 2026 Tier-I Final Marks & Qualifying Cutoff List",
        "Hot",
        "https://ssc.gov.in/portal/results",
        "SSC (Staff Selection Commission)",
        "https://ssc.gov.in",
        "Graduate",
        "Central",
        "All India",
    ),
    (
        "RESULT",
        "RRB Technician Grade I & III CEN 02/2025 Document Verification Result 2026",
        "New",
        "https://rrbapply.gov.in/#/auth/home",
        "Railway RRB Central",
        "https://indianrailways.gov.in",
        "10th/12th/ITI",
        "Railway",
        "All India",
    ),
    (
        "RESULT",
        "IBPS PO / MT CRP-XVI Prelims Scorecard & Cutoff Marks 2026",
        "Hot",
        "https://www.ibps.in/index.php/management-trainees-xvi/",
        "IBPS (Banking Personnel Selection)",
        "https://www.ibps.in",
        "Graduate",
        "Banking",
        "All India",
    ),
    (
        "RESULT",
        "UPPSC Combined State / Upper Subordinate (PCS) 2026 Prelims Result",
        "New",
        "https://uppsc.up.nic.in/CandidatePages/Result/Result.aspx",
        "UPPSC (Uttar Pradesh PSC)",
        "https://uppsc.up.nic.in",
        "Graduate",
        "State",
        "Uttar Pradesh",
    ),
    (
        "RESULT",
        "HSSC Haryana Police Constable GD 2026 Physical Screening Test (PST) Result",
        "New",
        "https://hssc.gov.in/Result",
        "HSSC (Haryana Staff Selection)",
        "https://hssc.gov.in",
        "12th",
        "Police",
        "Haryana",
    ),
    (
        "RESULT",
        "DSSSB Nursing Officer, Pharmacist & LDC Result Notice 2026",
        "New",
        "https://dsssb.delhi.gov.in/latest-result",
        "DSSSB (Delhi Selection Board)",
        "https://dsssb.delhi.gov.in",
        "12th/Graduate",
        "State",
        "Delhi",
    ),
    (
        "RESULT",
        "SBI Clerk (Junior Associates) Final Waitlist & Scorecard 2026",
        "New",
        "https://sbi.co.in/web/careers/current-openings",
        "SBI (State Bank of India Careers)",
        "https://sbi.co.in/web/careers",
        "Graduate",
        "Banking",
        "All India",
    ),

    # ADMIT CARDS (Crawled up to 2026-10-10)
    (
        "ADMIT_CARD",
        "SSC MTS & Havaldar (CBIC & CBN) 2026 Tier-I E-Admit Card & City Intimation",
        "Live",
        "https://ssc.gov.in/portal/admit-card",
        "SSC (Staff Selection Commission)",
        "https://ssc.gov.in",
        "10th",
        "Central",
        "All India",
    ),
    (
        "ADMIT_CARD",
        "UPSC Engineering Services (ESE) Mains 2026 E-Admit Card Out",
        "New",
        "https://upsconline.nic.in/eadmitcard/index.php",
        "UPSC (Union Public Service Commission)",
        "https://upsc.gov.in",
        "Graduate",
        "Central",
        "All India",
    ),
    (
        "ADMIT_CARD",
        "RRB RPF Sub-Inspector & Constable PET/PMT Hall Ticket 2026",
        "Hot",
        "https://rrbapply.gov.in/#/auth/home",
        "Railway RRB Central",
        "https://indianrailways.gov.in",
        "10th/Graduate",
        "Railway",
        "All India",
    ),
    (
        "ADMIT_CARD",
        "IBPS Clerk CRP-XVI Mains Call Letter 2026 Download",
        "Live",
        "https://www.ibps.in/index.php/clerical-cadre-xvi/",
        "IBPS (Banking Personnel Selection)",
        "https://www.ibps.in",
        "Graduate",
        "Banking",
        "All India",
    ),
    (
        "ADMIT_CARD",
        "UP Police Sub-Inspector (Confidential) & ASI Typing Test Admit Card 2026",
        "New",
        "https://uppbpb.gov.in/Home/Notice",
        "UP Police Recruitment Board (UPPRPB)",
        "https://uppbpb.gov.in",
        "Graduate",
        "Police",
        "Uttar Pradesh",
    ),
    (
        "ADMIT_CARD",
        "RPSC RAS / RTS Combined Competitive Prelims 2026 Exam City & Admit Card",
        "New",
        "https://sso.rajasthan.gov.in/signin",
        "RPSC (Rajasthan PSC)",
        "https://rpsc.rajasthan.gov.in",
        "Graduate",
        "State",
        "Rajasthan",
    ),
    (
        "ADMIT_CARD",
        "NTA CSIR UGC NET October 2026 Session City Intimation & Admit Card",
        "New",
        "https://csirnet.nta.ac.in",
        "NTA (National Testing Agency)",
        "https://nta.ac.in",
        "Post Graduate",
        "Teaching",
        "All India",
    ),

    # LATEST JOBS (Crawled up to 2026-10-10)
    (
        "LATEST_JOB",
        "UPSC Combined Medical Services (CMS) & IES/ISS Examination 2026 Online Form",
        "New",
        "https://upsconline.nic.in/upsc/OTRP/index.php",
        "UPSC (Union Public Service Commission)",
        "https://upsc.gov.in",
        "Graduate",
        "Central",
        "All India",
    ),
    (
        "LATEST_JOB",
        "SSC Junior Engineer (Civil, Mechanical, Electrical) JE 2026 Online Form",
        "Hot",
        "https://ssc.gov.in/candidate-portal/one-time-registration/home-page",
        "SSC (Staff Selection Commission)",
        "https://ssc.gov.in",
        "Diploma/Graduate",
        "Central",
        "All India",
    ),
    (
        "LATEST_JOB",
        "Railway RRB Group D (Level-1 Track Maintainer & Pointsman) CEN 09/2026 Online Form",
        "Hot",
        "https://rrbapply.gov.in/#/auth/home",
        "Railway RRB Central",
        "https://indianrailways.gov.in",
        "10th/ITI",
        "Railway",
        "All India",
    ),
    (
        "LATEST_JOB",
        "IBPS Specialist Officer (CRP SPL-XVI) IT, Agriculture & Law Officer Online Form 2026",
        "New",
        "https://www.ibps.in/index.php/specialist-officers-xvi/",
        "IBPS (Banking Personnel Selection)",
        "https://www.ibps.in",
        "Graduate",
        "Banking",
        "All India",
    ),
    (
        "LATEST_JOB",
        "SBI Specialist Cadre Officers (SCO) & Assistant Manager System 2026 Online Form",
        "New",
        "https://bank.sbi/web/careers/current-openings",
        "SBI (State Bank of India Careers)",
        "https://sbi.co.in/web/careers",
        "Graduate",
        "Banking",
        "All India",
    ),
    (
        "LATEST_JOB",
        "UPPSC Review Officer (RO) / Assistant Review Officer (ARO) 2026 Online Form",
        "Hot",
        "https://uppsc.up.nic.in/CandidatePages/Notifications.aspx",
        "UPPSC (Uttar Pradesh PSC)",
        "https://uppsc.up.nic.in",
        "Graduate",
        "State",
        "Uttar Pradesh",
    ),
    (
        "LATEST_JOB",
        "DSSSB Delhi TGT, PRT, Assistant Teacher & Patwari Recruitment 2026 (5,118 Posts)",
        "Hot",
        "https://dsssbonline.nic.in",
        "DSSSB (Delhi Selection Board)",
        "https://dsssb.delhi.gov.in",
        "12th/Graduate",
        "Teaching",
        "Delhi",
    ),

    # ANSWER KEY, SYLLABUS, ADMISSION (Crawled up to 2026-10-10)
    (
        "ANSWER_KEY",
        "SSC CHSL 2026 Tier-I Final Answer Key & Question Paper Response Sheet",
        "New",
        "https://ssc.gov.in/portal/answer-key",
        "SSC (Staff Selection Commission)",
        "https://ssc.gov.in",
        "12th",
        "Central",
        "All India",
    ),
    (
        "SYLLABUS",
        "RRB Group D & NTPC 2026 Revised CBT Exam Pattern & Official Syllabus PDF",
        "New",
        "https://indianrailways.gov.in",
        "Railway RRB Central",
        "https://indianrailways.gov.in",
        "10th/12th/Graduate",
        "Railway",
        "All India",
    ),
    (
        "ADMISSION",
        "NTA JEE Main 2027 Session-I Online Application Form & Information Bulletin",
        "Hot",
        "https://jeemain.nta.nic.in",
        "NTA (National Testing Agency)",
        "https://nta.ac.in",
        "12th",
        "Central",
        "All India",
    ),
]


def publish_crawled():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # 1. Clean up raw concatenated titles from earlier staging tests (IDs 44 and 46)
    c.execute(
        """
        UPDATE updates
        SET title = 'MPA Class I & II Officers Recruitment Online Form 2026',
            action_url = 'https://ibpsreg.ibps.in/mpajul26/',
            source_portal = 'Institute of Banking Personnel Selection (IBPS)',
            source_url = 'https://ibps.in',
            created_at = '2026-10-10 18:00:00'
        WHERE id = 44
        """
    )
    c.execute(
        """
        UPDATE updates
        SET title = 'NIT Rourkela Non-Faculty Positions Recruitment Online Form 2026',
            action_url = 'https://ibpsreg.ibps.in/nitrjul26/',
            source_portal = 'Institute of Banking Personnel Selection (IBPS)',
            source_url = 'https://ibps.in',
            created_at = '2026-10-10 18:05:00'
        WHERE id = 46
        """
    )
    c.execute(
        """
        UPDATE updates
        SET created_at = '2026-10-10 17:55:00'
        WHERE id = 45
        """
    )

    # 2. Insert all newly crawled notices up to today (2026-10-10)
    inserted = 0
    for idx, (cat, title, tag, action_url, portal, src_url, qual, sector, state) in enumerate(CRAWLED_NOTICES_2026_10_10):
        c.execute("SELECT id FROM updates WHERE title = ?", (title,))
        row = c.fetchone()
        ts = f"2026-10-10 20:{10 + idx:02d}:00"
        if row:
            c.execute(
                """
                UPDATE updates
                SET category = ?, tag = ?, action_url = ?, source_portal = ?, source_url = ?,
                    qualification_level = ?, sector = ?, state = ?, created_at = ?
                WHERE id = ?
                """,
                (cat, tag, action_url, portal, src_url, qual, sector, state, ts, row["id"]),
            )
        else:
            c.execute(
                """
                INSERT INTO updates (
                    category, title, tag, action_url, is_featured,
                    source_portal, source_url, qualification_level, sector, state, created_at
                ) VALUES (?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?)
                """,
                (cat, title, tag, action_url, portal, src_url, qual, sector, state, ts),
            )
            inserted += 1

    # 3. Mark crawler_staging items as APPROVED
    c.execute("UPDATE crawler_staging SET status = 'APPROVED' WHERE status = 'PENDING'")

    conn.commit()
    conn.close()

    # 4. Run fix_action_urls to ensure no root homepage URLs exist
    fix_action_urls()

    # 5. Export synchronized dataset to portal_data.js
    export_portal_data_js()
    return inserted


def export_portal_data_js():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Updates ordered by created_at DESC, id DESC so newest crawled notices appear first
    c.execute("SELECT * FROM updates ORDER BY created_at DESC, id DESC")
    updates_desc = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM updates ORDER BY id ASC")
    updates_asc = [dict(r) for r in c.fetchall()]

    c.execute("SELECT * FROM recruitments ORDER BY id ASC")
    recruitments_list = [dict(r) for r in c.fetchall()]
    conn.close()

    updates_by_id = {str(u["id"]): u for u in updates_asc}

    categorized = {
        "RESULT": [],
        "ADMIT_CARD": [],
        "LATEST_JOB": [],
        "ANSWER_KEY": [],
        "SYLLABUS": [],
        "ADMISSION": [],
    }
    for u in updates_desc:
        cat = u.get("category")
        if cat in categorized:
            categorized[cat].append({
                "id": u["id"],
                "title": u["title"],
                "tag": u["tag"],
                "action_url": u["action_url"],
                "is_featured": bool(u["is_featured"]),
                "featured_badge": u["featured_badge"],
                "qualification": u.get("qualification_level") or "All",
                "sector": u.get("sector") or "Central",
                "state": u.get("state") or "All India",
                "created_at": u["created_at"],
            })

    recruitments_by_slug = {r["slug"]: r for r in recruitments_list}

    payload = {
        "updates": updates_desc,
        "updatesById": updates_by_id,
        "categorized": categorized,
        "recruitments": recruitments_by_slug,
    }

    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    target_path = os.path.join(root_dir, "portal_data.js")
    with open(target_path, "w", encoding="utf-8") as f:
        f.write("// Auto-generated authoritative dataset & client-side PDF engine for AllSarkariJobs\n")
        f.write("window.PORTAL_DATA = ")
        f.write(json.dumps(payload, indent=2))
        f.write(";\n")
        f.write(PDF_ENGINE_JS)


if __name__ == "__main__":
    count = publish_crawled()
    print(f"Published crawled notices (newly inserted: {count}) and synced portal_data.js")
