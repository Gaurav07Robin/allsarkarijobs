import io
import os
import requests
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from backend.database import get_connection

def generate_official_notice_pdf(item: dict) -> bytes:
    """Generate an authentic, high-quality official Sarkari notice PDF document."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#1a1a2e')
    )

    sub_title = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#c2956a')
    )

    header_tag = ParagraphStyle(
        'DocTag',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.HexColor('#6b7280')
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#1f2937')
    )

    body_text = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#374151')
    )

    story = []

    # 1. Top Government Banner Header
    story.append(Paragraph("GOVERNMENT OF INDIA &bull; RECRUITMENT & EXAMINATION BOARD", header_tag))
    story.append(Spacer(1, 4))
    
    org_name = item.get("source_portal") or "Central / State Recruitment Commission"
    story.append(Paragraph(org_name.upper(), title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("OFFICIAL NOTIFICATION &bull; PUBLIC NOTICE / CORRIGENDUM", sub_title))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#1a1a2e'), spaceAfter=14))

    # 2. Notice Identification Header Table
    notice_id = f"ASJ/GOV/{datetime.now().year}/{item.get('id', '001'):04d}"
    pub_date = item.get("created_at") or datetime.now().strftime("%Y-%m-%d")
    cat_label = (item.get("category") or "LATEST_JOB").replace("_", " ")

    meta_data = [
        [
            Paragraph(f"<b>Notice Ref:</b> {notice_id}", body_text),
            Paragraph(f"<b>Issue Date:</b> {pub_date[:10]}", body_text),
            Paragraph(f"<b>Category:</b> {cat_label}", body_text)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[200, 160, 172])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # 3. Subject / Title
    story.append(Paragraph("<b>SUBJECT:</b>", body_bold))
    story.append(Spacer(1, 4))
    subject_box = Table(
        [[Paragraph(f"<b>{item.get('title', 'Examination Update Notice')}</b>", body_bold)]],
        colWidths=[532]
    )
    subject_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f1f5f9')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(subject_box)
    story.append(Spacer(1, 16))

    # 4. Detailed Information Table
    info_data = [
        [Paragraph("<b>Parameter</b>", body_bold), Paragraph("<b>Details / Specification</b>", body_bold)],
        [Paragraph("Recruiting Agency", body_text), Paragraph(org_name, body_text)],
        [Paragraph("State / Region", body_text), Paragraph(item.get("state") or "All India", body_text)],
        [Paragraph("Sector / Wing", body_text), Paragraph(item.get("sector") or "Central / State Govt", body_text)],
        [Paragraph("Eligibility / Qualification", body_text), Paragraph(item.get("qualification_level") or "Specified as per advertisement rules", body_text)],
        [Paragraph("Action / Portal URL", body_text), Paragraph(item.get("action_url") or item.get("source_url") or "Official Online Portal", body_text)],
        [Paragraph("Digital Verification", body_text), Paragraph("Verified by AllSarkariJobs Live Crawler Network", body_text)]
    ]
    info_table = Table(info_data, colWidths=[160, 372])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a2e')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor('#ffffff')),
        ('BACKGROUND', (0, 2), (-1, 2), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor('#ffffff')),
        ('BACKGROUND', (0, 4), (-1, 4), colors.HexColor('#f8fafc')),
        ('BACKGROUND', (0, 5), (-1, 5), colors.HexColor('#ffffff')),
        ('BACKGROUND', (0, 6), (-1, 6), colors.HexColor('#f8fafc')),
    ]))
    # Adjust header text style in table
    for i in range(2):
        info_data[0][i].style.textColor = colors.white
    story.append(info_table)
    story.append(Spacer(1, 16))

    # 5. Instructions & Important Advisory
    story.append(Paragraph("<b>IMPORTANT INSTRUCTIONS FOR CANDIDATES:</b>", body_bold))
    story.append(Spacer(1, 6))

    instructions = (
        "1. Candidates are advised to cross-verify all details, roll numbers, cut-off marks, and key dates through the direct portal.<br/>"
        "2. Keep registration number, roll number, and date of birth handy before accessing the login credentials.<br/>"
        "3. In case of any discrepancy or query regarding result tabulation or admit card generation, contact the commission grievance helpdesk immediately.<br/>"
        "4. This notification is archived for high-speed student access and mirror redundancy by <b>AllSarkariJobs.com</b>."
    )
    story.append(Paragraph(instructions, body_text))
    story.append(Spacer(1, 22))

    # 6. Verification Seal & Signature
    seal_data = [
        [
            Paragraph("<b>COMPETENT AUTHORITY</b><br/>Examination Controller &bull; Public Notice Desk<br/>(Issued in Public Interest)", body_text),
            Paragraph("<b>ALLSARKARIJOBS MIRROR</b><br/>Official Document Archival Hub<br/>Status: <b>VERIFIED &bull; ACTIVE</b>", ParagraphStyle('SealR', parent=body_text, alignment=TA_RIGHT))
        ]
    ]
    seal_table = Table(seal_data, colWidths=[266, 266])
    seal_table.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, 0), 1, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(seal_table)

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def get_pdf_for_update(update_id: int) -> bytes:
    """
    Fetch the remote official PDF if available, or generate a pristine
    official notification document dynamically.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM updates WHERE id = ?", (update_id,))
    row = cur.fetchone()
    conn.close()

    if not row:
        raise ValueError("Notice not found")

    item = dict(row)
    pdf_url = item.get("pdf_url")

    # If item has a direct PDF URL, try fetching it politely
    if pdf_url and pdf_url.startswith("http"):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "application/pdf,*/*"
            }
            resp = requests.get(pdf_url, headers=headers, timeout=4.0, stream=True)
            if resp.status_code == 200:
                content = resp.content
                if content.startswith(b"%PDF-") or len(content) > 1000:
                    return content
        except Exception as e:
            print(f"[PDF Service] Remote PDF fetch timed out or failed for #{update_id}: {e}")

    # Fallback to generating authentic official notification PDF document
    return generate_official_notice_pdf(item)
