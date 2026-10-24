#!/usr/bin/env python3
"""
build_core_pdf_whitepapers.py
=============================
Generates 3 authoritative, publication-grade engineering PDF whitepapers for ADI Communications
and Lead Engineer Gary Pearce (07860 244 274) using ReportLab.

Documents:
1. 2026-uk-domestic-cctv-legal-compliance-checklist.pdf
2. hotel-hmo-anti-theft-tv-wall-mounting-specification.pdf
3. starlink-90mph-pennine-gale-mounting-engineering-guide.pdf

Author: Gary Pearce / ADI Communications
Direct Engineer: 07860 244 274 | info@adicommunications.co.uk
"""

import os
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether, PageBreak
)
from reportlab.pdfgen import canvas

# Output directories
REPO_ROOT = Path(__file__).resolve().parent
PDF_DIRS = [
    REPO_ROOT / "assets" / "pdfs",
    Path(r"C:\Users\Gary\.gemini\antigravity\scratch\adi-communications-rebuild\assets\pdfs"),
    Path(r"C:\Users\Gary\.gemini\antigravity\scratch\adi-communications-rebuild\dist\assets\pdfs"),
]

for d in PDF_DIRS:
    d.mkdir(parents=True, exist_ok=True)

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas for dynamic total page numbering and authoritative footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))

        # Header rule & title (pages > 1)
        if self._pageNumber > 1:
            self.setStrokeColor(colors.HexColor("#E2E8F0"))
            self.setLineWidth(0.5)
            self.line(40, A4[1] - 35, A4[0] - 40, A4[1] - 35)
            self.drawString(40, A4[1] - 30, "ADI Communications | Physical Engineering & Security Technical Specification")
            self.drawRightString(A4[0] - 40, A4[1] - 30, "Lead Engineer: 07860 244 274")

        # Footer rule & details
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.5)
        self.line(40, 45, A4[0] - 40, 45)

        footer_text = (
            "ADI Communications • Gary Pearce (25+ Yrs Hands-On Field Experience) • "
            "£10M Public Liability • Direct: 07860 244 274"
        )
        self.drawString(40, 32, footer_text)
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(A4[0] - 40, 32, page_str)
        self.restoreState()

def build_pdf_document(filename: str, title: str, subtitle: str, doc_id: str, sections: list):
    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )

    sub_style = ParagraphStyle(
        'DocSub',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#475569'),
        spaceAfter=12
    )

    meta_badge_style = ParagraphStyle(
        'MetaBadge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#FF5500')
    )

    h2_style = ParagraphStyle(
        'DocH2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'DocBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=6
    )

    callout_style = ParagraphStyle(
        'DocCallout',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor('#1E293B')
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=colors.white
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        textColor=colors.HexColor('#1E293B')
    )

    story = []

    # Document Header Box
    header_data = [
        [
            Paragraph(f"<b>DOCUMENT ID:</b> {doc_id} &nbsp;|&nbsp; <b>REVISION:</b> 2026.1 &nbsp;|&nbsp; <b>CLASSIFICATION:</b> TRADE TECHNICAL SPECIFICATION", meta_badge_style),
            Paragraph("<b>STATUS:</b> VERIFIED ACTIVE", meta_badge_style)
        ]
    ]
    header_table = Table(header_data, colWidths=[380, 135])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFF7ED')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#FFEDD5')),
        ('PADDING', (0,0), (-1,-1), 6),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # Main Title
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(subtitle, sub_style))

    # Author Credentials Banner
    cred_data = [
        [
            Paragraph("<b>Author / Lead Engineer:</b> Gary Pearce (ADI Communications)<br/>"
                      "<b>Direct Field Contact:</b> 07860 244 274 &nbsp;|&nbsp; info@adicommunications.co.uk<br/>"
                      "<b>Web Asset:</b> https://adicommunications.co.uk &nbsp;|&nbsp; Shield: https://tvandhomesecurity.blogspot.com", body_style),
            Paragraph("<b>Professional Accreditation & Coverage:</b><br/>"
                      "• 25+ Years Hands-On Physical Security & Telecoms<br/>"
                      "• £10,000,000 Public Liability Insurance Coverage<br/>"
                      "• NVQ Level 1-4 Data Cabling, Fibre & Electrical<br/>"
                      "• 9.98 / 10 Rated Across 84+ Verified Client Reviews", body_style)
        ]
    ]
    cred_table = Table(cred_data, colWidths=[270, 245])
    cred_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F8FAFC')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
        ('PADDING', (0,0), (-1,-1), 8),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(cred_table)
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceBefore=2, spaceAfter=8))

    # Render Sections
    for sec in sections:
        sec_title = sec.get('title')
        sec_paras = sec.get('paragraphs', [])
        sec_table = sec.get('table', None)
        sec_callout = sec.get('callout', None)

        if sec_title:
            story.append(Paragraph(sec_title, h2_style))

        for p in sec_paras:
            story.append(Paragraph(p, body_style))

        if sec_table:
            # Format table with headers
            t_data = []
            for r_idx, row in enumerate(sec_table):
                t_row = []
                for cell in row:
                    if r_idx == 0:
                        t_row.append(Paragraph(cell, table_header_style))
                    else:
                        t_row.append(Paragraph(cell, table_cell_style))
                t_data.append(t_row)

            # Auto calculate colWidths
            col_count = len(sec_table[0])
            col_width = 515 / col_count
            tbl = Table(t_data, colWidths=[col_width]*col_count)
            tbl.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1E293B')),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E1')),
                ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor('#F8FAFC')]),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            story.append(Spacer(1, 4))
            story.append(tbl)
            story.append(Spacer(1, 6))

        if sec_callout:
            callout_box = Table([[Paragraph(f"<b>CRITICAL TRADE PROTOCOL:</b> {sec_callout}", callout_style)]], colWidths=[515])
            callout_box.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EFF6FF')),
                ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#93C5FD')),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            story.append(Spacer(1, 4))
            story.append(callout_box)
            story.append(Spacer(1, 6))

    # Final Sign-off block
    signoff = [
        [
            Paragraph("<b>FIELD VERIFICATION & ASSURANCE:</b><br/>"
                      "All physical works executed strictly to UK Building Regulations (Part B Fire Safety, Part P Electrical), "
                      "BS 7671 standards, and double-screened CAI-benchmarked cabling. CAI membership is not claimed. "
                      "Direct engineering queries or site audit booking: <b>07860 244 274</b>.", body_style)
        ]
    ]
    signoff_table = Table(signoff, colWidths=[515])
    signoff_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F1F5F9')),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor('#94A3B8')),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(Spacer(1, 8))
    story.append(signoff_table)

    # Build to primary path, then copy to other directories
    primary_dir = PDF_DIRS[0]
    primary_path = primary_dir / filename
    doc = SimpleDocTemplate(
        str(primary_path),
        pagesize=A4,
        leftMargin=40,
        rightMargin=40,
        topMargin=45,
        bottomMargin=50
    )
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"  [SAVED PRIMARY] {primary_path} ({primary_path.stat().st_size / 1024:.1f} KB)")

    import shutil
    for d in PDF_DIRS[1:]:
        target_path = d / filename
        shutil.copy2(primary_path, target_path)
        print(f"  [COPIED] {target_path} ({target_path.stat().st_size / 1024:.1f} KB)")

def generate_whitepaper_1():
    print("\n--- Generating Whitepaper 1: CCTV Legal Compliance ---")
    sections = [
        {
            "title": "1. UK Surveillance Camera Code of Practice & Boundary Compliance",
            "paragraphs": [
                "Under UK General Data Protection Regulation (UK GDPR) and the Data Protection Act 2018, domestic CCTV systems whose field of view extends beyond the property boundary into public footpaths, highways, or neighbouring curtilages fall fully under Information Commissioner's Office (ICO) data controller jurisdiction.",
                "To maintain absolute compliance, homeowners and commercial operators must demonstrate legitimate interest, establish transparent signage, and implement physical and digital privacy zones before system commissioning."
            ],
            "callout": "Never record public or neighbouring airspace without documented justification. Point cameras strictly within boundary perimeters wherever feasible."
        },
        {
            "title": "2. The Strict Prohibition on Audio Recording in Public & Communal Zones",
            "paragraphs": [
                "The ICO maintains an uncompromising stance regarding continuous ambient audio recording. Intercepting conversations of passersby, visitors, or neighbours without explicit consent constitutes an intrusive violation of privacy that cannot be justified under standard property security grounds.",
                "Professional CCTV hardware (Hikvision, Uniview, Dahua) featuring built-in microphones must have continuous audio capture disabled across all boundary and communal channels. Audio recording must only activate upon deliberate two-way intercom triggering (e.g., video doorbell press)."
            ],
            "table": [
                ["Monitoring Zone", "Video Capture Status", "Continuous Audio Capture", "ICO Signage Required"],
                ["Private Driveway / Garden", "Fully Permitted", "Strictly Prohibited", "Recommended"],
                ["Shared Access Road / HMO", "Permitted (Masked)", "Strictly Prohibited", "Mandatory"],
                ["Public Pavement / Road", "Requires Privacy Mask", "Unlawful Eavesdropping", "Mandatory with Contact"],
                ["Commercial Retail / Office", "Fully Permitted", "Prohibited (Except Panic)", "Mandatory ICO Sign"]
            ]
        },
        {
            "title": "3. Hardware Privacy Masking Configuration (Hikvision ColorVu & AcuSense)",
            "paragraphs": [
                "Commercial NVRs and IP cameras provide digital 4-point privacy masking overlays directly rendered onto the camera DSP prior to stream encoding. These blacked-out zones are permanently omitted from live feeds, NVR recordings, and remote playback.",
                "Our field installations calibrate digital masking down to the millimetre across neighbouring bedroom windows, private patio areas, and public footpaths, ensuring captured footage cannot record private spaces even when high-resolution 4K digital zoom is applied."
            ]
        },
        {
            "title": "4. Mandatory ICO Signage Specifications & Subject Access Requests (SAR)",
            "paragraphs": [
                "Where camera coverage captures shared or public zones, weatherproof warning signs must be placed at all points of entry. Signs must clearly state: (1) Purpose of monitoring (e.g. Crime Prevention & Public Safety); (2) Identity of Data Controller; (3) Contact telephone number / email.",
                "Operators must maintain a 30-day automated footage retention policy (auto-overwrite) and possess the technical capability to respond to Subject Access Requests (SAR) within 30 calendar days at £0 charge to the data subject."
            ],
            "callout": "Signage without contact details or operational purpose fails ICO compliance audits and renders footage inadmissible in civil boundary dispute proceedings."
        }
    ]
    build_pdf_document(
        filename="2026-uk-domestic-cctv-legal-compliance-checklist.pdf",
        title="2026 UK Domestic & Commercial CCTV Legal Compliance & Privacy Checklist",
        subtitle="ICO Surveillance Code, Boundary Privacy Masking, Audio Eavesdropping Prohibitions & SAR Procedures",
        doc_id="SPEC-CCTV-ICO-2026",
        sections=sections
    )

def generate_whitepaper_2():
    print("\n--- Generating Whitepaper 2: Hotel & HMO Anti-Theft TV Mounting ---")
    sections = [
        {
            "title": "1. Commercial Hospitality vs. Residential TV Mounting Liabilities",
            "paragraphs": [
                "Hospitality environments (hotels, guest houses, serviced apartments, student accommodation, and high-density HMO properties) experience continuous mechanical abuse, tampering, and theft risks that destroy consumer-grade TV brackets within months.",
                "Standard residential click-and-hook mounts allow screens to be unlatched in under 5 seconds. Furthermore, flimsy plastic latches fail under the downward cantilever leverage of guests pulling on screen edges, creating severe public liability injury risks."
            ],
            "callout": "All public and guest-facing wall brackets must feature industrial solid steel locking bars and pin-Torx security fasteners meeting commercial insurance standards."
        },
        {
            "title": "2. Structural Fastening & M6 SnapToggle Hollow-Wall Anchoring",
            "paragraphs": [
                "Modern commercial dry-lined plasterboard walls lack structural timber backing at optimal screen viewing heights. Standard plastic wall plugs or expanding metal rawlbolts crush gypsum cores under dynamic pull-out torque.",
                "ADI Communications deploys solid steel M6 SnapToggle cavity anchors rated to 120kg tensile load capacity per fixing point. The solid zinc-plated steel channel swivels behind 12.5mm or 25mm drywall, clamping the bracket with massive surface area distribution that eliminates wall blowouts."
            ],
            "table": [
                ["Fixing Type", "Plasterboard Pull-Out Rating", "Dynamic Shear Rating", "Hospitality Suitability"],
                ["Plastic Wall Plug", "10 kg - 15 kg", "15 kg", "Unacceptable (High Hazard)"],
                ["Hollow Wall Metal Anchor", "25 kg - 35 kg", "30 kg", "Unacceptable for Public Use"],
                ["M6 SnapToggle Steel Channel", "105 kg - 120 kg", "145 kg", "Fully Approved Commercial Standard"],
                ["M8 Masonry Sleeve Anchor", "250 kg+", "300 kg+", "Fully Approved Solid Brick/Block"]
            ]
        },
        {
            "title": "3. Commercial Display Protocol: Samsung LYNK REACH & LG Pro:Centric",
            "paragraphs": [
                "Commercial hospitality displays feature centralised management software allowing hoteliers to lock TV menus, disable physical input buttons, push custom branding, and broadcast fire emergency alerts.",
                "Mounting architecture must accommodate specialised hardware dimensions: Samsung The Frame displays require deep, fire-rated recessed cavity boxes to house One Connect media boxes flush within wall voids, while LG Pro:Centric screens demand ultra-slim clearance with discrete RJ45 data drops for network video delivery."
            ]
        },
        {
            "title": "4. Tamper-Proof In-Wall Media Enclosures & Cable Chasing Regulations",
            "paragraphs": [
                "External streaming sticks (Chromecasts, Apple TVs, Fire Sticks) plugged into rear HDMI ports invite theft and guest tampering. We install recessed metal enclosures positioned directly behind the display chassis, protected by keyed access locks.",
                "All mains power, HDMI 2.1 4K 120Hz interconnects, and Cat6 network cabling are chased through internal cavity voids using fire-rated grommets and low-smoke zero-halogen (LSZH) sheathing compliant with BS 7671 and UK Building Regulations Part B (Fire Safety)."
            ]
        }
    ]
    build_pdf_document(
        filename="hotel-hmo-anti-theft-tv-wall-mounting-specification.pdf",
        title="Commercial Hotel & HMO Anti-Theft TV Wall Mounting Specification",
        subtitle="Structural Asset Protection, M6 SnapToggle Hollow-Wall Anchoring, Tamper-Proof Locking & In-Wall Recessed Media Enclosures",
        doc_id="SPEC-TV-HOSP-2026",
        sections=sections
    )

def generate_whitepaper_3():
    print("\n--- Generating Whitepaper 3: Starlink 90mph Pennine Gale Mounting ---")
    sections = [
        {
            "title": "1. Wind Loading Dynamics on Starlink Gen 3 & Gen 2 Phased Arrays",
            "paragraphs": [
                "The rectangular SpaceX Starlink Gen 3 (594mm x 383mm) and Gen 2 (513mm x 303mm) flat panels present substantial surface area to high-velocity aerodynamic wind shear. Across the Pennines, Peak District, and Yorkshire Dales, wind gusts regularly exceed 75mph to 90mph.",
                "At 90mph, wind pressure on a Gen 3 panel creates over 450 Newtons of lateral force. Standard satellite mini-dishes have minimal surface drag, whereas flat electronic phased arrays act as aerofoils, transferring massive vibrational torque into mounting brackets and masonry."
            ],
            "callout": "Never deploy plastic or clamp-style satellite brackets for Starlink in Pennine or upland terrains. Galvanised 2-inch steel masts with welded storm gussets are mandatory."
        },
        {
            "title": "2. Non-Drill Stainless Chimney Lashing Cradles vs. Mechanical Anchor Failures",
            "paragraphs": [
                "Drilling mechanical anchors into aged stone or Victorian lime mortar chimney stacks causes catastrophic masonry fracturing during storm cycles. Vibrational oscillation shears mortar bonds, leading to stack instability and water ingress.",
                "The engineered solution is a non-drill chimney lashing cradle utilizing twin 5-metre stainless steel wire lashing cables wound around the chimney perimeter and tensioned with heavy-duty J-bolts. This compressive wrapping exerts uniform lateral pressure across all four masonry corners without a single drilled hole, preserving heritage architecture while withstanding 90mph+ gales."
            ],
            "table": [
                ["Mounting Architecture", "Wind Gale Rating", "Masonry Impact", "Heritage / Conservation Safe"],
                ["Plastic / Standard J-Pole", "40 mph - 50 mph", "Prone to Screws Pulling Out", "No"],
                ["Single-Stack Drill Bracket", "60 mph - 70 mph", "Cracks Victorian Lime Mortar", "No (Violates Listed Regs)"],
                ["Galvanised Heavy-Duty Starlink Chimney Bracket", "90 mph - 100 mph", "Double-Spaced Structural Anchors", "Yes (Engineered Stand-off)"],
                ["Stainless Non-Drill Chimney Lashing", "90 mph - 100 mph", "Zero Masonry Penetration", "100% Conservation Approved"]
            ]
        },
        {
            "title": "3. External Cat6 Channelling, Drip Loops & RoW Galvanic Isolation",
            "paragraphs": [
                "SpaceX factory Starlink cables feature proprietary connectors that must be protected during external wall ingress. We route UV-stabilised, direct-burial external Cat6 cable alongside the dish lead, terminating into a weatherproof IP66 external junction enclosure.",
                "Every external wall penetration features a downward-sloping 45-degree drip loop and heavy-duty silicone seal grommets, preventing driven rain from migrating along the cable sheath into internal wall cavities. Internal networking connects directly to Gigabit POE switches and whole-home mesh nodes."
            ]
        },
        {
            "title": "4. Outbuilding Network Extensions & Point-to-Point Wireless Bridges",
            "paragraphs": [
                "High-speed Starlink broadband is frequently deployed on rural farms, equestrian estates, and country properties with detached stone barns and garden home offices. Thick 500mm gritstone walls completely absorb standard Wi-Fi signals.",
                "We extend Starlink gigabit throughput across rural grounds up to 5 kilometres using commercial 5GHz / 60GHz outdoor point-to-point (PtP) wireless bridges (Ubiquiti airMAX / MikroTik) or direct-burial shielded Cat6/Fibre runs, delivering zero-latency 250Mbps+ connectivity to all outbuildings."
            ]
        }
    ]
    build_pdf_document(
        filename="starlink-90mph-pennine-gale-mounting-engineering-guide.pdf",
        title="Starlink Gen 3 & Gen 2 90mph Pennine Gale Mounting Engineering Guide",
        subtitle="Non-Drill Chimney Lashing Systems, Galvanised Heavy-Duty Starlink Chimney Brackets, Discrete Drip Loops & PtP Bridges",
        doc_id="SPEC-STAR-PENNINE-2026",
        sections=sections
    )

if __name__ == "__main__":
    print("=================================================================")
    print("  ADI COMMUNICATIONS - CORE ENGINEERING PDF WHITEPAPER ENGINE")
    print("  Lead Engineer: Gary Pearce (07860 244 274)")
    print("=================================================================")
    generate_whitepaper_1()
    generate_whitepaper_2()
    generate_whitepaper_3()
    print("\n[SUCCESS] All 3 engineering whitepapers generated and synchronized across all directories!")
