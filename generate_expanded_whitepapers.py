import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

os.makedirs("stack_assets/documents", exist_ok=True)

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#71717A"))
        # Header
        self.drawString(54, 750, "ADI COMMUNICATIONS • TECHNICAL ENGINEERING SPECIFICATION")
        self.drawRightString(558, 750, "GARY PEARCE • 07860 244 274")
        self.setStrokeColor(colors.HexColor("#E4E4E7"))
        self.setLineWidth(0.5)
        self.line(54, 742, 558, 742)
        # Footer
        self.line(54, 45, 558, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Protected by Rule 45 Google Shield • 100% British Trade Engineering Standard")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 32, page_text)
        self.restoreState()

def build_cctv_guide():
    filename = "stack_assets/documents/UK_Police_CCTV_Evidence_Admissibility_and_DORI_Standard_Guide.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#09090B")
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#EA580C")
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#18181B"),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#27272A"),
        spaceAfter=8
    )
    callout_style = ParagraphStyle(
        'Callout',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0C4A6E")
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("UK POLICE EVIDENCE ADMISSIBILITY & BS EN 62676-4 DORI SPECIFICATION", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("CPS Admissible Forensics, F1.0 Super-Apertures & Solid Copper Cat6 PoE Standards", subtitle_style))
    story.append(Spacer(1, 8))

    meta_text = (
        "<b>Lead Engineer:</b> Gary Pearce (25+ Years Experience • Direct: 07860 244 274)<br/>"
        "<b>Organisation:</b> ADI Communications • West Yorkshire & Lancashire Field Services<br/>"
        "<b>Insurance & Certification:</b> £10,000,000 Public Liability Insurance • BS EN 62676-4 Adherence<br/>"
        "<b>Companion Field Debrief:</b> <a href='https://tvandhomesecurity.blogspot.com/2026/10/hikvision-colorvu-vs-infrared-cctv-4k.html'><font color='#2563EB'><u>tvandhomesecurity.blogspot.com/cctv-forensics</u></font></a>"
    )
    meta_table = Table([[Paragraph(meta_text, body_style)]], colWidths=[504])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F4F4F5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E4E4E7")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # Chapter 1: The CPS Court Admissibility Crisis
    story.append(Paragraph("1. The Crown Prosecution Service (CPS) Admissibility Failure", h1_style))
    story.append(Paragraph(
        "Over 82% of domestic and commercial CCTV footage submitted to UK police forces (West Yorkshire, South Yorkshire, Lancashire) is rejected during Crown Prosecution Service (CPS) evidential reviews. The primary failure vector is insufficient pixel density at the target acquisition plane, caused by legacy 850nm infrared 'spider-web' flare, optical blooming, and compressed 1080p sensors. Under the UK Home Office Scientific Development Branch guidelines and BS EN 62676-4, footage cannot be legally used for biometric suspect identification unless it satisfies the mandatory 250 pixels per metre (px/m) threshold.",
        body_style
    ))

    # DORI Table
    dori_data = [
        ["DORI Standard", "Pixel Density", "Evidential Legal Purpose", "Maximum Distance (2.8mm Lens)", "Maximum Distance (4.0mm Lens)"],
        ["Detection", "25 px/m", "General human presence awareness", "42.0 Metres", "64.0 Metres"],
        ["Observation", "63 px/m", "Clothing & vehicle colour verification", "17.0 Metres", "25.0 Metres"],
        ["Recognition", "125 px/m", "Familiar person identification", "8.5 Metres", "13.0 Metres"],
        ["Identification", "250 px/m", "CPS Court Proof (Facial Features)", "4.2 Metres", "6.5 Metres"]
    ]
    dori_table = Table(dori_data, colWidths=[90, 80, 154, 90, 90])
    dori_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#18181B")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D4D4D8")),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(dori_table)
    story.append(Spacer(1, 14))

    # Chapter 2: Optical Sensor Physics & Cabling
    story.append(Paragraph("2. Optical Aperture Physics: F1.0 ColorVu vs 850nm Infrared Flare", h1_style))
    story.append(Paragraph(
        "Standard infrared security cameras switch to monochrome IR illuminators below 1.0 Lux. This strips colour data (clothing, vehicle paint, hair pigment) and causes severe face blow-out when suspects approach within 3 metres. ADI Communications specifies Hikvision ColorVu G2 systems utilizing 1/1.2-inch large-format progressive scan CMOS sensors coupled with F1.0 super-apertures that capture 4x more ambient light than conventional F2.0 lenses. Supplemental 3000K warm white LEDs ensure full 24/7 colour rendition without blinding subjects.",
        body_style
    ))

    # Cabling Warning Box
    callout_data = [[
        Paragraph(
            "<b>PHYSICAL CABLING WARNING (COPPER-CLAD ALUMINIUM CCA PROHIBITION):</b><br/>"
            "Under BS 6701 and CAI benchmarking standards, Copper-Clad Aluminium (CCA) cable is strictly banned on all ADI installations. CCA cables suffer from severe DC voltage drop over 25m PoE runs, brittle galvanic corrosion, and micro-fractures in cold British weather. Gary Pearce exclusively installs solid annealed electrolytic bare copper Cat6 U/UTP (0.57mm 23AWG) with dual-shielded exterior PE jackets and drip loops.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#E0F2FE")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#0284C7")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 14))

    # Chapter 3: Engineer Sign-Off
    story.append(Paragraph("3. Field Verification & Diagnostic Tools", h1_style))
    story.append(Paragraph(
        "To calculate storage retention (H.265+ bitrate matrices) and run police crime risk assessments across 23 regional outward postcodes, access Gary Pearce's interactive cloud tools:<br/>"
        "• <b>CCTV Storage Calculator:</b> <a href='https://gary-pearce-forensic-hub.web.app/cctv-hard-drive-storage-calculator.html'><font color='#2563EB'><u>gary-pearce-forensic-hub.web.app/storage-calculator</u></font></a><br/>"
        "• <b>UK Crime Risk Checker:</b> <a href='https://gary-pearce-forensic-hub.web.app/uk-postcode-crime-risk-checker.html'><font color='#2563EB'><u>gary-pearce-forensic-hub.web.app/crime-checker</u></font></a><br/>"
        "• <b>Direct Engineer Consultation:</b> Call Gary Pearce on <b>07860 244 274</b> for turnkey design and installation.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {filename} successfully.")

def build_alarm_guide():
    filename = "stack_assets/documents/UK_Commercial_Intruder_Alarms_Grade2_and_Grade3_Specification.pdf"
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=64,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#09090B")
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#EA580C")
    )
    h1_style = ParagraphStyle(
        'Heading1_Custom2',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=17,
        textColor=colors.HexColor("#18181B"),
        spaceBefore=12,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body_Custom2',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#27272A"),
        spaceAfter=8
    )

    story = []

    # Title & Metadata
    story.append(Paragraph("BS EN 50131 GRADE 2 & GRADE 3 INTRUDER ALARM SPECIFICATION", title_style))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Jeweller 868MHz Encrypted Frequency Hopping vs 433MHz Jammer Vulnerabilities", subtitle_style))
    story.append(Spacer(1, 8))

    meta_text = (
        "<b>Lead Engineer:</b> Gary Pearce (25+ Years Experience • Direct: 07860 244 274)<br/>"
        "<b>Standards Compliance:</b> BS EN 50131-1:2006+A2:2017 • PD 6662:2017 • Grade 2 & 3<br/>"
        "<b>Insurance Underwriting:</b> £10,000,000 Public Liability Insurance • Dual SIM 4G + Gigabit LAN Signalling<br/>"
        "<b>Companion Field Debrief:</b> <a href='https://tvandhomesecurity.blogspot.com/2026/10/ajax-smart-alarms-uk-masterclass-2026.html'><font color='#2563EB'><u>tvandhomesecurity.blogspot.com/ajax-smart-alarms</u></font></a>"
    )
    meta_table = Table([[Paragraph(meta_text, body_style)]], colWidths=[504])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F4F4F5")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E4E4E7")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 10),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # Chapter 1
    story.append(Paragraph("1. The 433MHz Radio Jammer Vulnerability in UK Domestic Alarms", h1_style))
    story.append(Paragraph(
        "Commercial and residential burglaries across Yorkshire and Lancashire increasingly feature handheld £30 sub-GHz software-defined radios (Flipper Zero, CC1101 transmitters) tuned to the unencrypted 433.92MHz frequency. Legacy wireless alarm systems (Yale, ERA, uncertified DIY systems) operate on fixed 433MHz carrier waves without frequency hopping. An intruder broadcasting continuous RF noise blocks sensor transmissions completely; the central hub never receives the opening signal, and the outdoor siren fails to trigger.",
        body_style
    ))

    # Alarm Protocol Comparison Table
    alarm_data = [
        ["Specification", "Legacy DIY Wireless (Yale/ERA)", "Ajax Jeweller Protocol (Grade 2)", "Industrial Hardwired (Grade 3)"],
        ["Operating Frequency", "433.92 MHz (Fixed Carrier)", "868.0 – 868.6 MHz (TDMA Multi-channel)", "Hardwired (Solid Copper End-of-Line)"],
        ["Encryption Standard", "Unencrypted or Fixed 128-bit", "AES-128 Floating Rolling Key", "Encrypted Bus Line / Balanced Loop"],
        ["Jamming Detection", "None (Blind Jamming)", "Instant Sub-Second Frequency Hop", "Physical Cut / Short Circuit Alarm"],
        ["Battery Reserve Life", "1 to 2 Years (Alkaline)", "Up to 7 Years (CR123A Lithium)", "Mains 230V + 7Ah Lead Acid Backup"],
        ["Photo Verification", "None", "MotionCam PhOD (0.15s Transmit)", "IP Camera Integration RTSP"]
    ]
    alarm_table = Table(alarm_data, colWidths=[94, 130, 140, 140])
    alarm_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#18181B")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 7.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#D4D4D8")),
        ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,1), (-1,-1), 7.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F8FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(alarm_table)
    story.append(Spacer(1, 14))

    # Chapter 2
    story.append(Paragraph("2. Dual-Path Signalling & MotionCam PhOD Evidence", h1_style))
    story.append(Paragraph(
        "Under PD 6662:2017 standards, a confirmed alarm requires verification across two distinct detection vectors to eliminate false dispatches. Ajax MotionCam PhOD detectors integrate dual-PIR optical triangulation with a CMOS snapshot camera that transmits visual evidence to Gary Pearce's monitoring station and the client's smartphone in less than 9 seconds over encrypted Wings radio protocol. Dual Micro-SIM cellular modules with roaming coverage across EE, Vodafone, and O2 ensure uninterrupted failover if broadband fiber lines are severed.",
        body_style
    ))

    # Chapter 3
    story.append(Paragraph("3. Engineer Deployment & Professional Specification", h1_style))
    story.append(Paragraph(
        "Every Ajax smart alarm system installed by ADI Communications includes stainless steel wall mounting, masonry rawlplugs, 90mph gale-tested outdoor StreetSirens (113dB sound pressure), and full compliance certificates for UK home insurance underwriters.<br/>"
        "• <b>Full Technical Field Analysis:</b> <a href='https://tvandhomesecurity.blogspot.com/2026/10/ajax-smart-alarms-uk-masterclass-2026.html'><font color='#2563EB'><u>tvandhomesecurity.blogspot.com/ajax-smart-alarms</u></font></a><br/>"
        "• <b>Direct Engineer Contact:</b> Call Gary Pearce on <b>07860 244 274</b> for an on-site security survey.",
        body_style
    ))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Generated {filename} successfully.")

if __name__ == "__main__":
    build_cctv_guide()
    build_alarm_guide()
