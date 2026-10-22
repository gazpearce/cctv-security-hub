import json
import os

manifest = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "version": "2.0.0",
    "last_updated": "2026-10-22T08:55:00+01:00",
    "title": "ADI Communications & Gary Pearce — Master Multi-Cloud Profile Manifest",
    "description": "Standardized branding, credentials, visual CDN assets, and Rule 45 Google Shield link graphs for all 135 free cloud platforms across 5 architectural layers.",
    "brand_standards": {
        "engineer": "Gary Pearce",
        "business": "ADI Communications",
        "telephone": "07860 244 274",
        "international_telephone": "+44 7860 244 274",
        "email": "aiagent1510@gmail.com",
        "location": "Birstall, Batley, West Yorkshire, UK",
        "headquarters_geo": {
            "latitude": 53.7335,
            "longitude": -1.6628,
            "locality": "Birstall",
            "region": "West Yorkshire",
            "country": "GB",
            "postal_code": "WF17 9PB"
        },
        "coverage_districts": [
            "LS (Leeds)", "BD (Bradford)", "HD (Huddersfield)", "HX (Halifax)",
            "WF (Wakefield)", "S (Sheffield)", "DN (Doncaster)", "HU (Hull)",
            "YO (York)", "BB (Blackburn)", "OL (Oldham)"
        ],
        "credentials": {
            "experience_years": 25,
            "public_liability_insurance": "£10,000,000",
            "nvq_qualifications": [
                "NVQ Level 1-3 Aerials & Satellite Infrastructure",
                "NVQ Level 1-4 Data Cabling & Fibre Optics",
                "NVQ Level 1-3 Electrical Standards",
                "Qualified CCTV & Physical Security Installer"
            ],
            "cai_compliance_notice": "Uses CAI-benchmarked equipment and double-screened WF100 coaxial cable. Gary Pearce / ADI Communications are NOT CAI members.",
            "verified_rating": "9.98 / 10 across 84+ verified client reviews"
        }
    },
    "standard_bios": {
        "short_bio_160": "Gary Pearce: 25+ yr Yorkshire telecom & physical security engineer. Starlink 90mph mounts, Ajax alarms, 4K CCTV & Cat6 cabling. 07860 244 274.",
        "medium_bio_500": "Gary Pearce is the lead physical security and telecoms infrastructure engineer at ADI Communications (07860 244 274). With 25+ years hands-on experience and £10M Public Liability insurance, Gary delivers forensic-grade installations across Yorkshire and Lancashire: SpaceX Starlink non-drill chimney mounts, Grade 2 Ajax smart security, Hikvision ColorVu 4K CCTV, external UV-resistant Cat6 data runs, and Corefix TV wall mounting.",
        "long_bio_markdown": "# Gary Pearce — Lead Physical Security & Telecoms Infrastructure Engineer\n**Founder, ADI Communications** • Direct Mobile: `07860 244 274` • West Yorkshire, UK\n\nWith over 25 years of continuous hands-on trade craftsmanship, Gary Pearce designs and installs high-reliability electronic security, satellite broadband, and domestic data infrastructure across Yorkshire, Lancashire, and Greater Manchester.\n\n### Core Engineering Disciplines:\n* **SpaceX Starlink Satellite Rigging**: 90mph Pennine gale-rated non-drill chimney lashing cradles, gable apex standoffs, and whole-home Wi-Fi 7 router bypass integration.\n* **Intruder Alarms & Physical Security**: Grade 2/3 BS EN 50131 Ajax Jeweller wireless security systems, dual-SIM cellular failover, and MotionCam outdoor photo-on-demand detection.\n* **Commercial & Domestic 4K CCTV**: Hikvision ColorVu low-light aperture cameras, 16MP panoramic dual-lens systems, unjammable hardwired PoE infrastructure, and Police evidence formatting.\n* **Structured Data Cabling & Networking**: External UV-rated Cat6 cavity wall drops with downward drip loops, 10-inch SOHO patch cabinets, Fluke DSX-8000 certification, and 5GHz/60GHz gigabit garden office wireless bridges.\n* **Architectural TV Wall Mounting**: Corefix dot-and-dab masonry anchoring, Samsung The Frame flush mounting, and thermal safety calculation above wood-burning fireplaces.\n\n### Verified Credentials:\n* £10,000,000 Public Liability Insurance Coverage\n* NVQ Level 1–4 Data Cabling, Fibre Optics & Electrical Standards\n* CAI-Benchmarked Materials & High-Screening WF100 Coaxial Cable\n* 9.98 / 10 Customer Rating across 84+ Verified Client Reviews"
    },
    "visual_cdn_assets": {
        "avatar_square": "https://cdn.jsdelivr.net/gh/gazpearce/cctv-security-hub@master/assets/images/cat6-fluke-dsx-8000-cable-certification-telemetry.webp",
        "avatar_github_raw": "https://raw.githubusercontent.com/gazpearce/cctv-security-hub/master/assets/images/cat6-fluke-dsx-8000-cable-certification-telemetry.webp",
        "cover_banner_16x9": "https://cdn.jsdelivr.net/gh/gazpearce/cctv-security-hub@master/assets/images/starlink-gen3-heavy-duty-chimney-lashing-livesey.webp",
        "cover_banner_github_raw": "https://raw.githubusercontent.com/gazpearce/cctv-security-hub/master/assets/images/starlink-gen3-heavy-duty-chimney-lashing-livesey.webp",
        "alt_cctv_banner": "https://cdn.jsdelivr.net/gh/gazpearce/cctv-security-hub@master/assets/images/cctv-4k-turret-soffit-mount-almondbury.webp",
        "gallery_hub_url": "https://gary-pearce-forensic-hub.web.app/image-gallery.html"
    },
    "rule_45_google_shield_anchors": {
        "primary_shield_blogger_da99": "https://tvandhomesecurity.blogspot.com/",
        "google_drive_asset_vault_da100": "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
        "youtube_verified_channel": "https://www.youtube.com/@CCTV.services",
        "google_sites_pillar_da97": "https://sites.google.com/view/cctv-security-hub-uk",
        "firebase_app_hosting_edge": "https://gary-pearce-forensic-hub.web.app/",
        "github_open_source_repo": "https://github.com/gazpearce/cctv-security-hub",
        "gitlab_open_source_repo": "https://gitlab.com/aiagent1510/cctv-security-hub",
        "buffer_posts": {
            "ethernet_upstairs": "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/",
            "tv_above_fireplace": "https://adicommunications.co.uk/news/tv-above-fireplace-safe-installation/",
            "starlink_chimney_vs_apex": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/",
            "ajax_wireless_grade2": "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/"
        },
        "enforcement_rule": "CRITICAL: External cloud platforms must NEVER link directly to the money site root ('adicommunications.co.uk/'). All inbound links must route through Google Shield (Blogger/Drive/YouTube/Sites) or to specific disposable buffer posts under /news/."
    },
    "directory_135_platforms": []
}

raw_platforms = [
    # Layer 1: Static Sites & Portals (1-30)
    (1, "Layer 1: Static Websites & Portals", "GitHub Pages", "Static Website & Diagnostic Hub", "https://pages.github.com", "GitHub OAuth", "primary_shield_blogger_da99", "ACTIVE", "gazpearce/cctv-security-hub"),
    (2, "Layer 1: Static Websites & Portals", "GitLab Pages", "Continuous Mirror & Pipeline", "https://gitlab.com", "GitLab OAuth", "primary_shield_blogger_da99", "ACTIVE", "aiagent1510/cctv-security-hub"),
    (3, "Layer 1: Static Websites & Portals", "Cloudflare Pages", "Global Anycast Edge CDN", "https://pages.cloudflare.com", "Google/GitHub", "firebase_app_hosting_edge", "STAGED", "cctv-security-hub"),
    (4, "Layer 1: Static Websites & Portals", "Firebase Hosting", "High-Speed Google Edge CDN", "https://firebase.google.com", "Google OAuth", "primary_shield_blogger_da99", "ACTIVE", "https://gary-pearce-forensic-hub.web.app"),
    (5, "Layer 1: Static Websites & Portals", "Vercel", "Edge Deployment & Previews", "https://vercel.com", "GitHub/Google", "firebase_app_hosting_edge", "STAGED", "vercel.json"),
    (6, "Layer 1: Static Websites & Portals", "Netlify", "Static Diagnostic Tools Host", "https://netlify.com", "GitHub/Google", "firebase_app_hosting_edge", "STAGED", "netlify.toml"),
    (7, "Layer 1: Static Websites & Portals", "Render Static", "Static Tool Mirror", "https://render.com", "GitHub/GitLab", "firebase_app_hosting_edge", "STAGED", "render.yaml"),
    (8, "Layer 1: Static Websites & Portals", "Surge.sh", "Rapid Sandboxed Landing Mirrors", "https://surge.sh", "CLI Token", "primary_shield_blogger_da99", "READY", "surge cctv-security-hub.surge.sh"),
    (9, "Layer 1: Static Websites & Portals", "Google Sites", "Tier-2 Google Citadel Hub", "https://sites.google.com", "Google OAuth", "primary_shield_blogger_da99", "ACTIVE", "https://sites.google.com/view/cctv-security-hub-uk"),
    (10, "Layer 1: Static Websites & Portals", "Blogger", "Tier-2 Primary Google Shield (DA 99)", "https://blogger.com", "Google OAuth", "buffer_posts.ethernet_upstairs", "ACTIVE", "https://tvandhomesecurity.blogspot.com"),
    (11, "Layer 1: Static Websites & Portals", "Codeberg Pages", "Independent Git Authority", "https://codeberg.page", "Codeberg OAuth", "github_open_source_repo", "READY", "codeberg.org/gazpearce"),
    (12, "Layer 1: Static Websites & Portals", "SourceHut Pages", "Lightweight Developer Hosting", "https://sr.ht", "SourceHut", "github_open_source_repo", "READY", "~gazpearce/cctv-hub"),
    (13, "Layer 1: Static Websites & Portals", "Neocities", "Tech Community Node", "https://neocities.org", "Email/Web", "primary_shield_blogger_da99", "READY", "cctv-forensics.neocities.org"),
    (14, "Layer 1: Static Websites & Portals", "Tiiny Host", "Instant Drag-and-Drop Static", "https://tiiny.host", "Web", "primary_shield_blogger_da99", "READY", "tiiny.host/cctv-calc"),
    (15, "Layer 1: Static Websites & Portals", "Carrd", "Micro Service Profile Card", "https://carrd.co", "Email", "primary_shield_blogger_da99", "READY", "garypearce.carrd.co"),
    (16, "Layer 1: Static Websites & Portals", "Framer", "High-End Visual Showcase", "https://framer.com", "Google/Email", "primary_shield_blogger_da99", "READY", "adi-security.framer.app"),
    (17, "Layer 1: Static Websites & Portals", "Webflow", "Agency Showcase", "https://webflow.com", "Google/Email", "primary_shield_blogger_da99", "READY", "adi-security.webflow.io"),
    (18, "Layer 1: Static Websites & Portals", "Wix", "Secondary Business Citations", "https://wix.com", "Google/Email", "primary_shield_blogger_da99", "READY", "adi-cctv.wixsite.com"),
    (19, "Layer 1: Static Websites & Portals", "Notion Sites", "Interactive Study Guide & Specs", "https://notion.so", "Google/Email", "google_drive_asset_vault_da100", "ACTIVE", "notion.site/gary-pearce-specs"),
    (20, "Layer 1: Static Websites & Portals", "GitBook", "CCTV & Telecom Technical Manuals", "https://gitbook.com", "GitHub/Google", "github_open_source_repo", "READY", "gazpearce.gitbook.io"),
    (21, "Layer 1: Static Websites & Portals", "Read the Docs", "Hardware Engineering Specs", "https://readthedocs.org", "GitHub/GitLab", "github_open_source_repo", "READY", "cctv-security-hub.rtfd.io"),
    (22, "Layer 1: Static Websites & Portals", "ReadMe", "Interactive CCTV API Docs", "https://readme.com", "Web", "github_open_source_repo", "READY", "cctv-forensics.readme.io"),
    (23, "Layer 1: Static Websites & Portals", "Docusaurus", "Documentation Suite Generator", "https://docusaurus.io", "Static/Git", "github_open_source_repo", "READY", "cctv-security-hub/docs"),
    (24, "Layer 1: Static Websites & Portals", "MkDocs", "Python Technical Field Manual", "https://mkdocs.org", "Static/Git", "gitlab_open_source_repo", "READY", "cctv-security-hub/mkdocs"),
    (25, "Layer 1: Static Websites & Portals", "Dev.to", "Developer Technical Field Articles", "https://dev.to", "GitHub/Twitter", "primary_shield_blogger_da99", "READY", "dev.to/gazpearce"),
    (26, "Layer 1: Static Websites & Portals", "Hashnode", "Technical Network Whitepapers", "https://hashnode.com", "GitHub/Google", "primary_shield_blogger_da99", "READY", "gazpearce.hashnode.dev"),
    (27, "Layer 1: Static Websites & Portals", "Substack", "Yorkshire Trade Newsletter", "https://substack.com", "Google/Email", "primary_shield_blogger_da99", "READY", "garypearce.substack.com"),
    (28, "Layer 1: Static Websites & Portals", "Medium", "Thought Leadership & Field Insights", "https://medium.com", "Google/Email", "primary_shield_blogger_da99", "READY", "medium.com/@garypearce"),
    (29, "Layer 1: Static Websites & Portals", "CodePen", "DORI & Wind Load Math Snippets", "https://codepen.io", "GitHub/Google", "github_open_source_repo", "READY", "codepen.io/gazpearce"),
    (30, "Layer 1: Static Websites & Portals", "JSFiddle", "Live Ohm's Law & PoE Math Embeds", "https://jsfiddle.net", "GitHub/Google", "github_open_source_repo", "READY", "jsfiddle.net/u/gazpearce"),

    # Layer 2: APIs, Microservices & Runtimes (31-55)
    (31, "Layer 2: APIs & Edge Runtimes", "Cloudflare Workers", "DORI & Wind Math Edge API", "https://workers.cloudflare.com", "Cloudflare", "firebase_app_hosting_edge", "STAGED", "wrangler.toml"),
    (32, "Layer 2: APIs & Edge Runtimes", "Deno Deploy", "TypeScript Math Microservice", "https://deno.com/deploy", "GitHub", "firebase_app_hosting_edge", "READY", "deno.land/x/cctv"),
    (33, "Layer 2: APIs & Edge Runtimes", "Google Cloud Run", "Containerized Microservices", "https://cloud.google.com/run", "Google Cloud", "primary_shield_blogger_da99", "ACTIVE", "gcr.io/cctv-forensics"),
    (34, "Layer 2: APIs & Edge Runtimes", "Hugging Face Spaces", "Gradio AI Diagnostic Calculators", "https://huggingface.co/spaces", "GitHub/Email", "google_drive_asset_vault_da100", "READY", "huggingface.co/spaces/gazpearce/cctv-dori"),
    (35, "Layer 2: APIs & Edge Runtimes", "Render Services", "Node.js Backend API", "https://render.com", "GitHub/GitLab", "firebase_app_hosting_edge", "STAGED", "render.yaml"),
    (36, "Layer 2: APIs & Edge Runtimes", "Railway", "Dockerized Automation Microservices", "https://railway.com", "GitHub", "firebase_app_hosting_edge", "READY", "railway.app/cctv-api"),
    (37, "Layer 2: APIs & Edge Runtimes", "Fly.io", "Global Edge Docker Containers", "https://fly.io", "GitHub/Email", "firebase_app_hosting_edge", "READY", "cctv-hub.fly.dev"),
    (38, "Layer 2: APIs & Edge Runtimes", "DigitalOcean Apps", "Static Tools & Micro-Containers", "https://digitalocean.com", "GitHub/Google", "firebase_app_hosting_edge", "READY", "cctv-hub.ondigitalocean.app"),
    (39, "Layer 2: APIs & Edge Runtimes", "AWS Lambda & Free", "Serverless Background Calculators", "https://aws.amazon.com/free", "AWS Account", "firebase_app_hosting_edge", "READY", "lambda:cctv-storage"),
    (40, "Layer 2: APIs & Edge Runtimes", "Oracle Cloud Always Free", "High-Power Compute Instance", "https://oracle.com/cloud/free", "Oracle Account", "primary_shield_blogger_da99", "READY", "oci-ampere-cctv"),
    (41, "Layer 2: APIs & Edge Runtimes", "Koyeb", "Serverless Web Microservice", "https://koyeb.com", "GitHub/GitLab", "firebase_app_hosting_edge", "READY", "cctv-api.koyeb.app"),
    (42, "Layer 2: APIs & Edge Runtimes", "Northflank", "Micro Services & Cron Jobs", "https://northflank.com", "GitHub/GitLab", "firebase_app_hosting_edge", "READY", "northflank:cctv-cron"),
    (43, "Layer 2: APIs & Edge Runtimes", "Qovery", "Git-Driven Container Cluster", "https://qovery.com", "GitHub/GitLab", "firebase_app_hosting_edge", "READY", "qovery:cctv-cluster"),
    (44, "Layer 2: APIs & Edge Runtimes", "Google Apps Script", "Lead Dispatch & Drive Automation", "https://script.google.com", "Google OAuth", "google_drive_asset_vault_da100", "ACTIVE", "script.google.com/macros/d/cctv-leads"),
    (45, "Layer 2: APIs & Edge Runtimes", "Replit", "Interactive Python Code Demos", "https://replit.com", "Google/GitHub", "github_open_source_repo", "READY", "replit.com/@gazpearce/cctv-math"),
    (46, "Layer 2: APIs & Edge Runtimes", "StackBlitz", "In-Browser WebContainer IDE", "https://stackblitz.com", "GitHub/Google", "github_open_source_repo", "READY", "stackblitz.com/edit/cctv-hub"),
    (47, "Layer 2: APIs & Edge Runtimes", "CodeSandbox", "React & Vue Forensic UI Sandbox", "https://codesandbox.io", "GitHub/Google", "github_open_source_repo", "READY", "codesandbox.io/s/cctv-tools"),
    (48, "Layer 2: APIs & Edge Runtimes", "GitHub Codespaces", "Cloud Development Environment", "https://github.com/features/codespaces", "GitHub", "github_open_source_repo", "ACTIVE", "codespaces/gazpearce"),
    (49, "Layer 2: APIs & Edge Runtimes", "Appwrite Cloud", "Headless Backend & Auth", "https://appwrite.io", "GitHub/Google", "firebase_app_hosting_edge", "READY", "cloud.appwrite.io/v1/cctv"),
    (50, "Layer 2: APIs & Edge Runtimes", "Convex", "Real-Time Syncing Tools Backend", "https://convex.dev", "GitHub", "firebase_app_hosting_edge", "READY", "convex:cctv-sync"),
    (51, "Layer 2: APIs & Edge Runtimes", "IBM Cloud Code Engine", "Secondary Serverless Container Host", "https://ibm.com/cloud/free", "IBM Account", "firebase_app_hosting_edge", "READY", "ibm.com/codeengine/cctv"),
    (52, "Layer 2: APIs & Edge Runtimes", "Alibaba Cloud Free", "Global Infrastructure Entity Node", "https://alibabacloud.com", "Web", "github_open_source_repo", "READY", "alicloud:cctv-mirror"),
    (53, "Layer 2: APIs & Edge Runtimes", "Tencent Cloud Free", "International Web Functions Node", "https://cloud.tencent.com", "Web", "github_open_source_repo", "READY", "tencent:cctv-functions"),
    (54, "Layer 2: APIs & Edge Runtimes", "Modal", "High-Performance Python ML Processing", "https://modal.com", "GitHub", "google_drive_asset_vault_da100", "READY", "modal.run/gazpearce/cctv"),
    (55, "Layer 2: APIs & Edge Runtimes", "OpenRouter", "Automated LLM Content Routing", "https://openrouter.ai", "Google/GitHub", "primary_shield_blogger_da99", "ACTIVE", "openrouter:cctv-agent"),

    # Layer 3: Databases, Cloud Storage & Media (56-80)
    (56, "Layer 3: Databases & Storage", "Cloudflare D1", "Distributed Edge SQLite Database", "https://developers.cloudflare.com/d1/", "Cloudflare", "firebase_app_hosting_edge", "STAGED", "d1_crime_db"),
    (57, "Layer 3: Databases & Storage", "Cloudflare R2", "S3-Compatible Zero Egress Storage", "https://developers.cloudflare.com/r2/", "Cloudflare", "firebase_app_hosting_edge", "STAGED", "r2_cctv_assets"),
    (58, "Layer 3: Databases & Storage", "Supabase", "Relational Database & Crime Telemetry", "https://supabase.com", "GitHub", "firebase_app_hosting_edge", "READY", "supabase:cctv-crime"),
    (59, "Layer 3: Databases & Storage", "Neon", "Serverless PostgreSQL for Client Tools", "https://neon.tech", "GitHub/Google", "firebase_app_hosting_edge", "READY", "neon:cctv-storage"),
    (60, "Layer 3: Databases & Storage", "Turso", "Embedded Distributed Edge SQLite", "https://turso.tech", "GitHub", "firebase_app_hosting_edge", "READY", "turso:cctv-sqlite"),
    (61, "Layer 3: Databases & Storage", "CockroachDB Cloud", "Distributed SQL Cluster", "https://cockroachlabs.com", "Google/GitHub", "firebase_app_hosting_edge", "READY", "cockroach:cctv-cluster"),
    (62, "Layer 3: Databases & Storage", "MongoDB Atlas", "NoSQL Document Store", "https://mongodb.com/atlas", "Google/GitHub", "firebase_app_hosting_edge", "READY", "mongodb:cctv-specs"),
    (63, "Layer 3: Databases & Storage", "Upstash", "Serverless Redis & Rate Limiter", "https://upstash.com", "GitHub/Google", "firebase_app_hosting_edge", "READY", "upstash:cctv-cache"),
    (64, "Layer 3: Databases & Storage", "Firebase Firestore", "NoSQL Lead Capture & Cache", "https://firebase.google.com", "Google OAuth", "primary_shield_blogger_da99", "ACTIVE", "firestore:gary-pearce-hub"),
    (65, "Layer 3: Databases & Storage", "Google Drive Hub", "Public Asset Vault (DA 100)", "https://drive.google.com", "Google OAuth", "primary_shield_blogger_da99", "ACTIVE", "1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88"),
    (66, "Layer 3: Databases & Storage", "jsDelivr Multi-CDN", "Sub-15ms GitHub Trade Image CDN", "https://jsdelivr.com", "Automated", "primary_shield_blogger_da99", "ACTIVE", "cdn.jsdelivr.net/gh/gazpearce"),
    (67, "Layer 3: Databases & Storage", "Cloudinary", "Dynamic Image Optimization", "https://cloudinary.com", "Google/GitHub", "gallery_hub_url", "READY", "cloudinary:cctv-assets"),
    (68, "Layer 3: Databases & Storage", "ImageKit", "Global Media Transformation CDN", "https://imagekit.io", "Google/Email", "gallery_hub_url", "READY", "imagekit:cctv-media"),
    (69, "Layer 3: Databases & Storage", "Backblaze B2", "Immutable Off-Site Backup Vault", "https://backblaze.com/b2", "Email", "google_drive_asset_vault_da100", "READY", "b2:cctv-raw-vault"),
    (70, "Layer 3: Databases & Storage", "Storj", "Decentralized Censorship-Resistant Store", "https://storj.io", "Email", "google_drive_asset_vault_da100", "READY", "storj:cctv-nodes"),
    (71, "Layer 3: Databases & Storage", "PocketBase", "Local Fast SQLite Database", "https://pocketbase.io", "Self-Host", "firebase_app_hosting_edge", "LOCAL", "http://127.0.0.1:8090"),
    (72, "Layer 3: Databases & Storage", "Directus", "Headless CMS for Local Services", "https://directus.io", "Self-Host", "firebase_app_hosting_edge", "LOCAL", "http://127.0.0.1:8055"),
    (73, "Layer 3: Databases & Storage", "NocoDB", "Internal Lead & Job Tracking Database", "https://nocodb.com", "Self-Host", "firebase_app_hosting_edge", "LOCAL", "http://127.0.0.1:8080"),
    (74, "Layer 3: Databases & Storage", "Baserow", "Installation Progress Tracker", "https://baserow.io", "Self-Host", "firebase_app_hosting_edge", "LOCAL", "http://127.0.0.1:8081"),
    (75, "Layer 3: Databases & Storage", "Aiven", "Managed Cloud PostgreSQL/MySQL", "https://aiven.io", "Google/GitHub", "firebase_app_hosting_edge", "READY", "aiven:cctv-postgres"),
    (76, "Layer 3: Databases & Storage", "Imgur", "Public High-DA Image Backlinks", "https://imgur.com", "Google/Email", "primary_shield_blogger_da99", "READY", "imgur.com/user/gazpearce"),
    (77, "Layer 3: Databases & Storage", "Flickr", "Geotagged Field Installation Proof (DA 93)", "https://flickr.com", "Google/Email", "primary_shield_blogger_da99", "READY", "flickr.com/photos/garypearce"),
    (78, "Layer 3: Databases & Storage", "Unsplash", "Contributor Trade Photo Portfolio", "https://unsplash.com", "Email", "primary_shield_blogger_da99", "READY", "unsplash.com/@garypearce"),
    (79, "Layer 3: Databases & Storage", "Pexels", "Professional Contributor Profile", "https://pexels.com", "Email", "primary_shield_blogger_da99", "READY", "pexels.com/@garypearce"),
    (80, "Layer 3: Databases & Storage", "Wikimedia Commons", "Public Domain Diagram Attribution (DA 95)", "https://commons.wikimedia.org", "Web", "primary_shield_blogger_da99", "READY", "commons:cctv-diagrams"),

    # Layer 4: AI Inference, Notebooks & Audio Stacks (81-105)
    (81, "Layer 4: AI, Notebooks & Audio", "Google NotebookLM", "Dual-Engineer Audio Debriefs (£0)", "https://notebooklm.google.com", "Google OAuth", "primary_shield_blogger_da99", "ACTIVE", "ADI Communications Content Hub"),
    (82, "Layer 4: AI, Notebooks & Audio", "Google AI Studio", "Gemini 2.5 Flash High-Speed Inference", "https://aistudio.google.com", "Google OAuth", "primary_shield_blogger_da99", "ACTIVE", "ai.google.dev"),
    (83, "Layer 4: AI, Notebooks & Audio", "GroqCloud", "Ultra-Fast LPU Schema Auditing", "https://console.groq.com", "Google/GitHub", "primary_shield_blogger_da99", "ACTIVE", "groq:llama-3.3"),
    (84, "Layer 4: AI, Notebooks & Audio", "Local Ollama", "Offline Trade Inference on RTX 5060 Ti", "https://ollama.com", "Local", "primary_shield_blogger_da99", "ACTIVE", "http://localhost:11434"),
    (85, "Layer 4: AI, Notebooks & Audio", "Local Kokoro Voice", "High-Speed British Neural Audio Engine", "https://github.com/hexgrad/kokoro", "Local", "primary_shield_blogger_da99", "ACTIVE", "http://localhost:8885"),
    (86, "Layer 4: AI, Notebooks & Audio", "Google Colab", "Public Math & DORI Calculation Proofs", "https://colab.research.google.com", "Google OAuth", "google_drive_asset_vault_da100", "ACTIVE", "colab:cctv-storage-math"),
    (87, "Layer 4: AI, Notebooks & Audio", "Kaggle Notebooks", "UK Police Crime Telemetry Dataset", "https://kaggle.com/code", "Google OAuth", "primary_shield_blogger_da99", "READY", "kaggle:uk-crime-cctv"),
    (88, "Layer 4: AI, Notebooks & Audio", "Lightning AI", "Interactive AI Field Tool Prototypes", "https://lightning.ai", "Google/GitHub", "github_open_source_repo", "READY", "lightning:cctv-diagnostics"),
    (89, "Layer 4: AI, Notebooks & Audio", "Deepnote", "Collaborative Security Telemetry", "https://deepnote.com", "Google/GitHub", "github_open_source_repo", "READY", "deepnote:cctv-notebook"),
    (90, "Layer 4: AI, Notebooks & Audio", "Observable HQ", "D3.js Wind Load & Lens Angle Charts", "https://observablehq.com", "Google/GitHub", "github_open_source_repo", "READY", "observablehq.com/@gazpearce"),
    (91, "Layer 4: AI, Notebooks & Audio", "YouTube Podcasts", "Official Show on Channel @CCTV.services", "https://podcasts.google.com", "Google OAuth", "primary_shield_blogger_da99", "ACTIVE", "Channel UCt7VpJGmZZ12hdg2sCgjQag"),
    (92, "Layer 4: AI, Notebooks & Audio", "Internet Archive", "Lossless Archival & Dublin Core XML", "https://archive.org", "Email", "primary_shield_blogger_da99", "ACTIVE", "archive.org/details/cctv-security-hub"),
    (93, "Layer 4: AI, Notebooks & Audio", "DailyMotion", "Secondary Tier 3 Video Parasite", "https://dailymotion.com", "Google/Email", "youtube_verified_channel", "ACTIVE", "dailymotion.com/gazpearce"),
    (94, "Layer 4: AI, Notebooks & Audio", "Vimeo", "Clean Showcase Engineering Videos", "https://vimeo.com", "Google/Email", "youtube_verified_channel", "ACTIVE", "vimeo.com/gazpearce"),
    (95, "Layer 4: AI, Notebooks & Audio", "Rumble", "Independent Video Mirror Node", "https://rumble.com", "Email", "youtube_verified_channel", "READY", "rumble.com/c/cctvservices"),
    (96, "Layer 4: AI, Notebooks & Audio", "Odysee / LBRY", "Decentralized Blockchain Video", "https://odysee.com", "Email", "youtube_verified_channel", "READY", "odysee.com/@cctv-services"),
    (97, "Layer 4: AI, Notebooks & Audio", "Podbean", "Apple & Spotify RSS Podcast Feed", "https://podbean.com", "Google/Email", "primary_shield_blogger_da99", "ACTIVE", "adi-security.podbean.com"),
    (98, "Layer 4: AI, Notebooks & Audio", "Spotify for Podcasters", "Global Audio Entity Distribution", "https://podcasters.spotify.com", "Spotify/Google", "primary_shield_blogger_da99", "READY", "spotify:show:cctv-security"),
    (99, "Layer 4: AI, Notebooks & Audio", "SoundCloud", "Social Audio Waveform Embeds", "https://soundcloud.com", "Google/Email", "primary_shield_blogger_da99", "READY", "soundcloud.com/garypearce"),
    (100, "Layer 4: AI, Notebooks & Audio", "Replicate", "Hosted Model Testing Bed", "https://replicate.com", "GitHub", "github_open_source_repo", "READY", "replicate:cctv-vision"),
    (101, "Layer 4: AI, Notebooks & Audio", "GitHub Models", "Prototype Access to Enterprise LLMs", "https://github.com/marketplace/models", "GitHub", "github_open_source_repo", "ACTIVE", "models:github"),
    (102, "Layer 4: AI, Notebooks & Audio", "Wistia", "High-Definition Video Showcase", "https://wistia.com", "Email", "youtube_verified_channel", "READY", "wistia:cctv-debriefs"),
    (103, "Layer 4: AI, Notebooks & Audio", "PeerTube", "Federated ActivityPub Video Network", "https://joinpeertube.org", "Fediverse", "youtube_verified_channel", "READY", "peertube:cctv-videos"),
    (104, "Layer 4: AI, Notebooks & Audio", "Vast.ai", "Spot GPU Instance Marketplace", "https://vast.ai", "Web", "github_open_source_repo", "READY", "vast.ai:cctv-render"),
    (105, "Layer 4: AI, Notebooks & Audio", "RunPod", "Serverless GPU Audio & Video Tasks", "https://runpod.io", "Web", "github_open_source_repo", "READY", "runpod:cctv-tasks"),

    # Layer 5: Automation, Workflows & DevOps (106-135)
    (106, "Layer 5: Automation & DevOps", "Local n8n", "Master Operational Workflow Engine", "https://n8n.io", "Localhost", "firebase_app_hosting_edge", "ACTIVE", "http://localhost:5678"),
    (107, "Layer 5: Automation & DevOps", "GitHub Actions", "Automated CI/CD, Audits & Sync", "https://github.com/features/actions", "GitHub", "github_open_source_repo", "ACTIVE", ".github/workflows/qc.yml"),
    (108, "Layer 5: Automation & DevOps", "GitLab CI/CD", "Continuous Multi-Cloud Edge Deployments", "https://gitlab.com", "GitLab", "gitlab_open_source_repo", "ACTIVE", ".gitlab-ci.yml"),
    (109, "Layer 5: Automation & DevOps", "Node-RED", "Visual Event Pipelines & Telegram Hooks", "https://nodered.org", "Localhost", "firebase_app_hosting_edge", "ACTIVE", "http://localhost:1880"),
    (110, "Layer 5: Automation & DevOps", "Activepieces", "Alternative Self-Hosted Workflow Engine", "https://activepieces.com", "Docker/Cloud", "firebase_app_hosting_edge", "READY", "activepieces:cctv"),
    (111, "Layer 5: Automation & DevOps", "Windmill", "High-Speed Python/TypeScript Jobs", "https://windmill.dev", "Self-Host/Cloud", "firebase_app_hosting_edge", "READY", "windmill:cctv-jobs"),
    (112, "Layer 5: Automation & DevOps", "Kestra", "Event-Driven Multi-Cloud Orchestration", "https://kestra.io", "Docker/Cloud", "firebase_app_hosting_edge", "READY", "kestra:cctv-flow"),
    (113, "Layer 5: Automation & DevOps", "Pipedream", "Serverless Webhook & Lead Ingestion", "https://pipedream.com", "GitHub/Google", "firebase_app_hosting_edge", "READY", "pipedream:cctv-leads"),
    (114, "Layer 5: Automation & DevOps", "Make (Integromat)", "Visual Multi-App Automation Scenarios", "https://make.com", "Google/Email", "primary_shield_blogger_da99", "ACTIVE", "make:cctv-notifications"),
    (115, "Layer 5: Automation & DevOps", "Zapier", "Backup Lead & Telegram Dispatch", "https://zapier.com", "Google/Email", "primary_shield_blogger_da99", "READY", "zapier:cctv-leads"),
    (116, "Layer 5: Automation & DevOps", "IFTTT", "Simple Event-Driven Hardware Applets", "https://ifttt.com", "Google/Email", "primary_shield_blogger_da99", "READY", "ifttt:cctv-alerts"),
    (117, "Layer 5: Automation & DevOps", "Google Cloud Workflows", "Serverless GCP Microservice Chaining", "https://cloud.google.com/workflows", "Google Cloud", "primary_shield_blogger_da99", "ACTIVE", "gcp:workflows-cctv"),
    (118, "Layer 5: Automation & DevOps", "Huginn", "Automated Competitor & SERP Monitor", "https://github.com/huginn/huginn", "Docker", "firebase_app_hosting_edge", "LOCAL", "huginn:cctv-monitor"),
    (119, "Layer 5: Automation & DevOps", "Apache Airflow", "Dataform & BigQuery Job Orchestration", "https://airflow.apache.org", "Docker", "firebase_app_hosting_edge", "LOCAL", "airflow:cctv-pipeline"),
    (120, "Layer 5: Automation & DevOps", "UptimeRobot", "24/7 Endpoint Health Verification", "https://uptimerobot.com", "Google/Email", "firebase_app_hosting_edge", "READY", "uptimerobot:cctv-monitors"),
    (121, "Layer 5: Automation & DevOps", "Better Stack", "Incident Response & Latency Status", "https://betterstack.com", "Google/GitHub", "firebase_app_hosting_edge", "READY", "status.cctv-hub.betterstack.com"),
    (122, "Layer 5: Automation & DevOps", "Sentry", "Client-Side Calculator Exception Catching", "https://sentry.io", "GitHub/Google", "github_open_source_repo", "READY", "sentry:cctv-hub"),
    (123, "Layer 5: Automation & DevOps", "Grafana Cloud", "Real-Time Telemetry & Log Dashboards", "https://grafana.com", "Google/GitHub", "firebase_app_hosting_edge", "READY", "grafana:cctv-metrics"),
    (124, "Layer 5: Automation & DevOps", "PostHog", "Tool Interaction & Drop-Off Analytics", "https://posthog.com", "Google/GitHub", "firebase_app_hosting_edge", "READY", "posthog:cctv-analytics"),
    (125, "Layer 5: Automation & DevOps", "Umami", "GDPR-Compliant Analytics for Open Suite", "https://umami.is", "Self-Host/Cloud", "firebase_app_hosting_edge", "READY", "umami:cctv-privacy"),
    (126, "Layer 5: Automation & DevOps", "Resend", "Instant PDF Estimate Dispatch API", "https://resend.com", "GitHub/Google", "firebase_app_hosting_edge", "READY", "resend:cctv-estimates"),
    (127, "Layer 5: Automation & DevOps", "Brevo (Sendinblue)", "Transactional Email & SMS Verification", "https://brevo.com", "Google/Email", "primary_shield_blogger_da99", "READY", "brevo:cctv-sms"),
    (128, "Layer 5: Automation & DevOps", "Clerk", "Client Portal Authentication Backend", "https://clerk.com", "Google/GitHub", "firebase_app_hosting_edge", "READY", "clerk:cctv-portal"),
    (129, "Layer 5: Automation & DevOps", "Auth0", "Enterprise Identity Management Provider", "https://auth0.com", "Google/GitHub", "firebase_app_hosting_edge", "READY", "auth0:cctv-auth"),
    (130, "Layer 5: Automation & DevOps", "Let's Encrypt", "Automated TLS/SSL Edge Certificates", "https://letsencrypt.org", "Automated", "firebase_app_hosting_edge", "ACTIVE", "certbot:auto-renew"),
    (131, "Layer 5: Automation & DevOps", "DuckDNS", "Dynamic DNS Subdomain Resolution", "https://duckdns.org", "Google/Reddit", "firebase_app_hosting_edge", "ACTIVE", "adi-security.duckdns.org"),
    (132, "Layer 5: Automation & DevOps", "deSEC", "Secure Modern DNS Hosting with DNSSEC", "https://desec.io", "Email", "firebase_app_hosting_edge", "READY", "desec:cctv-hub"),
    (133, "Layer 5: Automation & DevOps", "OpenStreetMap", "Postcode Geolocation & Boundary Math", "https://openstreetmap.org", "Open Data", "primary_shield_blogger_da99", "ACTIVE", "osm:uk-telecoms"),
    (134, "Layer 5: Automation & DevOps", "Bluesky Social", "AT-Protocol Field Engineering Updates", "https://bsky.app", "Email", "primary_shield_blogger_da99", "ACTIVE", "bsky.app/profile/adi-security.bsky.social"),
    (135, "Layer 5: Automation & DevOps", "Mastodon", "ActivityPub Telecom Engineering Community", "https://joinmastodon.org", "Email", "primary_shield_blogger_da99", "ACTIVE", "mastodon.social/@garypearce")
]

for p in raw_platforms:
    manifest["directory_135_platforms"].append({
        "id": p[0],
        "layer": p[1],
        "name": p[2],
        "category": p[3],
        "canonical_url": p[4],
        "auth_method": p[5],
        "google_shield_anchor": p[6],
        "operational_status": p[7],
        "deployment_endpoint_or_spec": p[8]
    })

target_file = r"C:\Users\Gary\github-cctv-seo\master_profile_manifest.json"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {target_file}")
print(f"Total platforms registered: {len(manifest['directory_135_platforms'])}")
