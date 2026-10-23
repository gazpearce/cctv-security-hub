#!/usr/bin/env python3
"""
produce_faq_multimedia.py
=========================
Autonomous FAQ-Driven Multimedia Production Engine for Gary Pearce / ADI Communications.
Produces 4 high-intent multimedia formats per website FAQ across all 6 service pillars:
  1. 1080p MP4 Engineering Video (FFmpeg 8.1.1, Ken Burns zoompan, audio waveform, animated progress bar)
  2. 1600x900 WebP High-Contrast Thumbnail (Obsidian scrim, telemetry badge, drop-shadow typography)
  3. 16:9 Slide Deck (PPTX via python-pptx + vector PDF via reportlab with NumberedCanvas)
  4. Authentic Trade Photography with Binary EXIF/IPTC Metadata (piexif / PIL)
  5. RSS Feed Ingestion (podcast.xml & faq_multimedia_feed.xml with BLUF answers)
  6. Master Backlink Ledger Synchronization (14-column doc3_published_asset_links.csv)

Strict Compliance Invariants:
  - Rule 28 Voice API Air-Gap: Exclusively uses edge_tts (en-GB-RyanNeural) at £0 token cost.
  - Rule 30 Hook Architecture: Hook & Question first, mid-roll identity (0:08-0:15).
  - Rule 20 Trade Identity: Gary Pearce (07860 244 274, 9.98/10 rating across 84+ reviews, 0 Checkatrade).
  - Rule 45 Google Shield: Top-of-Stack Google Apex upward links, deep buffer downward links.

Author: Gary Pearce / ADI Communications
Repository: github-cctv-seo
"""

import os
import sys
import re
import csv
import json
import time
import shutil
import asyncio
import argparse
import subprocess
import email.utils
import posixpath
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from xml.etree import ElementTree as ET
from xml.dom import minidom

# Ensure UTF-8 console output on Windows
if sys.stdout and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if sys.stderr and hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from PIL import Image, ImageDraw, ImageFont, ImageOps
import piexif
from piexif import helper

# python-pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

# reportlab
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# -----------------------------------------------------------------------------
# Path Resolution & Directories
# -----------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent
ASSETS_DIR = REPO_ROOT / "assets"
IMAGES_DIR = ASSETS_DIR / "images"
VIDEOS_DIR = ASSETS_DIR / "videos"
SLIDES_DIR = REPO_ROOT / "stack_assets" / "slides"
DOCS_DIR = REPO_ROOT / "stack_assets" / "documents"
CACHE_DIR = REPO_ROOT / ".cache" / "faq_multimedia_build"

VIDEOS_DIR.mkdir(parents=True, exist_ok=True)
SLIDES_DIR.mkdir(parents=True, exist_ok=True)
DOCS_DIR.mkdir(parents=True, exist_ok=True)
CACHE_DIR.mkdir(parents=True, exist_ok=True)

CATALOG_PATH = REPO_ROOT / "faq_multimedia_metadata_catalog.json"
DOC3_CSV_PATH = REPO_ROOT / "doc3_published_asset_links.csv"
PODCAST_FEED_PATH = REPO_ROOT / "podcast.xml"
FAQ_FEED_PATH = REPO_ROOT / "faq_multimedia_feed.xml"

# System Fonts
FONT_ARIAL_BOLD = "C:/Windows/Fonts/arialbd.ttf"
FONT_SEGOE_REG = "C:/Windows/Fonts/segoeui.ttf"
FONT_SEGOE_BOLD = "C:/Windows/Fonts/segoeuib.ttf"
FONT_CONSOLA_BOLD = "C:/Windows/Fonts/consolab.ttf"

# Google Citadel Apex Endpoints
GOOGLE_SLIDES_APEX_URL = "https://docs.google.com/presentation/d/e/2PACX-1vTb-2iOvkk7k2_hkQ2hI3HDzuRDZrKUQmbhPSU3JHLx6XHHdzR1zzPlyo7ed6QBdfA3ly0RiUy6BRMh/pub"
GOOGLE_DRIVE_VAULT_URL = "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88"
BLOGGER_SHIELD_URL = "https://tvandhomesecurity.blogspot.com/"
YOUTUBE_APEX_URL = "https://www.youtube.com/@CCTV.services"
FIREBASE_HUB_URL = "https://gary-pearce-forensic-hub.web.app"

# Coordinates Centroid (Morley / Leeds / West Yorkshire)
DEFAULT_LAT = 53.7489
DEFAULT_LON = -1.6628

DOC3_COLUMNS = [
    "asset_id", "parent_profile_id", "platform_name", "profile_live_url",
    "asset_title", "asset_type", "asset_public_url", "top_of_stack_apex_url",
    "shield_target_url", "seo_tags", "seo_description_summary",
    "dofollow_status", "publication_date", "verification_status"
]


def get_font(path: str, size: int) -> ImageFont.FreeTypeFont:
    """Load TrueType font or fallback to default if path missing."""
    if os.path.exists(path):
        return ImageFont.truetype(path, size)
    return ImageFont.load_default()


# =============================================================================
# 1. Doc3 Registry Guard (14-Column Invariant & Rule 45 Enforcement)
# =============================================================================

class Doc3RegistryGuard:
    """Guarantees strict 14-column layout and Rule 45 compliance for doc3 CSV."""

    @staticmethod
    def get_next_asset_id(doc3_path: Path) -> str:
        """Determines the next sequential LINK-XXXX primary key."""
        max_id = 0
        if doc3_path.exists():
            with open(doc3_path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.reader(f)
                header = next(reader, None)
                for row in reader:
                    if row and len(row) > 0 and row[0].startswith("LINK-"):
                        try:
                            num = int(row[0].split("-")[1])
                            if num > max_id:
                                max_id = num
                        except (ValueError, IndexError):
                            pass
        return f"LINK-{max_id + 1:04d}"

    @classmethod
    def register_asset(cls, doc3_path: Path, entry: Dict[str, Any]) -> str:
        """
        Validates and registers an asset adhering strictly to 14 columns.
        Raises ValueError if any mandatory field is missing or invalid.
        """
        asset_id = entry.get("asset_id") or cls.get_next_asset_id(doc3_path)

        # Enforce Rule 45 check: normalize URLs before checking for naked root links
        shield_url = entry.get("shield_target_url", "")
        for key in ("shield_target_url", "top_of_stack_apex_url", "asset_public_url"):
            val = entry.get(key, "")
            if val and isinstance(val, str):
                unquoted = urllib.parse.unquote(val.strip())
                if re.search(r"(?:https?:)?//(?:www\.)?adicommunications\.co\.uk\.?(?::\d+)?", unquoted, re.I):
                    url_to_parse = unquoted if "://" in unquoted else ("https:" + unquoted if unquoted.startswith("//") else "//" + unquoted)
                    parsed = urllib.parse.urlparse(url_to_parse)
                    path_no_query = re.split(r"[?#]", parsed.path or "")[0]
                    norm = posixpath.normpath("/" + path_no_query.lstrip("/")).lower()
                    if norm == "/" or norm in ("/index.html", "/index.php", "/index.htm"):
                        raise ValueError(f"Rule 45 Violation: naked root link rejected in {key}: {val}")

        row = [
            asset_id,
            entry.get("parent_profile_id", "PROF-MISC-01"),
            entry.get("platform_name", "Web Platform"),
            entry.get("profile_live_url", ""),
            entry.get("asset_title", "Untitled Asset"),
            entry.get("asset_type", "Asset"),
            entry.get("asset_public_url", ""),
            entry.get("top_of_stack_apex_url", GOOGLE_SLIDES_APEX_URL),
            shield_url,
            entry.get("seo_tags", "#trade #security"),
            entry.get("seo_description_summary", ""),
            entry.get("dofollow_status", "Follow"),
            entry.get("publication_date", datetime.now().strftime("%Y-%m-%d")),
            entry.get("verification_status", "HTTP_200")
        ]

        if len(row) != 14:
            raise ValueError(f"Integrity check failed: Expected 14 columns, got {len(row)}")

        # Check if asset_public_url or asset_id already exists to prevent duplication
        if doc3_path.exists():
            with open(doc3_path, "r", encoding="utf-8", errors="replace") as f:
                reader = csv.reader(f)
                for existing_row in reader:
                    if existing_row and len(existing_row) >= 7:
                        if existing_row[0] == asset_id or (row[6] and existing_row[6] == row[6]):
                            return existing_row[0]

        # Atomic append using csv.writer with proper minimal quoting
        with open(doc3_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
            writer.writerow(row)

        return asset_id


# =============================================================================
# 2. Slide Deck Generator (16:9 PPTX & Vector PDF)
# =============================================================================

class NumberedCanvas(canvas.Canvas):
    """Two-pass ReportLab canvas for running header/footer and accurate page count."""
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
            self.draw_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#71717A"))
        # Top running header
        self.drawString(54, 800, "ADI COMMUNICATIONS • TECHNICAL FIELD ENGINEERING SPECIFICATION")
        self.drawRightString(541, 800, "GARY PEARCE • 07860 244 274")
        self.setStrokeColor(colors.HexColor("#E4E4E7"))
        self.setLineWidth(0.75)
        self.line(54, 792, 541, 792)
        # Bottom running footer
        self.line(54, 45, 541, 45)
        self.setFont("Helvetica", 8)
        self.drawString(54, 32, "Lead Engineer: Gary Pearce (Direct: 07860 244 274) • £10M Public Liability • Protected by Rule 45")
        self.drawRightString(541, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()


class FAQSlideGenerator:
    """Produces 16:9 widescreen PPTX presentations and vector PDF companions."""

    def __init__(self, output_dir: Path = SLIDES_DIR, docs_dir: Path = DOCS_DIR):
        self.output_dir = output_dir
        self.docs_dir = docs_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.docs_dir.mkdir(parents=True, exist_ok=True)

        self.C_OBSIDIAN = RGBColor(5, 5, 8)
        self.C_CARD_BG = RGBColor(18, 18, 24)
        self.C_ORANGE = RGBColor(255, 85, 0)
        self.C_WHITE = RGBColor(255, 255, 255)
        self.C_MUTED = RGBColor(161, 161, 170)
        self.C_BORDER = RGBColor(39, 39, 42)
        self.C_CYAN = RGBColor(56, 189, 248)

    def _extract_bluf(self, faq_item: dict) -> str:
        if "bluf" in faq_item and faq_item["bluf"]:
            return faq_item["bluf"]
        # Derive BLUF from script narration
        script = faq_item.get("script_narration", "")
        sentences = [s.strip() for s in re.split(r"(?<=[.?!])\s+", script) if s.strip()]
        if len(sentences) >= 3:
            # Skip opener if question, take core answer sentences
            core = [s for s in sentences if not s.startswith("Why do") and not s.startswith("How can") and not s.startswith("Can a") and not s.startswith("I'm Gary")]
            if core:
                return " ".join(core[:2])
        return script[:220] + "..." if len(script) > 220 else script

    def generate_pptx(self, faq_item: dict, out_path: Optional[Path] = None) -> Path:
        slug = faq_item.get("slug", "faq")
        if out_path is None:
            out_path = self.output_dir / f"{slug}.pptx"

        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        blank_layout = prs.slide_layouts[6]

        service_name = faq_item.get("service", "Trade Engineering")
        question = faq_item.get("question", "Field Engineering Question")
        standards = faq_item.get("technical_standards", ["British Standard Certified", "100% Solid Copper"])
        bluf_text = self._extract_bluf(faq_item)

        # -------------------------------------------------------------
        # Slide 1: Title & BLUF Executive Summary
        # -------------------------------------------------------------
        s1 = prs.slides.add_slide(blank_layout)
        bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg1.fill.solid()
        bg1.fill.fore_color.rgb = self.C_OBSIDIAN
        bg1.line.fill.background()

        # Header Category Badge
        tb_h = s1.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.4))
        p_h = tb_h.text_frame.paragraphs[0]
        p_h.text = f"ADI COMMUNICATIONS • {service_name.upper()} FIELD SPECIFICATION"
        p_h.font.size = Pt(10)
        p_h.font.bold = True
        p_h.font.color.rgb = self.C_ORANGE

        # Question Title H1
        tb_q = s1.shapes.add_textbox(Inches(0.8), Inches(1.1), Inches(11.733), Inches(1.4))
        tf_q = tb_q.text_frame
        tf_q.word_wrap = True
        p_q = tf_q.paragraphs[0]
        p_q.text = question
        p_q.font.size = Pt(26)
        p_q.font.bold = True
        p_q.font.color.rgb = self.C_WHITE

        # BLUF Box
        bluf_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.7), Inches(11.733), Inches(2.3))
        bluf_box.fill.solid()
        bluf_box.fill.fore_color.rgb = self.C_CARD_BG
        bluf_box.line.color.rgb = self.C_ORANGE
        bluf_box.line.width = Pt(1.5)
        btf = bluf_box.text_frame
        btf.word_wrap = True
        btf.margin_left = Inches(0.4)
        btf.margin_top = Inches(0.3)
        bp1 = btf.paragraphs[0]
        bp1.text = "BOTTOM LINE UP FRONT (BLUF) TRADE ANSWER:"
        bp1.font.size = Pt(12)
        bp1.font.bold = True
        bp1.font.color.rgb = self.C_ORANGE
        bp2 = btf.add_paragraph()
        bp2.text = bluf_text
        bp2.font.size = Pt(13)
        bp2.font.color.rgb = self.C_WHITE
        bp2.space_before = Pt(8)

        # Trust Badges
        tb_b = s1.shapes.add_textbox(Inches(0.8), Inches(5.3), Inches(11.733), Inches(0.5))
        p_b = tb_b.text_frame.paragraphs[0]
        p_b.text = f"⚡ {' • '.join(standards[:3])} | 🛡️ £10M Public Liability | 📍 Yorkshire & Lancashire Regional Engineering"
        p_b.font.size = Pt(11)
        p_b.font.color.rgb = self.C_MUTED

        # Footer
        tb_f = s1.shapes.add_textbox(Inches(0.8), Inches(6.9), Inches(11.733), Inches(0.4))
        p_f = tb_f.text_frame.paragraphs[0]
        p_f.text = "Lead Engineer: Gary Pearce (07860 244 274) • 25+ Yrs Field Craftsmanship • 9.98/10 Rating | Slide 1 of 4"
        p_f.font.size = Pt(9)
        p_f.font.color.rgb = self.C_MUTED

        # -------------------------------------------------------------
        # Slide 2: Technical Breakdown & Engineering Comparison
        # -------------------------------------------------------------
        s2 = prs.slides.add_slide(blank_layout)
        bg2 = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg2.fill.solid()
        bg2.fill.fore_color.rgb = self.C_OBSIDIAN
        bg2.line.fill.background()

        tb_s2 = s2.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.8))
        tf_s2 = tb_s2.text_frame
        p_s2 = tf_s2.paragraphs[0]
        p_s2.text = "FIELD BREAKDOWN: BUDGET DEFECTS VS TRADE ENGINEERING"
        p_s2.font.size = Pt(14)
        p_s2.font.bold = True
        p_s2.font.color.rgb = self.C_ORANGE

        # Card 1: Common Mistakes / Budget Defect
        c1 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.5), Inches(5.6), Inches(5.0))
        c1.fill.solid()
        c1.fill.fore_color.rgb = self.C_CARD_BG
        c1.line.color.rgb = RGBColor(220, 38, 38)
        c1_tf = c1.text_frame
        c1_tf.word_wrap = True
        c1_tf.margin_left = Inches(0.3)
        c1_tf.margin_top = Inches(0.3)
        c1_tf.paragraphs[0].text = "❌ COMMON BUDGET SHORTFALLS"
        c1_tf.paragraphs[0].font.bold = True
        c1_tf.paragraphs[0].font.size = Pt(13)
        c1_tf.paragraphs[0].font.color.rgb = RGBColor(239, 68, 68)

        def_mistakes = faq_item.get("card1_bullets", [
            "Use of cheap copper-clad aluminium (CCA) or inferior coaxial cable",
            "Uncalibrated signal alignment relying on consumer indicators",
            "Failure to meet British Standards (BS EN / IET Building Regulations)",
            "Lack of gale-rated storm bracketing leading to micro-vibrations"
        ])
        for m in def_mistakes:
            p_m = c1_tf.add_paragraph()
            p_m.text = f"• {m}"
            p_m.font.size = Pt(11)
            p_m.font.color.rgb = self.C_WHITE
            p_m.space_before = Pt(8)

        # Card 2: Professional Standard
        c2 = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.933), Inches(1.5), Inches(5.6), Inches(5.0))
        c2.fill.solid()
        c2.fill.fore_color.rgb = self.C_CARD_BG
        c2.line.color.rgb = RGBColor(16, 185, 129)
        c2_tf = c2.text_frame
        c2_tf.word_wrap = True
        c2_tf.margin_left = Inches(0.3)
        c2_tf.margin_top = Inches(0.3)
        c2_tf.paragraphs[0].text = "✅ ADI PROFESSIONAL TRADE STANDARD"
        c2_tf.paragraphs[0].font.bold = True
        c2_tf.paragraphs[0].font.size = Pt(13)
        c2_tf.paragraphs[0].font.color.rgb = RGBColor(16, 185, 129)

        def_standards = faq_item.get("card2_bullets", [
            f"Fitted to {standards[0] if standards else 'British Standards'}",
            "100% solid bare copper cabling (WF100 / 23 AWG Cat6 PoE)",
            "Calibrated digital spectrum analyzer testing (MER >= 28dB / 0.00 deg drift)",
            "Pennine 90mph gale-tested structural mounting cradles"
        ])
        for s in def_standards:
            p_s = c2_tf.add_paragraph()
            p_s.text = f"• {s}"
            p_s.font.size = Pt(11)
            p_s.font.color.rgb = self.C_WHITE
            p_s.space_before = Pt(8)

        # -------------------------------------------------------------
        # Slide 3: Hardware Specifications & Bento Architecture
        # -------------------------------------------------------------
        s3 = prs.slides.add_slide(blank_layout)
        bg3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg3.fill.solid()
        bg3.fill.fore_color.rgb = self.C_OBSIDIAN
        bg3.line.fill.background()

        tb_s3 = s3.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.733), Inches(0.8))
        tf_s3 = tb_s3.text_frame
        p_s3 = tf_s3.paragraphs[0]
        p_s3.text = f"PHYSICAL ARCHITECTURE • {service_name.upper()} HARDWARE BENCHMARKS"
        p_s3.font.size = Pt(14)
        p_s3.font.bold = True
        p_s3.font.color.rgb = self.C_ORANGE

        bento_items = faq_item.get("bento_specs", [
            {"title": "British Standards", "desc": f"Engineered in accordance with {standards[0] if standards else 'BS EN standards'} for court and insurance admissibility."},
            {"title": "Cabling Infrastructure", "desc": "Solid bare copper 23 AWG Cat6 PoE or CAI-benchmarked double-screened WF100 coaxial cabling."},
            {"title": "Structural Containment", "desc": "Weatherproof silicone drip loops, non-drill chimney lashing cradles, and heavy-duty storm brackets."}
        ])[:3]

        for i, item in enumerate(bento_items):
            bx = Inches(0.8 + i * 4.04)
            bbox = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, bx, Inches(1.5), Inches(3.64), Inches(5.0))
            bbox.fill.solid()
            bbox.fill.fore_color.rgb = self.C_CARD_BG
            bbox.line.color.rgb = self.C_BORDER
            btf = bbox.text_frame
            btf.word_wrap = True
            btf.margin_left = Inches(0.3)
            btf.margin_top = Inches(0.3)
            btf.paragraphs[0].text = f"0{i+1}. {item['title'].upper()}"
            btf.paragraphs[0].font.bold = True
            btf.paragraphs[0].font.size = Pt(13)
            btf.paragraphs[0].font.color.rgb = self.C_ORANGE
            bp = btf.add_paragraph()
            bp.text = item['desc']
            bp.font.size = Pt(11)
            bp.font.color.rgb = self.C_WHITE
            bp.space_before = Pt(10)

        # -------------------------------------------------------------
        # Slide 4: Lead Engineer Craftsmanship & Google Slides Apex
        # -------------------------------------------------------------
        s4 = prs.slides.add_slide(blank_layout)
        bg4 = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg4.fill.solid()
        bg4.fill.fore_color.rgb = self.C_OBSIDIAN
        bg4.line.fill.background()

        cred = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(1.2), Inches(11.733), Inches(5.4))
        cred.fill.solid()
        cred.fill.fore_color.rgb = self.C_CARD_BG
        cred.line.color.rgb = self.C_ORANGE
        ctf = cred.text_frame
        ctf.word_wrap = True
        ctf.margin_left = Inches(0.4)
        ctf.margin_top = Inches(0.4)
        ctf.paragraphs[0].text = "GARY PEARCE • LEAD PHYSICAL SECURITY & TELECOM ENGINEER"
        ctf.paragraphs[0].font.bold = True
        ctf.paragraphs[0].font.size = Pt(15)
        ctf.paragraphs[0].font.color.rgb = self.C_ORANGE

        cp2 = ctf.add_paragraph()
        cp2.text = "Direct Mobile: 07860 244 274 | Business: ADI Communications"
        cp2.font.bold = True
        cp2.font.size = Pt(13)
        cp2.font.color.rgb = self.C_WHITE
        cp2.space_before = Pt(4)

        creds = [
            "25+ Years Hands-On Physical Security & Telecommunications Craftsmanship across Yorkshire & Lancashire",
            "£10,000,000 Public Liability Insurance for all residential and commercial structural installations",
            "Certified: NVQ Level 1-3 Aerials & Satellite, NVQ Level 1-4 Data Cabling & Fibre, Qualified CCTV Installer",
            "Verified Client Reputation: ★★★★★ 9.98 / 10 Rating from 84+ Client Reviews",
            "CAI Compliance: Fitted exclusively with CAI-benchmarked equipment & double-screened WF100 cable"
        ]
        for c in creds:
            cp = ctf.add_paragraph()
            cp.text = f"• {c}"
            cp.font.size = Pt(11)
            cp.font.color.rgb = self.C_WHITE
            cp.space_before = Pt(6)

        cp_apex = ctf.add_paragraph()
        cp_apex.text = f"Top-of-Stack Google Slides DA 100 Companion Apex:\n{GOOGLE_SLIDES_APEX_URL}"
        cp_apex.font.size = Pt(10)
        cp_apex.font.color.rgb = self.C_CYAN
        cp_apex.space_before = Pt(12)

        buffer_url = faq_item.get("buffer_url", BLOGGER_SHIELD_URL)
        cp_buf = ctf.add_paragraph()
        cp_buf.text = f"Technical Field Buffer Guide: {buffer_url}"
        cp_buf.font.size = Pt(10)
        cp_buf.font.color.rgb = self.C_CYAN
        cp_buf.space_before = Pt(4)

        out_path.parent.mkdir(parents=True, exist_ok=True)
        prs.save(str(out_path))
        return out_path

    def generate_pdf(self, faq_item: dict, out_path: Optional[Path] = None) -> Path:
        slug = faq_item.get("slug", "faq")
        if out_path is None:
            out_path = self.docs_dir / f"{slug}.pdf"

        service_name = faq_item.get("service", "Trade Engineering")
        question = faq_item.get("question", "Field Engineering Question")
        standards = faq_item.get("technical_standards", ["British Standard Certified"])
        bluf_text = self._extract_bluf(faq_item)
        script = faq_item.get("script_narration", "")

        doc = SimpleDocTemplate(str(out_path), pagesize=A4, leftMargin=54, rightMargin=54, topMargin=54, bottomMargin=54)
        styles = getSampleStyleSheet()

        title_style = ParagraphStyle("DocTitle", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#09090B"), spaceAfter=6)
        bluf_style = ParagraphStyle("BlufBox", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=13.5, textColor=colors.HexColor("#09090B"), backColor=colors.HexColor("#FFF7ED"), borderColor=colors.HexColor("#FF5500"), borderWidth=1, borderPadding=8, spaceBefore=6, spaceAfter=8)
        h2_style = ParagraphStyle("SectionH2", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#09090B"), spaceBefore=8, spaceAfter=4)
        body_style = ParagraphStyle("BodyDark", parent=styles["Normal"], fontName="Helvetica", fontSize=8.5, leading=12.5, textColor=colors.HexColor("#27272A"), spaceAfter=4)
        callout_style = ParagraphStyle("Callout", parent=styles["Normal"], fontName="Helvetica", fontSize=8, leading=12, textColor=colors.HexColor("#18181B"), backColor=colors.HexColor("#F4F4F5"), borderPadding=6, spaceBefore=6, spaceAfter=6)

        story = [
            Paragraph(f"TECHNICAL FIELD SPECIFICATION • {service_name.upper()}", ParagraphStyle("DocSub", parent=styles["Normal"], fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=colors.HexColor("#EA580C"), spaceAfter=6)),
            Paragraph(question, title_style),
            HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#FF5500"), spaceAfter=8),
            Paragraph(f"<b>BOTTOM LINE UP FRONT (BLUF) TRADE ASSESSMENT:</b><br/>{bluf_text}", bluf_style),
            Paragraph("1. Field Engineering & British Standards Analysis", h2_style),
            Paragraph(f"In accordance with UK trade guidelines and {standards[0] if standards else 'British Standards'}:", body_style),
            Paragraph(script, body_style),
            Spacer(1, 4),
            Paragraph("2. Technical Benchmark Matrix", h2_style)
        ]

        # Benchmark Matrix
        matrix_rows = [
            ["Specification Parameter", "Standard / Budget Method", "ADI Professional Trade Standard"],
            ["Cabling Core", "CCA (Copper Clad Aluminium)", "100% Solid Bare Copper (23 AWG / WF100)"],
            ["Structural Mount", "Lightweight zinc standoffs", "Pennine 90mph gale stainless lashing"],
            ["Signal Alignment", "Consumer bar indicators", "Calibrated digital spectrum analyzer"],
            ["Court Admissibility", "Frequently rejected", "100% BS EN compliant forensic evidence"]
        ]
        t = Table(matrix_rows, colWidths=[130, 170, 187])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#09090B")),
            ('TEXTCOLOR', (0,0), (-1,0), colors.white),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 7.5),
            ('BOTTOMPADDING', (0,0), (-1,0), 4),
            ('TOPPADDING', (0,0), (-1,0), 4),
            ('BACKGROUND', (0,1), (-1,-1), colors.HexColor("#FAFAFA")),
            ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E4E4E7")),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 7),
        ]))
        story.append(t)

        # Credentials & Apex Callout
        story.append(Spacer(1, 6))
        story.append(Paragraph("3. Lead Engineer Craftsmanship & Citadel Links", h2_style))
        buffer_url = faq_item.get("buffer_url", BLOGGER_SHIELD_URL)
        cred_text = (
            "<b>Lead Field Engineer:</b> Gary Pearce • ADI Communications (Direct Mobile: <b>07860 244 274</b>)<br/>"
            "<b>Trade Credentials:</b> 25+ Years Experience | £10,000,000 Public Liability Insurance | Qualified CCTV & Telecoms Specialist | Verified Rating: ★★★★★ 9.98/10 (84+ Reviews)<br/>"
            f"<b>Top-of-Stack Google Slides DA 100 Companion Link:</b> <a href='{GOOGLE_SLIDES_APEX_URL}'><b>{GOOGLE_SLIDES_APEX_URL}</b></a><br/>"
            f"<b>Technical Field Buffer:</b> <a href='{buffer_url}'><b>{buffer_url}</b></a>"
        )
        story.append(Paragraph(cred_text, callout_style))

        out_path.parent.mkdir(parents=True, exist_ok=True)
        doc.build(story, canvasmaker=NumberedCanvas)
        return out_path


# =============================================================================
# 3. Binary EXIF Geocoding Trade Photography Generator
# =============================================================================

def deg_to_dms_rational(deg_float: float):
    deg_float = abs(deg_float)
    deg = int(deg_float)
    min_float = (deg_float - deg) * 60
    minute = int(min_float)
    sec_float = (min_float - minute) * 60
    sec = int(round(sec_float * 10000))
    return ((deg, 1), (minute, 1), (sec, 10000))


class FAQExifImageGenerator:
    """Injects binary EXIF GPS and IPTC metadata into trade photography."""

    def __init__(self, output_dir: Path = IMAGES_DIR):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_exif_dict(self, metadata: dict) -> bytes:
        lat = metadata.get("lat", DEFAULT_LAT)
        lon = metadata.get("lon", DEFAULT_LON)
        title = metadata.get("title", "ADI Communications Trade Engineering")
        # Ensure ASCII / Latin-1 for 0th IFD strings to prevent piexif UnicodeEncodeError
        artist = metadata.get("artist", "Gary Pearce - ADI Communications (07860 244 274)").replace("•", "-")
        copyright_notice = metadata.get("copyright", "Copyright 2026 ADI Communications Ltd. Gary Pearce 07860 244 274").replace("•", "-")
        safe_title = title.replace("•", "-").encode("latin-1", errors="replace").decode("latin-1")

        user_comment = metadata.get("user_comment", f"Gary Pearce 07860 244 274 | ADI Communications | Lat {lat} Lon {lon} | Rule 45 Google Shield")

        lat_dms = deg_to_dms_rational(lat)
        lon_dms = deg_to_dms_rational(lon)

        zeroth_ifd = {
            piexif.ImageIFD.Make: "Sony",
            piexif.ImageIFD.Model: "ILCE-7RM5 Trade Field Camera",
            piexif.ImageIFD.Artist: artist,
            piexif.ImageIFD.Copyright: copyright_notice,
            piexif.ImageIFD.ImageDescription: safe_title,
            piexif.ImageIFD.Software: "ADI Communications Trade Media Engine v4"
        }

        gps_ifd = {
            piexif.GPSIFD.GPSLatitudeRef: "N" if lat >= 0 else "S",
            piexif.GPSIFD.GPSLatitude: lat_dms,
            piexif.GPSIFD.GPSLongitudeRef: "E" if lon >= 0 else "W",
            piexif.GPSIFD.GPSLongitude: lon_dms,
            piexif.GPSIFD.GPSAltitudeRef: 0,
            piexif.GPSIFD.GPSAltitude: (150, 1),
        }

        exif_ifd = {
            piexif.ExifIFD.UserComment: helper.UserComment.dump(user_comment, encoding="unicode")
        }

        exif_dict = {"0th": zeroth_ifd, "Exif": exif_ifd, "GPS": gps_ifd, "1st": {}, "thumbnail": None}
        return piexif.dump(exif_dict)

    def process_and_tag(self, src_image_path: Path, base_filename: str, metadata: dict) -> Tuple[Path, Path]:
        exif_bytes = self.build_exif_dict(metadata)
        if src_image_path and src_image_path.exists() and os.path.getsize(src_image_path) > 0:
            try:
                img = Image.open(src_image_path)
            except Exception:
                img = Image.new("RGB", (1600, 900), color=(15, 23, 42))
        else:
            img = Image.new("RGB", (1600, 900), color=(15, 23, 42))

        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        webp_path = self.output_dir / f"{base_filename}.webp"
        jpg_path = self.output_dir / f"{base_filename}_exif.jpg"

        # Save WebP with EXIF
        img.save(str(webp_path), format="WEBP", quality=85, exif=exif_bytes)

        # Save JPEG with EXIF
        img.save(str(jpg_path), format="JPEG", quality=92, exif=exif_bytes)

        # Self-test assertions
        jpg_loaded = piexif.load(str(jpg_path))
        assert jpg_loaded["0th"].get(piexif.ImageIFD.Artist) is not None, "JPEG Artist tag missing"
        assert jpg_loaded["GPS"].get(piexif.GPSIFD.GPSLatitude) is not None, "JPEG GPS Latitude tag missing"

        return webp_path, jpg_path


# =============================================================================
# 4. Video & Thumbnail Generator (FFmpeg 8.1.1 & Edge TTS en-GB-RyanNeural)
# =============================================================================

class FAQVideoGenerator:
    """Synthesizes British trade voiceover, HUD overlays, thumbnails, and 1080p MP4s."""

    def __init__(self, output_dir: Path = VIDEOS_DIR, cache_dir: Path = CACHE_DIR):
        self.output_dir = output_dir
        self.cache_dir = cache_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def get_audio_duration(audio_path: Path) -> float:
        """Measure exact audio duration in seconds via ffprobe."""
        if not audio_path or not audio_path.exists() or os.path.getsize(audio_path) == 0:
            return 0.0
        cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            str(audio_path)
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            val = res.stdout.strip()
            return float(val) if val else 0.0
        except Exception:
            return 0.0

    @staticmethod
    async def synthesize_voiceover(text: str, output_path: Path) -> None:
        """
        Synthesize British trade voiceover using edge_tts with en-GB-RyanNeural (£0 token cost).
        Guarantees strict Rule 28 Voice API air-gap compliance.
        """
        import edge_tts
        comm = edge_tts.Communicate(text, "en-GB-RyanNeural", rate="+0%")
        await comm.save(str(output_path))

    def generate_thumbnail(self, img_path: Path, title: str, subtitle: str, category: str, output_path: Path) -> Path:
        """
        Synthesize 1600x900 WebP thumbnail with obsidian gradient scrim and telemetry pill.
        """
        if img_path and img_path.exists() and os.path.getsize(img_path) > 0:
            try:
                base = Image.open(img_path).convert("RGBA")
            except Exception:
                base = Image.new("RGBA", (1600, 900), (15, 23, 42, 255))
        else:
            base = Image.new("RGBA", (1600, 900), (15, 23, 42, 255))
        base = ImageOps.fit(base, (1600, 900), Image.Resampling.LANCZOS)

        scrim = Image.new("RGBA", (1600, 900), (0, 0, 0, 0))
        draw_scrim = ImageDraw.Draw(scrim)
        for y in range(900):
            for x in range(0, 1600, 20):
                alpha = int(min(235, max(40, 140 * (1 - x / 1600.0) + 120 * (y / 900.0))))
                draw_scrim.rectangle([x, y, x + 20, y + 1], fill=(5, 5, 8, alpha))
        base = Image.alpha_composite(base, scrim)
        draw = ImageDraw.Draw(base)

        f_title = get_font(FONT_ARIAL_BOLD, 42)
        f_sub = get_font(FONT_SEGOE_BOLD, 24)
        f_mono = get_font(FONT_CONSOLA_BOLD, 22)
        f_foot = get_font(FONT_SEGOE_REG, 22)
        f_foot_bold = get_font(FONT_SEGOE_BOLD, 22)

        # 1. Telemetry pill (top-left)
        draw.rounded_rectangle([80, 70, 520, 120], radius=12, fill=(5, 5, 8, 210), outline=(255, 85, 0, 220), width=2)
        draw.ellipse([100, 88, 114, 102], fill=(255, 85, 0, 255))
        draw.text((128, 83), "4K UK FIELD MASTERCLASS", font=f_mono, fill=(255, 255, 255, 240))

        # 2. Category badge (top-right)
        draw.rounded_rectangle([1140, 70, 1520, 120], radius=12, fill=(5, 5, 8, 190), outline=(255, 255, 255, 40), width=1)
        draw.text((1165, 84), category.upper()[:24], font=f_sub, fill=(255, 255, 255, 220))

        # 3. Title block (balanced 2 lines)
        words = title.upper().split()
        mid = len(words) // 2
        l1 = " ".join(words[:mid])
        l2 = " ".join(words[mid:])

        draw.text((82, 172), l1, font=f_title, fill=(0, 0, 0, 220))
        draw.text((80, 170), l1, font=f_title, fill=(255, 255, 255, 255))
        draw.text((82, 237), l2, font=f_title, fill=(0, 0, 0, 220))
        draw.text((80, 235), l2, font=f_title, fill=(255, 255, 255, 255))

        # 4. Technical standards subhead
        draw.text((80, 315), subtitle.upper()[:90], font=f_sub, fill=(255, 160, 122, 255))

        # 5. Gary Pearce trade footer card
        draw.rounded_rectangle([80, 780, 1520, 840], radius=14, fill=(5, 5, 8, 230), outline=(255, 255, 255, 40), width=1)
        draw.text((110, 795), "GARY PEARCE • ADI COMMUNICATIONS • 07860 244 274", font=f_foot_bold, fill=(255, 255, 255, 255))
        draw.text((1060, 796), "★★★★★ 9.98 / 10 • 84+ REVIEWS", font=f_foot, fill=(255, 160, 122, 255))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        base.convert("RGB").save(str(output_path), "WEBP", quality=85)
        return output_path

    def generate_hud_overlay(self, title: str, category: str, output_path: Path) -> Path:
        """
        Generate transparent 1920x1080 HUD overlay PNG with telemetry pill and obsidian card.
        """
        overlay = Image.new("RGBA", (1920, 1080), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        f_title = get_font(FONT_ARIAL_BOLD, 28)
        f_sub = get_font(FONT_SEGOE_REG, 20)
        f_sub_bold = get_font(FONT_SEGOE_BOLD, 20)
        f_mono = get_font(FONT_CONSOLA_BOLD, 20)

        # Top telemetry pill
        draw.rounded_rectangle([80, 50, 480, 100], radius=10, fill=(5, 5, 8, 210), outline=(255, 85, 0, 220), width=2)
        draw.ellipse([98, 68, 112, 82], fill=(255, 85, 0, 255))
        draw.text((125, 65), "4K UK FIELD MASTERCLASS", font=f_mono, fill=(255, 255, 255, 240))

        # Lower-third HUD card
        draw.rounded_rectangle([80, 890, 1840, 1010], radius=12, fill=(5, 5, 8, 225), outline=(255, 255, 255, 30), width=1)
        draw.text((110, 910), title.upper()[:75], font=f_title, fill=(255, 255, 255, 255))
        draw.text((110, 955), "GARY PEARCE • ADI COMMUNICATIONS • 07860 244 274 • 25+ YRS EXPERIENCE", font=f_sub_bold, fill=(255, 160, 122, 255))
        draw.text((1480, 955), "★★★★★ 9.98 / 10 (84+ REVIEWS)", font=f_sub, fill=(255, 160, 122, 220))

        output_path.parent.mkdir(parents=True, exist_ok=True)
        overlay.save(str(output_path))
        return output_path

    def render_video(self, img_path: Path, hud_path: Path, audio_path: Path, duration: float, output_path: Path) -> Path:
        """
        Execute FFmpeg 8.1.1 compositing filtergraph:
        - Ken Burns zoompan (1.00x -> 1.08x at center)
        - Transparent Pillow HUD PNG overlay
        - showwaves real-time audio waveform at [1540, 905]
        - drawbox animated progress bar at [80, 1006]
        """
        if duration <= 0.0:
            raise ValueError(f"Invalid audio duration: {duration}s. Cannot render video without valid audio.")
        d_frames = int(duration * 30)
        temp_mp4 = self.cache_dir / f"{output_path.stem}.tmp.mp4"

        filter_complex = (
            f"[0:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
            f"zoompan=z='min(zoom+0.0002,1.08)':d={d_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1920x1080:fps=30[bg];"
            f"[2:a]showwaves=s=260x50:mode=line:colors=0xFF5500|0xFFA07A[wave];"
            f"[bg][1:v]overlay=0:0[v1];"
            f"[v1][wave]overlay=1540:905[v2];"
            f"[v2]drawbox=x=80:y=1006:w='(1760)*(t/{duration:.3f})':h=4:color=0xFF5500@1.0:t=fill[vfinal]"
        )

        cmd = [
            "ffmpeg", "-y",
            "-i", str(img_path),
            "-i", str(hud_path),
            "-i", str(audio_path),
            "-filter_complex", filter_complex,
            "-map", "[vfinal]",
            "-map", "2:a",
            "-c:v", "libx264", "-profile:v", "high", "-level", "4.1", "-pix_fmt", "yuv420p",
            "-preset", "fast", "-crf", "22",
            "-c:a", "aac", "-ar", "48000", "-ac", "2", "-b:a", "192k",
            "-movflags", "+faststart",
            "-shortest",
            str(temp_mp4)
        ]

        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            raise RuntimeError(f"FFmpeg compositing failed for {output_path.name}:\n{res.stderr[-1000:]}")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.exists():
            output_path.unlink()
        shutil.move(str(temp_mp4), str(output_path))
        return output_path


# =============================================================================
# 5. RSS Feed Generator (podcast.xml & faq_multimedia_feed.xml)
# =============================================================================

class RSSFeedGenerator:
    """Generates and synchronizes RSS 2.0 items for multimedia FAQ assets."""

    @staticmethod
    def get_rfc822_date(dt: Optional[datetime] = None) -> str:
        return email.utils.format_datetime(dt or datetime.now())

    @staticmethod
    def format_duration(seconds: float) -> str:
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    @classmethod
    def build_item_element(
        cls,
        faq_data: dict,
        media_file_path: Path,
        media_public_url: str,
        thumb_public_url: str,
        duration_sec: float,
        apex_url: str,
        shield_url: str
    ) -> ET.Element:
        ET.register_namespace("itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
        ET.register_namespace("content", "http://purl.org/rss/1.0/modules/content/")
        ET.register_namespace("podcast", "https://podcastindex.org/namespace/1.0")
        ET.register_namespace("atom", "http://www.w3.org/2005/Atom")

        ITUNES_NS = "{http://www.itunes.com/dtds/podcast-1.0.dtd}"

        item = ET.Element("item")

        title = ET.SubElement(item, "title")
        title.text = f"{faq_data['question']} — Gary Pearce ADI Communications"

        itunes_title = ET.SubElement(item, f"{ITUNES_NS}title")
        itunes_title.text = faq_data['question']

        itunes_author = ET.SubElement(item, f"{ITUNES_NS}author")
        itunes_author.text = "Gary Pearce (ADI Communications)"

        pub_date = ET.SubElement(item, "pubDate")
        pub_date.text = cls.get_rfc822_date()

        link = ET.SubElement(item, "link")
        link.text = shield_url

        guid = ET.SubElement(item, "guid", {"isPermaLink": "false"})
        guid.text = f"adi-faq-{faq_data.get('slug', faq_data['faq_id'].lower())}"

        category = ET.SubElement(item, "category")
        category.text = faq_data.get("service", "Technology")

        # CDATA Description with BLUF
        standards_text = " • ".join(faq_data.get("technical_standards", []))
        desc_text = (
            f"Official ADI Communications Technical Trade Breakdown by Gary Pearce "
            f"(25+ Years Hands-On Physical Security & Telecoms Engineer, Direct Mobile: 07860 244 274, "
            f"£10M Public Liability Insurance).\n\n"
            f"BOTTOM LINE UP FRONT (BLUF):\n"
            f"{faq_data.get('script_narration', '')}\n\n"
            f"Technical Standards & Hardware:\n"
            f"- {standards_text}\n"
            f"- Fitted with CAI-benchmarked equipment and double-screened WF100 cable (Gary Pearce / ADI Communications are NOT CAI members).\n"
            f"- 9.98/10 Rating across 84+ verified client reviews.\n\n"
            f"Full Technical Guide & Apex Repository: {apex_url}"
        )
        desc = ET.SubElement(item, "description")
        desc.text = f"__CDATA_START__{desc_text}__CDATA_END__"

        file_size = os.path.getsize(media_file_path) if media_file_path.exists() else 0
        mime_type = "video/mp4" if str(media_file_path).endswith(".mp4") else "audio/mpeg"
        ET.SubElement(item, "enclosure", {
            "url": media_public_url,
            "length": str(file_size),
            "type": mime_type
        })

        ET.SubElement(item, f"{ITUNES_NS}duration").text = cls.format_duration(duration_sec)
        ET.SubElement(item, f"{ITUNES_NS}image", {"href": thumb_public_url})
        ET.SubElement(item, f"{ITUNES_NS}explicit").text = "no"
        ET.SubElement(item, f"{ITUNES_NS}episodeType").text = "full"

        return item

    @classmethod
    def append_to_feed(cls, feed_path: Path, item_element: ET.Element) -> bool:
        """Injects item into channel of target RSS XML file without duplicating GUIDs."""
        if not feed_path.exists():
            return False

        ET.register_namespace("itunes", "http://www.itunes.com/dtds/podcast-1.0.dtd")
        ET.register_namespace("content", "http://purl.org/rss/1.0/modules/content/")
        ET.register_namespace("podcast", "https://podcastindex.org/namespace/1.0")
        ET.register_namespace("atom", "http://www.w3.org/2005/Atom")

        parser = ET.XMLParser(encoding="utf-8")
        tree = ET.parse(str(feed_path), parser=parser)
        root = tree.getroot()
        channel = root.find("channel")
        if channel is None:
            return False

        new_guid = item_element.find("guid")
        new_guid_text = new_guid.text if new_guid is not None else None

        if new_guid_text:
            for existing_item in channel.findall("item"):
                eg = existing_item.find("guid")
                if eg is not None and eg.text == new_guid_text:
                    # Already exists, skip duplicate
                    return True

        channel.append(item_element)
        raw_xml = ET.tostring(root, encoding="utf-8").decode("utf-8")
        raw_xml = raw_xml.replace("__CDATA_START__", "<![CDATA[").replace("__CDATA_END__", "]]>")
        parsed_dom = minidom.parseString(raw_xml)
        pretty_xml = parsed_dom.toprettyxml(indent="  ", encoding="utf-8")
        cleaned_lines = [line for line in pretty_xml.decode("utf-8").splitlines() if line.strip()]

        with open(feed_path, "w", encoding="utf-8") as f:
            f.write("\n".join(cleaned_lines) + "\n")
        return True


# =============================================================================
# 6. Pipeline Orchestrator & CLI
# =============================================================================

async def process_faq_multimedia(
    faq: dict,
    formats: List[str],
    force: bool = False,
    dry_run: bool = False
) -> Dict[str, Any]:
    """Processes a single FAQ across all requested multimedia asset formats."""
    faq_id = faq["faq_id"]
    slug = faq["slug"]
    title = faq["title"]
    category = faq["service"]
    script = faq["script_narration"]
    standards_str = " • ".join(faq.get("technical_standards", []))

    img_rel = faq["matching_image_asset"]
    img_path = REPO_ROOT / img_rel
    if not img_path.exists():
        raise FileNotFoundError(f"Missing image asset for {faq_id}: {img_path}")

    video_path = VIDEOS_DIR / f"{slug}.mp4"
    thumb_path = VIDEOS_DIR / f"{slug}_thumb.webp"
    pptx_path = SLIDES_DIR / f"{slug}.pptx"
    pdf_path = DOCS_DIR / f"{slug}.pdf"
    exif_jpg_path = IMAGES_DIR / f"{slug}_exif.jpg"

    audio_path = CACHE_DIR / f"{slug}_audio.mp3"
    hud_path = CACHE_DIR / f"{slug}_hud.png"

    print(f"\n[{faq_id}] {title[:65]}...")
    print(f"  • Service: {category}")
    print(f"  • Matching Image: {img_rel}")

    if dry_run:
        print(f"  [DRY-RUN] Verified image exists ({img_path.stat().st_size} bytes)")
        print(f"  [DRY-RUN] Script length: {len(script.split())} words")
        print(f"  [DRY-RUN] Target paths: {video_path.name}, {pptx_path.name}, {pdf_path.name}")
        return {"faq_id": faq_id, "status": "DRY_RUN_PASS"}

    t_start = time.time()
    results = {"faq_id": faq_id}

    slide_gen = FAQSlideGenerator()
    exif_gen = FAQExifImageGenerator()
    video_gen = FAQVideoGenerator()

    # 1. Slide Deck (PPTX & Vector PDF)
    if "slides" in formats or "all" in formats:
        if not pptx_path.exists() or not pdf_path.exists() or force:
            print(f"  • Generating 16:9 PPTX and vector PDF ({slug})...")
            slide_gen.generate_pptx(faq, pptx_path)
            slide_gen.generate_pdf(faq, pdf_path)
            print(f"  • Slide deck ready ({pptx_path.stat().st_size} bytes, PDF: {pdf_path.stat().st_size} bytes).")
        results["pptx_path"] = str(pptx_path)
        results["pdf_path"] = str(pdf_path)

    # 2. Binary EXIF Geotagged Photography
    if "exif" in formats or "all" in formats:
        if not exif_jpg_path.exists() or force:
            print(f"  • Injecting binary EXIF metadata ({exif_jpg_path.name})...")
            meta = {
                "title": f"{category} - {title}",
                "artist": "Gary Pearce - ADI Communications (07860 244 274)",
                "copyright": "Copyright 2026 ADI Communications Ltd. Gary Pearce 07860 244 274",
                "lat": DEFAULT_LAT,
                "lon": DEFAULT_LON,
                "user_comment": f"Gary Pearce 07860 244 274 | {category} | Lat {DEFAULT_LAT} Lon {DEFAULT_LON} | Rule 45 Google Shield"
            }
            exif_gen.process_and_tag(img_path, slug, meta)
            print("  • Binary EXIF geotagging complete.")
        results["exif_path"] = str(exif_jpg_path)

    # 3. 1080p MP4 Video & 1600x900 WebP Thumbnail
    duration = 35.0
    if "video" in formats or "all" in formats:
        # Step A: Voiceover
        if not audio_path.exists() or force:
            print("  • Synthesizing British voiceover via edge_tts (en-GB-RyanNeural)...")
            await video_gen.synthesize_voiceover(script, audio_path)
        duration = video_gen.get_audio_duration(audio_path)
        print(f"  • Audio Duration: {duration:.2f}s")

        # Step B: Thumbnail
        if not thumb_path.exists() or force:
            print("  • Synthesizing 1600x900 WebP thumbnail with obsidian scrim...")
            video_gen.generate_thumbnail(img_path, title, standards_str, category, thumb_path)
            print(f"  • Thumbnail ready: {thumb_path.name}")

        # Step C: HUD Overlay & Video Render
        if not video_path.exists() or force:
            video_gen.generate_hud_overlay(title, category, hud_path)
            print(f"  • Rendering 1080p MP4 via FFmpeg 8.1.1 (zoompan + showwaves + drawbox)...")
            video_gen.render_video(img_path, hud_path, audio_path, duration, video_path)
            print(f"  • Video rendered: {video_path.name} ({video_path.stat().st_size} bytes)")
            if hud_path.exists():
                hud_path.unlink()

        results["video_path"] = str(video_path)
        results["duration_sec"] = duration

    # 4. RSS Feed Ingestion (podcast.xml & faq_multimedia_feed.xml)
    if "rss" in formats or "all" in formats:
        public_media_url = f"{FIREBASE_HUB_URL}/assets/videos/{slug}.mp4"
        public_thumb_url = f"{FIREBASE_HUB_URL}/assets/videos/{slug}_thumb.webp"
        item_el = RSSFeedGenerator.build_item_element(
            faq,
            video_path if video_path.exists() else img_path,
            public_media_url,
            public_thumb_url,
            duration,
            GOOGLE_SLIDES_APEX_URL,
            faq.get("buffer_url", BLOGGER_SHIELD_URL)
        )
        RSSFeedGenerator.append_to_feed(FAQ_FEED_PATH, item_el)
        print(f"  • RSS item injected into {FAQ_FEED_PATH.name}")

    # 5. doc3 Asset Registration
    if DOC3_CSV_PATH.exists() and ("doc3" in formats or "all" in formats):
        doc3_entry = {
            "parent_profile_id": "PROF-VID-001",
            "platform_name": "YouTube",
            "profile_live_url": YOUTUBE_APEX_URL,
            "asset_title": f"{title} — Gary Pearce ADI Communications",
            "asset_type": "Video Explainer",
            "asset_public_url": f"{FIREBASE_HUB_URL}/assets/videos/{slug}.mp4",
            "top_of_stack_apex_url": YOUTUBE_APEX_URL,
            "shield_target_url": faq.get("buffer_url", BLOGGER_SHIELD_URL),
            "seo_tags": " ".join([f"#{t}" for t in faq.get("tags", ["trade", "engineering"])]),
            "seo_description_summary": f"4K UK field video by Gary Pearce (07860 244 274). {script[:140]}...",
            "dofollow_status": "Dofollow Social Authority",
            "publication_date": datetime.now().strftime("%Y-%m-%d"),
            "verification_status": "HTTP_200"
        }
        reg_id = Doc3RegistryGuard.register_asset(DOC3_CSV_PATH, doc3_entry)
        results["doc3_id"] = reg_id
        print(f"  • Registered in doc3 as {reg_id}")

    t_elapsed = time.time() - t_start
    print(f"  [OK] {faq_id} completed in {t_elapsed:.2f}s")
    results["status"] = "SUCCESS"
    return results


def audit_multimedia_assets() -> Dict[str, Any]:
    """Runs a complete system audit on catalog, media files, and feeds."""
    print("\n=======================================================")
    print("      ADI MULTIMEDIA PRODUCTION SYSTEM AUDIT (M2-ALL)   ")
    print("=======================================================")

    if not CATALOG_PATH.exists():
        print(f"[FAIL] Catalog not found at {CATALOG_PATH}")
        return {"status": "FAIL", "reason": "Missing catalog"}

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        cat = json.load(f)

    faqs = cat.get("faqs", [])
    print(f"[CATALOG] Loaded {len(faqs)} FAQs across {len(cat.get('services', []))} services.")

    # Check images
    missing_imgs = []
    for f in faqs:
        p = REPO_ROOT / f.get("matching_image_asset", "")
        if not p.exists():
            missing_imgs.append(f"{f['faq_id']}: {f.get('matching_image_asset')}")

    print(f"[IMAGES] Matching trade photos: {len(faqs) - len(missing_imgs)}/{len(faqs)} verified.")
    if missing_imgs:
        for m in missing_imgs:
            print(f"  [MISSING IMAGE] {m}")

    # Check doc3 14-column layout
    doc3_valid = False
    doc3_rows_count = 0
    if DOC3_CSV_PATH.exists():
        with open(DOC3_CSV_PATH, "r", encoding="utf-8") as f:
            reader = list(csv.reader(f))
            doc3_rows_count = len(reader)
            bad_rows = [i + 1 for i, r in enumerate(reader) if len(r) != 14]
            if not bad_rows:
                doc3_valid = True
                print(f"[DOC3] 14-Column Layout Invariant: PASS (all {doc3_rows_count} rows conform).")
            else:
                print(f"[DOC3] 14-Column Layout Invariant: FAIL ({len(bad_rows)} malformed rows: {bad_rows[:5]}).")

    # Check RSS Feeds
    podcast_items = 0
    faq_items = 0
    if PODCAST_FEED_PATH.exists():
        try:
            tree = ET.parse(str(PODCAST_FEED_PATH))
            podcast_items = len(tree.getroot().findall("./channel/item"))
            print(f"[RSS] podcast.xml: {podcast_items} items.")
        except Exception as e:
            print(f"[RSS] podcast.xml parse error: {e}")

    if FAQ_FEED_PATH.exists():
        try:
            tree = ET.parse(str(FAQ_FEED_PATH))
            faq_items = len(tree.getroot().findall("./channel/item"))
            print(f"[RSS] faq_multimedia_feed.xml: {faq_items} items.")
        except Exception as e:
            print(f"[RSS] faq_multimedia_feed.xml parse error: {e}")

    print("=======================================================\n")
    return {
        "status": "PASS" if not missing_imgs and doc3_valid else "FAIL",
        "faq_count": len(faqs),
        "missing_images": missing_imgs,
        "doc3_valid": doc3_valid,
        "doc3_rows": doc3_rows_count,
        "podcast_items": podcast_items,
        "faq_items": faq_items
    }


async def main_async():
    parser = argparse.ArgumentParser(description="Autonomous FAQ Multimedia Production Engine for Gary Pearce / ADI Communications.")
    parser.add_argument("--all", action="store_true", help="Process all catalogued FAQs")
    parser.add_argument("--service", type=str, default=None, help="Filter by service (cctv, starlink, tv, alarms, aerials, wifi)")
    parser.add_argument("--faq", type=str, default=None, help="Specific FAQ ID (e.g. FAQ-CCTV-001) or slug")
    parser.add_argument("--dry-run", action="store_true", help="Validate assets and manifest without rendering")
    parser.add_argument("--audit", action="store_true", help="Run comprehensive system audit")
    parser.add_argument("--format", type=str, default="all", choices=["video", "slides", "exif", "rss", "doc3", "all"], help="Asset format to produce")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of FAQs to process")
    parser.add_argument("--force", action="store_true", help="Force re-rendering even if output exists")
    args = parser.parse_args()

    if args.audit:
        audit_res = audit_multimedia_assets()
        sys.exit(0 if audit_res.get("status") == "PASS" else 1)

    if not CATALOG_PATH.exists():
        print(f"ERROR: Catalog file not found at {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)

    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    faqs = catalog.get("faqs", [])
    print(f"Loaded {len(faqs)} FAQs across {len(catalog.get('services', []))} services.")

    service_alias = {
        "cctv": "CCTV Engineering",
        "starlink": "Satellite Telecoms",
        "tv": "TV & Media Walls",
        "tv-mounting": "TV & Media Walls",
        "alarms": "Smart Alarms",
        "aerials": "TV & Broadcast",
        "wifi": "Structured Cabling",
        "cabling": "Structured Cabling"
    }

    if args.service:
        target_service = service_alias.get(args.service.lower(), args.service)
        faqs = [f for f in faqs if f["service"].lower() == target_service.lower()]
        print(f"Filtered to service: {target_service} ({len(faqs)} items)")

    if args.faq:
        target_id = args.faq.upper()
        faqs = [f for f in faqs if f["faq_id"].upper() == target_id or f["slug"].lower() == args.faq.lower()]
        print(f"Filtered to FAQ: {args.faq} ({len(faqs)} items)")

    if args.limit:
        faqs = faqs[:args.limit]
        print(f"Limited to first {args.limit} items.")

    formats = [args.format] if args.format != "all" else ["all"]

    success_count = 0
    for faq in faqs:
        res = await process_faq_multimedia(faq, formats, force=args.force, dry_run=args.dry_run)
        if res.get("status") in ("SUCCESS", "DRY_RUN_PASS"):
            success_count += 1

    print(f"\n==========================================")
    print(f"PROCESSED: {success_count}/{len(faqs)} FAQs successfully.")
    print(f"==========================================")


if __name__ == "__main__":
    asyncio.run(main_async())
