import json
import os

registry = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "version": "1.0.0",
    "last_updated": "2026-10-22T09:06:00+01:00",
    "title": "ADI Communications & Gary Pearce — Master 10-Stack Multi-Platform Architecture Registry",
    "description": "Comprehensive registry of 60 platforms across 10 specialized stacking layers: PDFs, presentations, public datasets, interactive tools, code, audio, GIS maps, MCP hosts, syndication, and autonomous agents.",
    "classification_standard": {
        "public_asset": "Raw document, dataset, slide deck, or media file accessible via direct URL.",
        "public_page_with_link": "Hosted HTML/viewer webpage where readers can click through to a Google Shield property.",
        "seo_value": "Entity co-citation, PageRank pass-through, and Google indexing authority."
    },
    "rule_45_shield_anchors": {
        "primary_blogger_da99": "https://tvandhomesecurity.blogspot.com/",
        "google_drive_vault_da100": "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
        "youtube_verified_channel": "https://www.youtube.com/@CCTV.services",
        "firebase_app_hub": "https://gary-pearce-forensic-hub.web.app/",
        "buffer_posts": {
            "starlink_chimney_apex": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/",
            "ajax_wireless_alarm": "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/",
            "ethernet_upstairs": "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/",
            "tv_above_fireplace": "https://adicommunications.co.uk/news/tv-above-fireplace-safe-installation/"
        }
    },
    "stacks": []
}

raw_stacks = [
    # Stack 1: PDF & Document Stacking (1-9)
    (1, "Stack 1: PDF & Document Stacking", "Simplebooklet", "https://simplebooklet.com", "Upload API & MCP Workflow", "API Key", "Public Flipbook Page", "Permanent", "primary_blogger_da99", "Interactive 3D page-turning flipbook with clickable links"),
    (2, "Stack 1: PDF & Document Stacking", "Internet Archive Documents", "https://archive.org", "S3-Compatible Upload API", "IAS3 Keys", "Permanent Public Item Page", "Permanent", "primary_blogger_da99", "Historical trade engineering manual archive with Dublin Core XML (DA 96)"),
    (3, "Stack 1: PDF & Document Stacking", "Google Drive PDF Vault", "https://drive.google.com", "Google Drive API v3", "Google OAuth", "Public PDF Viewer (DA 100)", "Permanent", "primary_blogger_da99", "Folder 1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88 hosting downloadable whitepapers"),
    (4, "Stack 1: PDF & Document Stacking", "Scribd", "https://scribd.com", "Web / API Upload", "Account", "Public Document Page", "Permanent", "primary_blogger_da99", "High-DA document discovery platform indexing technical installation manuals"),
    (5, "Stack 1: PDF & Document Stacking", "Issuu", "https://issuu.com", "Publishing API", "API Key", "Digital Publication Reader", "Permanent", "primary_blogger_da99", "Magazine-style digital brochures and homeowner security guides"),
    (6, "Stack 1: PDF & Document Stacking", "Calaméo", "https://calameo.com", "Calaméo API", "API Key", "Interactive Publication", "Permanent", "primary_blogger_da99", "Digital publishing platform for technical specifications and field reports"),
    (7, "Stack 1: PDF & Document Stacking", "Stirling-PDF Self-Hosted", "https://github.com/Stirling-Tools/Stirling-PDF", "Docker / REST API", "Localhost", "Local PDF Transcoding Engine", "Permanent", "firebase_app_hub", "Self-hosted Docker toolchain to merge, OCR, and sanitize trade PDFs"),
    (8, "Stack 1: PDF & Document Stacking", "GigaPDF Engine", "https://gigapdf.com", "REST API", "API Key", "Headless PDF Generation", "Permanent", "firebase_app_hub", "High-speed programmatic PDF generation from HTML/Markdown templates"),
    (9, "Stack 1: PDF & Document Stacking", "Blocpress", "https://blocpress.com", "HTTP API", "API Key", "Template Document Engine", "Permanent", "firebase_app_hub", "Template-driven document compiler for customized client estimates"),

    # Stack 2: Presentation Stacking (10-12)
    (10, "Stack 2: Presentation Stacking", "Google Slides", "https://slides.google.com", "Google Slides API", "Google OAuth", "Public 16:9 Presentation Deck", "Permanent", "primary_blogger_da99", "Interactive slide decks with embedded obstacle diagrams and cable schematics"),
    (11, "Stack 2: Presentation Stacking", "SlideShare", "https://slideshare.net", "Web / Slide Upload", "Account", "Public Presentation Page", "Permanent", "primary_blogger_da99", "Educational slide decks on UK satellite rigging and RF jammer mitigation"),
    (12, "Stack 2: Presentation Stacking", "Speaker Deck", "https://speakerdeck.com", "PDF Presentation Upload", "GitHub", "Public PDF Slide Deck", "Permanent", "primary_blogger_da99", "Clean developer-friendly presentation platform with high SEO authority"),

    # Stack 3: Data, Charts & Infographics (13-20)
    (13, "Stack 3: Data, Charts & Infographics", "Tableau Public", "https://public.tableau.com", "Tableau Desktop / Web", "Account", "Public Interactive Dashboard", "Permanent", "primary_blogger_da99", "Interactive Yorkshire & Lancashire crime telemetry and camera placement heatmaps"),
    (14, "Stack 3: Data, Charts & Infographics", "Flourish Studio", "https://flourish.studio", "Web / Embed", "Account", "Animated Comparison Story", "Permanent", "primary_blogger_da99", "Dynamic race charts comparing Starlink vs 4G/5G and Fibre speeds over 12 months"),
    (15, "Stack 3: Data, Charts & Infographics", "Observable HQ", "https://observablehq.com", "Notebook API", "GitHub", "Interactive D3.js Graphs", "Permanent", "primary_blogger_da99", "D3.js vector visualizations for wind shear forces and DORI pixel densities"),
    (16, "Stack 3: Data, Charts & Infographics", "Datawrapper", "https://datawrapper.de", "Datawrapper API", "API Key", "Responsive Interactive Charts", "Permanent", "primary_blogger_da99", "Mobile-optimized responsive tables and choropleth maps of UK crime rates"),
    (17, "Stack 3: Data, Charts & Infographics", "RAWGraphs", "https://rawgraphs.io", "Open-Source Web", "Client-Side", "SVG Vector Diagram Generator", "Permanent", "firebase_app_hub", "Alluvial and Voronoi diagram generator for complex security sensor zones"),
    (18, "Stack 3: Data, Charts & Infographics", "Google Sheets Public Data", "https://sheets.google.com", "Google Sheets API", "Google OAuth", "Public CSV / HTML Table (DA 100)", "Permanent", "primary_blogger_da99", "Live synchronizing database of camera models, DORI distances, and wattage"),
    (19, "Stack 3: Data, Charts & Infographics", "Looker Studio", "https://lookerstudio.google.com", "Google Analytics / BigQuery", "Google OAuth", "Public BI Dashboard", "Permanent", "primary_blogger_da99", "Executive security audit dashboard tracking Yorkshire crime incident telemetry"),
    (20, "Stack 3: Data, Charts & Infographics", "Kaggle Datasets", "https://kaggle.com/datasets", "Kaggle CLI / API", "Google OAuth", "Public Research Dataset", "Permanent", "primary_blogger_da99", "Open UK Police recorded crime and CCTV coverage dataset for data science research"),

    # Stack 4: Interactive Tools & Apps (21-26)
    (21, "Stack 4: Interactive Tools & Apps", "Firebase Hosting Edge", "https://firebase.google.com", "Firebase CLI", "Google OAuth", "High-Speed Tool Suite (DA 100)", "Permanent", "primary_blogger_da99", "Hosts all 12 forensic engineering calculators on gary-pearce-forensic-hub.web.app"),
    (22, "Stack 4: Interactive Tools & Apps", "GitHub Pages Tools", "https://pages.github.com", "Git Push", "GitHub", "Open-Source Diagnostic Hub", "Permanent", "primary_blogger_da99", "Standalone client diagnostic tools on gazpearce.github.io/cctv-security-hub"),
    (23, "Stack 4: Interactive Tools & Apps", "Vercel Edge Tools", "https://vercel.com", "Vercel CLI / Git", "GitHub/Google", "Edge Application Mirror", "Permanent", "firebase_app_hub", "Serverless Vite/React diagnostics with instant preview deployments"),
    (24, "Stack 4: Interactive Tools & Apps", "Netlify Static Hub", "https://netlify.com", "Netlify CLI / Git", "GitHub/Google", "Static Tool Mirror", "Permanent", "firebase_app_hub", "Static diagnostic calculators with edge redirect rules and headers"),
    (25, "Stack 4: Interactive Tools & Apps", "Render Services", "https://render.com", "Git Deploy", "GitHub/GitLab", "Static Web Service", "Permanent", "firebase_app_hub", "Automated git-driven static web app mirror"),
    (26, "Stack 4: Interactive Tools & Apps", "Hugging Face Gradio Spaces", "https://huggingface.co/spaces", "Git / Python", "HF Token", "Interactive AI Diagnostic Tool", "Permanent", "primary_blogger_da99", "Gradio space calculating DORI lens angles and Pennine storm wind resistance"),

    # Stack 5: Code & Developer Resources (27-32)
    (27, "Stack 5: Code & Developer Resources", "GitHub Repository", "https://github.com", "Git / REST API", "GitHub OAuth", "Public Code Repository (DA 96)", "Permanent", "primary_blogger_da99", "Primary repository gazpearce/cctv-security-hub with full open-source tools"),
    (28, "Stack 5: Code & Developer Resources", "GitLab Mirror", "https://gitlab.com", "Git / CI Runner", "GitLab OAuth", "Continuous Mirror & CI/CD", "Permanent", "primary_blogger_da99", "Independent European mirror aiagent1510/cctv-security-hub"),
    (29, "Stack 5: Code & Developer Resources", "Codeberg Pages", "https://codeberg.org", "Git Push", "Codeberg", "FOSS Git Authority Node", "Permanent", "primary_blogger_da99", "Non-profit open-source git platform hosted under strict European privacy laws"),
    (30, "Stack 5: Code & Developer Resources", "Read the Docs", "https://readthedocs.org", "Webhook / Git", "GitHub/GitLab", "Versioned Engineering Manual", "Permanent", "primary_blogger_da99", "Sphinx/MkDocs automated technical manual builds for physical security hardware"),
    (31, "Stack 5: Code & Developer Resources", "Docusaurus Hub", "https://docusaurus.io", "Static Build", "Node / Git", "Searchable Technical Library", "Permanent", "primary_blogger_da99", "Modern React documentation framework hosting full equipment specifications"),
    (32, "Stack 5: Code & Developer Resources", "MkDocs Material", "https://squidfunk.github.io/mkdocs-material/", "Static Build", "Python / Git", "Responsive Manual with Lightbox", "Permanent", "primary_blogger_da99", "Python-powered trade documentation with syntax highlighting and schema tables"),

    # Stack 6: Audio, Podcasts & Transcripts (33-38)
    (33, "Stack 6: Audio, Podcasts & Transcripts", "YouTube Podcasts", "https://podcasts.google.com", "YouTube Studio / RSS", "Google OAuth", "Google Search Podcast Carousels", "Permanent", "primary_blogger_da99", "Official show on Channel UCt7VpJGmZZ12hdg2sCgjQag with timestamped Key Moments"),
    (34, "Stack 6: Audio, Podcasts & Transcripts", "Spotify for Creators", "https://creators.spotify.com", "Spotify Podcasters API", "Spotify Account", "Global Spotify Show Page", "Permanent", "primary_blogger_da99", "Global audio entity distribution streaming technical audio debriefs"),
    (35, "Stack 6: Audio, Podcasts & Transcripts", "SoundCloud Waveforms", "https://soundcloud.com", "REST API", "OAuth 2.0", "Embeddable Audio Waveform", "Permanent", "primary_blogger_da99", "Embeddable audio waveforms for quick website engineering briefings"),
    (36, "Stack 6: Audio, Podcasts & Transcripts", "Podbean RSS Hub", "https://podbean.com", "Podbean API / RSS", "Account", "Public Podcast Feed Page", "Permanent", "primary_blogger_da99", "Automated distribution feed syndicating to Apple Podcasts and Amazon Music"),
    (37, "Stack 6: Audio, Podcasts & Transcripts", "Apple Podcasts Show", "https://podcasts.apple.com", "Podbean RSS Ingest", "Apple ID", "Apple Podcasts Show Page", "Permanent", "primary_blogger_da99", "Tier-1 audio directory footprint establishing high entity trust"),
    (38, "Stack 6: Audio, Podcasts & Transcripts", "Internet Archive Audio", "https://archive.org", "S3 API / CLI", "IAS3 Keys", "Permanent Audio Item Page", "Permanent", "primary_blogger_da99", "Lossless audio archive with full transcripts and technical show notes"),

    # Stack 7: Maps, Local Resources & Community Nodes (39-44)
    (39, "Stack 7: Maps & Community Nodes", "Google My Maps", "https://mymaps.google.com", "Google Maps Platform", "Google OAuth", "Custom Interactive Map Embed", "Permanent", "primary_blogger_da99", "Custom map pins showing Gary Pearce's verified trade installations across Yorkshire"),
    (40, "Stack 7: Maps & Community Nodes", "OpenStreetMap Nodes", "https://openstreetmap.org", "OSM API / Nominatim", "OSM Account", "Open Geographic Infrastructure", "Permanent", "primary_blogger_da99", "Boundary and geocoding verification for outward postcodes LS, BD, WF, HD, HX"),
    (41, "Stack 7: Maps & Community Nodes", "Wikimedia Commons Diagrams", "https://commons.wikimedia.org", "MediaWiki Bot", "Account", "Public Domain Diagram Attribution", "Permanent", "primary_blogger_da99", "Highest authority public domain entity reference for CCTV and optical cable math"),
    (42, "Stack 7: Maps & Community Nodes", "Pinterest Visual Guides", "https://pinterest.com", "Pinterest REST API v5", "OAuth 2.0", "Public Visual Pin & Board", "Permanent", "buffer_posts.starlink_chimney_apex", "High-authority visual Pins linking to specific /news/ buffer guides"),
    (43, "Stack 7: Maps & Community Nodes", "Flickr Geotagged Proof", "https://flickr.com", "Flickr Upload API", "OAuth 1.0a", "Geotagged Photo Page", "Permanent", "primary_blogger_da99", "Photo pages with Yorkshire/Lancashire coordinates and camera EXIF data"),
    (44, "Stack 7: Maps & Community Nodes", "Dev.to Technical Tutorials", "https://dev.to", "Dev.to REST API", "API Key", "Public Technical Article", "Permanent", "primary_blogger_da99", "Developer whitepapers with image embeds and source links to Google Shield"),

    # Stack 8: Agent-Friendly File & MCP Hosts (45-48)
    (45, "Stack 8: Agent-Friendly MCP Hosts", "X02 MCP Server", "https://x02.me", "https://up.x02.me/mcp", "MCP / API", "Subdomain File & Tool Hub", "Permanent (5GB)", "primary_blogger_da99", "Advertises native Model Context Protocol (MCP) server for direct agent uploads"),
    (46, "Stack 8: Agent-Friendly MCP Hosts", "beacon.host API", "https://beacon.host", "File Upload API", "API Key", "Shareable File & HTML Page", "Permanent", "primary_blogger_da99", "Direct and multi-step file upload API for HTML reports and PDFs"),
    (47, "Stack 8: Agent-Friendly MCP Hosts", "NudgeHost", "https://www.nudgehost.com", "Upload API", "Account", "Shareable PDF & HTML Links", "Permanent", "primary_blogger_da99", "API for uploading PDFs and receiving stable shareable URLs"),
    (48, "Stack 8: Agent-Friendly MCP Hosts", "Catbox.moe", "https://catbox.moe", "https://catbox.moe/user/api.php", "Anonymous / Userhash", "Direct Permanent File URL", "Permanent (200MB)", "firebase_app_hub", "100% free unauthenticated file/document upload API"),

    # Stack 9: Syndication Feeds & Newsletters (49-53)
    (49, "Stack 9: Syndication Feeds", "Substack Newsletter", "https://substack.com", "Web / Email", "Account", "Public Newsletter Article", "Permanent", "primary_blogger_da99", "Dedicated trade newsletter featuring Yorkshire telecom and security case studies"),
    (50, "Stack 9: Syndication Feeds", "Blogger Feed & API", "https://blogger.com", "Blogger API v3", "Google OAuth", "Atom & RSS Syndicate Feed", "Permanent", "buffer_posts.ethernet_upstairs", "Automated XML syndication feed powering third-party content aggregators"),
    (51, "Stack 9: Syndication Feeds", "RSSHub Feed Engine", "https://github.com/DIYgod/RSSHub", "RSSHub Router", "Localhost", "Multi-Source RSS Generator", "Permanent", "primary_blogger_da99", "Generates clean RSS/Atom feeds from social channels, blogs, and repos"),
    (52, "Stack 9: Syndication Feeds", "Medium Partner Stories", "https://medium.com", "Web Editor", "Google OAuth", "High-DA Story Page", "Permanent", "primary_blogger_da99", "Selected engineering essays with canonical link options back to Google Shield"),
    (53, "Stack 9: Syndication Feeds", "Hashnode Engineering Blog", "https://hashnode.com", "GraphQL API", "PAT", "Developer Article Page", "Permanent", "primary_blogger_da99", "Technical articles with embedded trade photography and canonical links"),

    # Stack 10: Master Orchestration Agents (54-60)
    (54, "Stack 10: Master Orchestration Agents", "Local n8n Workflow Engine", "https://n8n.io", "Self-Hosted on Docker", "Localhost", "Central Orchestration Bus", "Permanent", "firebase_app_hub", "Orchestrates multi-stack triggers, metadata formatting, and multi-API dispatch"),
    (55, "Stack 10: Master Orchestration Agents", "Google Drive API Agent", "https://developers.google.com/drive", "Google SDK / REST", "Google OAuth", "Document Vault Ingest", "Permanent", "primary_blogger_da99", "Uploads, manages permissions, and extracts public CDN links for Google Drive"),
    (56, "Stack 10: Master Orchestration Agents", "Blogger API Agent", "https://developers.google.com/blogger", "Blogger API v3", "Google OAuth", "Article Publisher", "Permanent", "primary_blogger_da99", "Publishes long-form field guides and embeds interactive calculators on DA 99 hub"),
    (57, "Stack 10: Master Orchestration Agents", "Google Slides API Agent", "https://developers.google.com/slides", "Google SDK / REST", "Google OAuth", "Presentation Deck Builder", "Permanent", "primary_blogger_da99", "Generates 16:9 engineering presentation decks programmatically"),
    (58, "Stack 10: Master Orchestration Agents", "Google Sheets API Agent", "https://developers.google.com/sheets", "Google SDK / REST", "Google OAuth", "Telemetry & Audit Ledger", "Permanent", "primary_blogger_da99", "Stores publication URLs, HTTP status codes, and link audit ledgers"),
    (59, "Stack 10: Master Orchestration Agents", "GitHub Actions CI/CD Agent", "https://github.com/features/actions", "GitHub Actions", "GitHub Token", "Automated Build & Deploy", "Permanent", "firebase_app_hub", "Automated QC audits, PDF generation, and multi-cloud sync on git push"),
    (60, "Stack 10: Master Orchestration Agents", "Telegram Dispatch Agent", "https://telegram.org", "Telegram Bot API", "Bot Token", "Instant Trade Mobile Dispatch", "Permanent", "firebase_app_hub", "Instant notifications sent to Gary Pearce (07860 244 274) on task completion")
]

for p in raw_stacks:
    registry["stacks"].append({
        "id": p[0],
        "layer_name": p[1],
        "platform_name": p[2],
        "canonical_url": p[3],
        "api_endpoint_or_method": p[4],
        "auth_type": p[5],
        "capability_type": p[6],
        "retention_policy": p[7],
        "google_shield_anchor": p[8],
        "engineering_notes": p[9]
    })

target_file = r"C:\Users\Gary\github-cctv-seo\multi_stack_master_registry.json"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {target_file}")
print(f"Total Stacking Platforms Registered: {len(registry['stacks'])}")
