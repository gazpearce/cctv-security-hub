import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

OUTPUT_DIR = r"C:\Users\Gary\github-cctv-seo\stack_assets\documents"
os.makedirs(OUTPUT_DIR, exist_ok=True)

class NumberedCanvas(canvas.Canvas):
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
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#71717A"))
        # Header
        self.drawString(54, 800, "ADI COMMUNICATIONS — TECHNICAL ENGINEERING WHITE PAPER")
        self.drawRightString(541, 800, "FIELD SPECIFICATION BS 6701 / EN 50131")
        self.setStrokeColor(colors.HexColor("#E4E4E7"))
        self.setLineWidth(0.75)
        self.line(54, 792, 541, 792)
        # Footer
        self.line(54, 45, 541, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Lead Engineer: Gary Pearce (Direct: 07860 244 274) • £10M Public Liability")
        self.drawRightString(541, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

styles = getSampleStyleSheet()
title_style = ParagraphStyle(
    "DocTitle",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=22,
    leading=26,
    textColor=colors.HexColor("#09090B"),
    spaceAfter=8
)
subtitle_style = ParagraphStyle(
    "DocSubtitle",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=11,
    leading=15,
    textColor=colors.HexColor("#71717A"),
    spaceAfter=15
)
h2_style = ParagraphStyle(
    "SectionH2",
    parent=styles["Normal"],
    fontName="Helvetica-Bold",
    fontSize=13,
    leading=17,
    textColor=colors.HexColor("#09090B"),
    spaceBefore=12,
    spaceAfter=6
)
body_style = ParagraphStyle(
    "BodyDark",
    parent=styles["Normal"],
    fontName="Helvetica",
    fontSize=9.5,
    leading=14,
    textColor=colors.HexColor("#27272A"),
    spaceAfter=8
)
bullet_style = ParagraphStyle(
    "BulletText",
    parent=body_style,
    leftIndent=15,
    bulletIndent=5,
    spaceAfter=4
)
callout_style = ParagraphStyle(
    "Callout",
    parent=styles["Normal"],
    fontName="Helvetica-Oblique",
    fontSize=9,
    leading=13,
    textColor=colors.HexColor("#18181B"),
    backColor=colors.HexColor("#F4F4F5"),
    borderPadding=10,
    spaceBefore=8,
    spaceAfter=12
)

# 1. STARLINK WHITE PAPER
pdf_1 = os.path.join(OUTPUT_DIR, "Starlink_UK_Gale_Rated_Chimney_Mounting_Specification.pdf")
doc1 = SimpleDocTemplate(pdf_1, pagesize=A4, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
story1 = []

story1.append(Paragraph("SpaceX Starlink Gen 3 Satellite Rigging Specification", title_style))
story1.append(Paragraph("Pennine 90mph Gale Force Wind Loading, Non-Drill Chimney Lashing & BS 6701 Cable Integration", subtitle_style))
story1.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#FF5500"), spaceAfter=12))

story1.append(Paragraph("1. Executive Engineering Summary", h2_style))
story1.append(Paragraph(
    "This technical specification defines the physical installation methodology for SpaceX Starlink Gen 3 and Gen 2 terminals "
    "across exposed UK upland residential structures. Authored by Gary Pearce, Lead Infrastructure Engineer at ADI Communications "
    "(Direct Mobile: 07860 244 274, 25+ years hands-on field craftsmanship), this document details structural wind-load mitigation, "
    "non-drill stainless chimney lashing cradles, and weather-sealed cavity wall drops complying with UK BS 6701 standards.",
    body_style
))

story1.append(Paragraph("2. Structural Wind-Load & Shear Calculations (90mph Gale Rating)", h2_style))
story1.append(Paragraph(
    "Under BS EN 1991-1-4 (Eurocode 1: Actions on structures — General actions — Wind actions), a rectangular Starlink Gen 3 flat panel "
    "(0.22 m² surface area) experiences significant dynamic drag forces in Northern UK Pennine micro-climates:",
    body_style
))

table_data1 = [
    ["Wind Speed (mph)", "Velocity (m/s)", "Dynamic Pressure (N/m²)", "Drag Force (N)", "Structural Mounting Requirement"],
    ["45 mph (Gale)", "20.1 m/s", "247 N/m²", "65 N", "Standard 1.5-inch alloy standoff"],
    ["70 mph (Severe Gale)", "31.3 m/s", "599 N/m²", "158 N", "Heavy-duty galvanised heavy-duty Starlink chimney bracket"],
    ["90 mph (Storm Force 10)", "40.2 m/s", "990 N/m²", "261 N", "Twin stainless steel chimney lashing kit with corner mitres"],
    ["105 mph (Extreme Gust)", "46.9 m/s", "1,349 N/m²", "356 N", "10-gauge structural steel brackets with M10 masonry sleeves"]
]
t1 = Table(table_data1, colWidths=[85, 65, 95, 70, 172])
t1.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#09090B")),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 8),
    ('BOTTOMPADDING', (0,0), (-1,0), 6),
    ('TOPPADDING', (0,0), (-1,0), 6),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E4E4E7")),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 7.5),
    ('ALIGN', (1,0), (3,-1), 'CENTER'),
]))
story1.append(t1)
story1.append(Spacer(1, 10))

story1.append(Paragraph("3. Non-Drill Chimney Lashing Protocol", h2_style))
story1.append(Paragraph("• <b>Zero Masonry Penetration:</b> Never drill into Victorian lime mortar or single-skin chimney brickwork, which causes frost heave and structural spalling.", bullet_style))
story1.append(Paragraph("• <b>Dual Steel Wire Cradles:</b> High-tensile 7-strand galvanised wire wrapped around the chimney perimeter, secured with heavy-duty J-bolts and tension ratchets.", bullet_style))
story1.append(Paragraph("• <b>Corner Mitre Angle Protectors:</b> Formed steel corner plates distribute mechanical clamping pressure evenly across 4 masonry corners, preventing edge-cracking.", bullet_style))
story1.append(Paragraph("• <b>External Solid Copper Cat6:</b> UV-stabilised high-grade shielded cable with a 150mm downward drip loop before masonry ingress.", bullet_style))

story1.append(Paragraph(
    "<b>Rule 45 Reference & Verification:</b> Full interactive wind-load calculators, obstacle cone diagnostic tools, and complete case studies are available on the "
    "ADI Communications Technical Portal: <a href='https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/'><b>https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/</b></a> "
    "and the Google Shield Companion Hub at <a href='https://tvandhomesecurity.blogspot.com/'><b>https://tvandhomesecurity.blogspot.com/</b></a>.",
    callout_style
))

doc1.build(story1, canvasmaker=NumberedCanvas)
print(f"Generated: {pdf_1}")

# 2. AJAX SMART ALARMS WHITE PAPER
pdf_2 = os.path.join(OUTPUT_DIR, "Ajax_Smart_Alarms_Grade2_Compliance_Yorkshire_Manual.pdf")
doc2 = SimpleDocTemplate(pdf_2, pagesize=A4, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
story2 = []

story2.append(Paragraph("Ajax Smart Alarms Grade 2 Architectural Manual", title_style))
story2.append(Paragraph("BS EN 50131-1 Compliance, Jeweller 868MHz Anti-Jamming & Dual-SIM Cellular Failover", subtitle_style))
story2.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#0066FF"), spaceAfter=12))

story2.append(Paragraph("1. Commercial Physical Security Engineering", h2_style))
story2.append(Paragraph(
    "This engineering standard outlines the deployment architecture for BS EN 50131 Grade 2 and Grade 3 wireless alarm systems "
    "installed by Gary Pearce / ADI Communications (07860 244 274, £10,000,000 Public Liability Insurance). It details why traditional "
    "433MHz legacy burglar alarm bells are vulnerable to handheld RF jammers and how Ajax Jeweller encrypted TDMA protocol provides "
    "uncompromised domestic and commercial perimeter protection across West Yorkshire.",
    body_style
))

story2.append(Paragraph("2. Technical Protocol Comparison: Legacy 433MHz vs Ajax Jeweller 868MHz", h2_style))
table_data2 = [
    ["Security Parameter", "Legacy 433MHz Bell Boxes (1990–2015)", "Ajax Jeweller 868MHz Protocol (Grade 2)"],
    ["Transmission Frequency", "Single fixed 433.92 MHz channel", "Multi-frequency hopping 868.0–868.6 MHz"],
    ["Encryption Standard", "Fixed code / No encryption", "AES-128 block cipher with dynamic rolling token"],
    ["Jamming Detection", "None (blind siren remains silent)", "Instant hub detection (sub-0.15s) with push alert"],
    ["Polling Supervision", "Unmonitored or 12–24 hour ping", "Configurable 12 to 300 second encrypted heartbeat"],
    ["Battery Autonomy", "1–2 years (frequent battery change)", "Up to 5–7 years with pre-installed industrial lithium"],
    ["Backhaul Communication", "PSTN copper line (easily cut outside)", "Ethernet + Dual Micro-SIM 2G/3G/4G cellular failover"]
]
t2 = Table(table_data2, colWidths=[120, 170, 197])
t2.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#09090B")),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 8),
    ('BOTTOMPADDING', (0,0), (-1,0), 6),
    ('TOPPADDING', (0,0), (-1,0), 6),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E4E4E7")),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 7.5),
]))
story2.append(t2)
story2.append(Spacer(1, 10))

story2.append(Paragraph("3. MotionCam PhOD Photo-Verification Architecture", h2_style))
story2.append(Paragraph("• <b>Dual Detection Vectors:</b> Combines wide-angle PIR motion detection with high-speed CMOS camera sensor.", bullet_style))
story2.append(Paragraph("• <b>Wings Independent Radio:</b> Operates on a dedicated secondary 868MHz radio channel specifically for animated image transmission.", bullet_style))
story2.append(Paragraph("• <b>Sub-9 Second Verification:</b> Sends encrypted 640×480 series photos directly to owner smartphones and Police monitoring stations before intruder enters the premises.", bullet_style))
story2.append(Paragraph("• <b>Outdoor Perimeter Defense:</b> MotionCam Outdoor PhOD provides 90° adjustable detection angle with anti-masking Grade 3 sensors.", bullet_style))

story2.append(Paragraph(
    "<b>Rule 45 Reference & Verification:</b> Detailed Grade selector tools, wireless range calculation models, and installation checklists are hosted on the "
    "ADI Communications Technical Portal: <a href='https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/'><b>https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/</b></a> "
    "and the Google Drive Forensic Vault at <a href='https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88'><b>Google Drive Hub</b></a>.",
    callout_style
))

doc2.build(story2, canvasmaker=NumberedCanvas)
print(f"Generated: {pdf_2}")

# 3. ETHERNET UPSTAIRS WHITE PAPER
pdf_3 = os.path.join(OUTPUT_DIR, "Ethernet_Upstairs_Without_Running_Cables_Field_Guide.pdf")
doc3 = SimpleDocTemplate(pdf_3, pagesize=A4, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
story3 = []

story3.append(Paragraph("How to Get Ethernet Upstairs Without Running Cables", title_style))
story3.append(Paragraph("UK Residential Field Analysis: Powerline AV2 vs MoCA 2.5 vs Discrete Exterior Cat6 Cavity Drops", subtitle_style))
story3.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#10B981"), spaceAfter=12))

story3.append(Paragraph("1. The UK Residential Wi-Fi Problem", h2_style))
story3.append(Paragraph(
    "Victorian gritstone, 1930s cavity masonry, and modern foil-backed Kingspan insulation severely attenuate 5GHz and 6GHz Wi-Fi "
    "signals in UK multi-storey homes. Authored by Gary Pearce (ADI Communications, 07860 244 274, 25+ years experience), "
    "this guide rigorously benchmarks real-world throughput, latency jitter, and physical trade feasibility for retrofitting gigabit "
    "backhaul to upstairs offices and bedrooms.",
    body_style
))

story3.append(Paragraph("2. Technical Throughput & Latency Jitter Comparison", h2_style))
table_data3 = [
    ["Technology", "Max Tested Bandwidth", "Ping Latency (Jitter)", "UK Wiring Suitability", "Physical Trade Feasibility"],
    ["Powerline AV2 (HomePlug)", "40–120 Mbps", "18–45 ms (High Jitter)", "Poor across dual consumer units or RCDs", "DIY plug-in; unstable during appliance spikes"],
    ["MoCA 2.5 (Coaxial)", "600–900 Mbps", "3–6 ms (Low Jitter)", "Excellent if WF100 coaxial cabling exists", "Requires unused aerial coaxial drops in bedrooms"],
    ["Tri-Band Wi-Fi 7 Mesh", "200–450 Mbps", "8–15 ms (Medium Jitter)", "Fair; heavily degraded by foil insulation", "No cabling; high upfront hardware cost (£400+)"],
    ["Exterior UV Cat6 Cavity Drop", "1,000–10,000 Mbps", "0.5–1.0 ms (Zero Jitter)", "100% universal across all UK masonry", "Trade installation by Gary Pearce; 100% stable"]
]
t3 = Table(table_data3, colWidths=[110, 85, 95, 105, 92])
t3.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#09090B")),
    ('TEXTCOLOR', (0,0), (-1,0), colors.white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,0), 8),
    ('BOTTOMPADDING', (0,0), (-1,0), 6),
    ('TOPPADDING', (0,0), (-1,0), 6),
    ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
    ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E4E4E7")),
    ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
    ('FONTSIZE', (0,1), (-1,-1), 7.5),
]))
story3.append(t3)
story3.append(Spacer(1, 10))

story3.append(Paragraph("3. Exterior Solid Copper Cat6 Installation Protocol", h2_style))
story3.append(Paragraph("• <b>Solid Copper Conductors:</b> Never use Copper Clad Aluminium (CCA) which oxidises and fails under UK winter frost.", bullet_style))
story3.append(Paragraph("• <b>UV-Rated Polyethylene Sheath:</b> 100% UV-resistant external black sheath preventing UV cracking and water ingress.", bullet_style))
story3.append(Paragraph("• <b>Mortar Line Drilling & Drip Loop:</b> Drilled at an upward angle through mortar line with a downward silicone drip loop preventing rainwater tracking inside.", bullet_style))
story3.append(Paragraph("• <b>Fluke DSX-8000 Certified:</b> Every drop certified to ISO/IEC 11801 Class E standards with hardwired RJ45 faceplates.", bullet_style))

story3.append(Paragraph(
    "<b>Rule 45 Reference & Verification:</b> Read the full investigative field report and interactive backhaul calculator at: "
    "<a href='https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/'><b>https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/</b></a> "
    "and the Google Shield Companion Post on <a href='https://tvandhomesecurity.blogspot.com/'><b>tvandhomesecurity.blogspot.com</b></a>.",
    callout_style
))

doc3.build(story3, canvasmaker=NumberedCanvas)
print(f"Generated: {pdf_3}")
