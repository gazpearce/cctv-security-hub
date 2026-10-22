import json
import os

registry = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "version": "1.0.0",
    "title": "ADI Communications & Gary Pearce — Master 100-Platform Free Image Stacking Registry",
    "description": "Comprehensive directory of 100 free image hosting, storage, and community platforms with API capabilities, public URL types, retention limits, and Rule 45 Google Shield link targets.",
    "classification_standard": {
        "type_a_direct_url": "Direct image file delivery (CDN / raw image) viewable anywhere.",
        "type_b_public_page": "Standalone public webpage featuring title, description, and rendered image.",
        "type_c_clickable_backlink": "Public webpage with an active clickable external anchor passing referral traffic and SEO entity signals."
    },
    "rule_45_shield_anchors": {
        "primary_blogger": "https://tvandhomesecurity.blogspot.com/",
        "google_drive_vault": "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
        "youtube_channel": "https://www.youtube.com/@CCTV.services",
        "firebase_hub": "https://gary-pearce-forensic-hub.web.app/",
        "buffer_posts": {
            "ethernet_upstairs": "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/",
            "tv_above_fireplace": "https://adicommunications.co.uk/news/tv-above-fireplace-safe-installation/",
            "starlink_chimney_vs_apex": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/",
            "ajax_wireless_grade2": "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/"
        }
    },
    "platforms": []
}

raw_platforms = [
    # Tier 1 — Best API-First Image Hosts (1-10)
    (1, "Tier 1: API-First Image Hosts", "ImgBB", "https://imgbb.com", "https://api.imgbb.com/1/upload", "API Key", "Type B (Viewer)", "Permanent", "32 MB", "primary_blogger", "Established API, accepts files/base64/URLs"),
    (2, "Tier 1: API-First Image Hosts", "Cloudinary", "https://cloudinary.com", "https://api.cloudinary.com/v1_1/{cloud_name}/image/upload", "API Key / Secret", "Type A (CDN)", "Permanent", "25 credits/mo", "firebase_hub", "Best for production media transforms and fast delivery"),
    (3, "Tier 1: API-First Image Hosts", "ImgCDN.dev", "https://imgcdn.dev", "https://imgcdn.dev/api/1/upload", "Public / Guest", "Type B (Viewer)", "Permanent", "20 MB", "primary_blogger", "Public upload API, guest uploads supported"),
    (4, "Tier 1: API-First Image Hosts", "YourImageShare", "https://yourimageshare.com", "https://yourimageshare.com/api/upload", "Upload-Only Key", "Type C (Clickable)", "Permanent", "15 MB", "primary_blogger", "Separate upload-only API key for secure automated n8n workflows"),
    (5, "Tier 1: API-First Image Hosts", "HotIMG", "https://hotimg.com", "https://hotimg.com/api/upload", "API Key", "Type C (Clickable)", "Configurable", "32 MB", "primary_blogger", "Supports image title, custom retention, and direct/viewer links"),
    (6, "Tier 1: API-First Image Hosts", "PixelHost", "https://pixelhost.fun", "https://pixelhost.fun/api/upload", "Unauthenticated", "Type A (Direct)", "Permanent", "20 files/req", "firebase_hub", "Multi-file batch uploads without API keys"),
    (7, "Tier 1: API-First Image Hosts", "picrd.com", "https://picrd.com", "https://picrd.com/api/upload", "Account-Free", "Type B (Viewer)", "Permanent", "60 uploads/hr", "primary_blogger", "Account-free REST API, public or unlisted albums"),
    (8, "Tier 1: API-First Image Hosts", "imgdb.io", "https://imgdb.io", "https://imgdb.io/api/upload", "No-Signup", "Type A (Direct)", "Permanent", "250 images/day", "firebase_hub", "No-signup upload API, shareable albums up to 64 images"),
    (9, "Tier 1: API-First Image Hosts", "ImageUpload.io", "https://imageupload.io", "https://imageupload.io/api/upload", "API Key", "Type B (Viewer)", "Permanent", "10 uploads/mo", "primary_blogger", "Authenticated API with share URLs and embed codes"),
    (10, "Tier 1: API-First Image Hosts", "FreeImage.Host", "https://freeimage.host", "https://freeimage.host/api/1/upload", "Public API Key", "Type B (Viewer)", "Permanent", "64 MB", "primary_blogger", "Chevereto-powered high-capacity image host with instant JSON response"),

    # Tier 2 — Photo Communities with Public Pages & Clickable Backlinks (11-30)
    (11, "Tier 2: Photo Communities", "Pinterest", "https://pinterest.com", "https://api.pinterest.com/v5/pins", "OAuth 2.0", "Type C (Clickable)", "Permanent", "Unlimited", "buffer_posts.starlink_chimney_vs_apex", "Pins with title, description, and high-authority destination link"),
    (12, "Tier 2: Photo Communities", "Flickr", "https://flickr.com", "https://up.flickr.com/services/upload/", "OAuth 1.0a", "Type C (Clickable)", "Permanent", "1,000 photos", "primary_blogger", "Photo page with title, description, tags, and EXIF camera metadata"),
    (13, "Tier 2: Photo Communities", "Tumblr", "https://tumblr.com", "https://api.tumblr.com/v2/blog/{blog-identifier}/post", "OAuth 1.0a / 2.0", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Public image post with caption, rich text, and dofollow/nofollow links"),
    (14, "Tier 2: Photo Communities", "Behance", "https://behance.net", "https://api.behance.net/v2/", "Adobe OAuth", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Public engineering project showcase with multi-image presentation"),
    (15, "Tier 2: Photo Communities", "DeviantArt", "https://deviantart.com", "https://www.deviantart.com/api/v1/oauth2/", "OAuth 2.0", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Public artwork and technical photography page with description"),
    (16, "Tier 2: Photo Communities", "500px", "https://500px.com", "https://api.500px.com/v1/photos/upload", "OAuth 1.0a", "Type B (Viewer)", "Permanent", "2,000 photos", "primary_blogger", "High-end photography community portfolio"),
    (17, "Tier 2: Photo Communities", "ArtStation", "https://artstation.com", "Manual / Web", "Web Account", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Professional project page with rich technical descriptions"),
    (18, "Tier 2: Photo Communities", "Dribbble", "https://dribbble.com", "https://api.dribbble.com/v2/", "OAuth 2.0", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Design shots and visual diagram showcases"),
    (19, "Tier 2: Photo Communities", "Wikimedia Commons", "https://commons.wikimedia.org", "https://commons.wikimedia.org/w/api.php", "MediaWiki Bot", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Highest authority public domain entity reference (DA 95)"),
    (20, "Tier 2: Photo Communities", "Internet Archive", "https://archive.org", "https://archive.org/services/upload/v1/", "S3-Access Keys", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Permanent historical archival with Dublin Core metadata (DA 96)"),
    (21, "Tier 2: Photo Communities", "Imgur", "https://imgur.com", "https://api.imgur.com/3/image", "OAuth 2.0 / Client-ID", "Type B (Viewer)", "Permanent", "1,250 uploads/day", "primary_blogger", "High-DA viral and technical image community pages (DA 93)"),
    (22, "Tier 2: Photo Communities", "Unsplash", "https://unsplash.com", "https://api.unsplash.com/", "Developer API", "Type B (Viewer)", "Permanent", "Contributor Profile", "primary_blogger", "Global photography distribution and artist attribution"),
    (23, "Tier 2: Photo Communities", "Pexels", "https://pexels.com", "Web Contributor", "Email", "Type B (Viewer)", "Permanent", "Contributor Profile", "primary_blogger", "High-authority stock and editorial photography platform"),
    (24, "Tier 2: Photo Communities", "Pixabay", "https://pixabay.com", "Web Contributor", "Email", "Type B (Viewer)", "Permanent", "Contributor Profile", "primary_blogger", "Editorial and diagram photography community"),
    (25, "Tier 2: Photo Communities", "Hashnode", "https://hashnode.com", "https://api.hashnode.com", "Personal Access Token", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Technical articles with embedded trade photography and canonical links"),
    (26, "Tier 2: Photo Communities", "Medium", "https://medium.com", "Web / API", "OAuth", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Editorial field engineering articles with embedded image stacks"),
    (27, "Tier 2: Photo Communities", "Dev.to", "https://dev.to", "https://dev.to/api/articles", "API Key", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Developer whitepapers with image embeds and source links"),
    (28, "Tier 2: Photo Communities", "WordPress.com", "https://wordpress.com", "https://public-api.wordpress.com/rest/v1.1/", "OAuth 2.0", "Type C (Clickable)", "Permanent", "3 GB", "primary_blogger", "Hosted blog posts and dedicated media attachment pages"),
    (29, "Tier 2: Photo Communities", "Blogger", "https://blogger.com", "https://www.googleapis.com/blogger/v3/", "Google OAuth", "Type C (Clickable)", "Permanent", "15 GB (Google)", "buffer_posts.ethernet_upstairs", "Tier-2 Primary Google Shield hub on tvandhomesecurity.blogspot.com (DA 99)"),
    (30, "Tier 2: Photo Communities", "Ghost", "https://ghost.org", "Admin API", "Admin API Key", "Type C (Clickable)", "Permanent", "Self-Hosted / Cloud", "primary_blogger", "Modern publishing platform with full image metadata control"),

    # Tier 3 — Free Image Storage & Automated Object Storage APIs (31-60)
    (31, "Tier 3: Storage & Object APIs", "Cloudflare R2", "https://cloudflare.com/products/r2/", "S3 Compatible API", "R2 Access Keys", "Type A (CDN)", "Permanent", "10 GB / Zero Egress", "firebase_hub", "Free S3-compatible storage with public bucket custom domain support"),
    (32, "Tier 3: Storage & Object APIs", "Amazon S3", "https://aws.amazon.com/s3/", "AWS SDK / REST", "IAM Keys", "Type A (CDN)", "Permanent", "5 GB (12 mo)", "firebase_hub", "Industry standard cloud object storage with public read policies"),
    (33, "Tier 3: Storage & Object APIs", "Google Cloud Storage", "https://cloud.google.com/storage", "GCP SDK / REST", "Service Account", "Type A (CDN)", "Permanent", "5 GB / mo free", "firebase_hub", "Google Anycast storage with public URL capabilities"),
    (34, "Tier 3: Storage & Object APIs", "Azure Blob Storage", "https://azure.microsoft.com/services/storage/blobs/", "Azure SDK", "Shared Key", "Type A (CDN)", "Permanent", "5 GB (12 mo)", "firebase_hub", "Microsoft enterprise object storage with public blob access"),
    (35, "Tier 3: Storage & Object APIs", "Backblaze B2", "https://backblaze.com/b2", "S3 Compatible / Native", "Application Key", "Type A (CDN)", "Permanent", "10 GB free", "firebase_hub", "Zero-egress partner with Cloudflare for high-speed image delivery"),
    (36, "Tier 3: Storage & Object APIs", "Supabase Storage", "https://supabase.com/storage", "REST / S3 API", "Anon Key", "Type A (CDN)", "Permanent", "1 GB free", "firebase_hub", "Public storage buckets integrated with PostgreSQL metadata"),
    (37, "Tier 3: Storage & Object APIs", "Firebase Storage", "https://firebase.google.com/docs/storage", "Google SDK", "Service Account", "Type A (CDN)", "Permanent", "5 GB (Spark)", "firebase_hub", "Google Cloud Storage integration for mobile and web apps"),
    (38, "Tier 3: Storage & Object APIs", "ImageKit", "https://imagekit.io", "Upload API", "Private Key", "Type A (CDN)", "Permanent", "20 GB/mo", "firebase_hub", "Global image CDN with dynamic resizing, format conversion, and optimization"),
    (39, "Tier 3: Storage & Object APIs", "Bunny.net Storage", "https://bunny.net", "REST / FTP", "Storage Password", "Type A (CDN)", "Paid / Low Cost", "Pay per GB", "firebase_hub", "Ultra-fast global replication edge storage"),
    (40, "Tier 3: Storage & Object APIs", "Storj Decentralized", "https://storj.io", "S3 Compatible API", "Access Grant", "Type A (CDN)", "Permanent", "25 GB free", "firebase_hub", "Decentralized, encrypted object storage with public link sharing"),
    (41, "Tier 3: Storage & Object APIs", "DigitalOcean Spaces", "https://digitalocean.com/products/spaces", "S3 Compatible API", "Spaces Key", "Type A (CDN)", "Paid ($5/mo)", "250 GB", "firebase_hub", "S3-compatible object storage with built-in CDN"),
    (42, "Tier 3: Storage & Object APIs", "Wasabi Cloud", "https://wasabi.com", "S3 Compatible API", "Wasabi Key", "Type A (CDN)", "Trial / Paid", "No egress fee", "firebase_hub", "Hot cloud storage with zero egress fees"),
    (43, "Tier 3: Storage & Object APIs", "MinIO Self-Hosted", "https://min.io", "S3 API", "Access Key", "Type A (CDN)", "Permanent", "Local Disk", "firebase_hub", "High-performance S3-compatible object storage for Docker rigs"),
    (44, "Tier 3: Storage & Object APIs", "Garage S3", "https://garagehq.deuxfleurs.fr", "S3 API", "Access Key", "Type A (CDN)", "Permanent", "Local Disk", "firebase_hub", "Lightweight distributed S3-compatible store designed for self-hosting"),
    (45, "Tier 3: Storage & Object APIs", "SeaweedFS", "https://github.com/seaweedfs/seaweedfs", "S3 / WebDAV", "Access Key", "Type A (CDN)", "Permanent", "Local Disk", "firebase_hub", "Blazing fast distributed storage engine with S3 gateway"),
    (46, "Tier 3: Storage & Object APIs", "Zenko CloudServer", "https://zenko.io", "S3 API", "Access Key", "Type A (CDN)", "Permanent", "Local Disk", "firebase_hub", "Multi-cloud data controller with unified S3 interface"),
    (47, "Tier 3: Storage & Object APIs", "Catbox.moe", "https://catbox.moe", "https://catbox.moe/user/api.php", "Public / Userhash", "Type A (Direct)", "Permanent", "200 MB/file", "firebase_hub", "100% free unauthenticated file/image upload API for permanent files"),
    (48, "Tier 3: Storage & Object APIs", "jsDelivr GitHub Multi-CDN", "https://jsdelivr.com", "Automated Git", "None (Open Source)", "Type A (CDN)", "Permanent", "Unlimited", "primary_blogger", "Sub-15ms global multi-CDN caching for gazpearce/cctv-security-hub"),
    (49, "Tier 3: Storage & Object APIs", "Google Drive Direct CDN", "https://drive.google.com", "Google API", "OAuth 2.0", "Type A (CDN)", "Permanent", "15 GB", "google_drive_vault", "Permanent Google Cloud edge thumbnail delivery (lh3.googleusercontent.com/d/...)"),
    (50, "Tier 3: Storage & Object APIs", "Postimages", "https://postimages.org", "REST API", "API Key", "Type B (Viewer)", "Permanent", "24 MB", "primary_blogger", "Reliable permanent image hosting with message board and direct links"),
    (51, "Tier 3: Storage & Object APIs", "Imgbox", "https://imgbox.com", "Web / API", "Account Key", "Type B (Viewer)", "Permanent", "10 MB", "primary_blogger", "Fast, free image hosting with unlimited storage time and galleries"),
    (52, "Tier 3: Storage & Object APIs", "ImgPile", "https://imgpile.com", "https://imgpile.com/api/1/upload", "API Key", "Type B (Viewer)", "Permanent", "100 MB", "primary_blogger", "Chevereto-based high-capacity free image hosting platform"),
    (53, "Tier 3: Storage & Object APIs", "ImageVenue", "https://imagevenue.com", "Web / API", "Account", "Type B (Viewer)", "Permanent", "10 MB", "primary_blogger", "Long-standing image gallery and sharing platform"),
    (54, "Tier 3: Storage & Object APIs", "ImgHippo", "https://imghippo.com", "https://api.imghippo.com/v1/upload", "API Key", "Type B (Viewer)", "Permanent", "10 MB", "primary_blogger", "Modern image hosting API with direct and viewer link responses"),
    (55, "Tier 3: Storage & Object APIs", "Pasteboard", "https://pasteboard.co", "Web / API", "None", "Type B (Viewer)", "Permanent", "10 MB", "primary_blogger", "Quick paste and image sharing portal"),
    (56, "Tier 3: Storage & Object APIs", "ImageBam", "https://imagebam.com", "Web / API", "Account", "Type B (Viewer)", "Permanent", "10 MB", "primary_blogger", "Mass image uploader with thumbnail galleries"),
    (57, "Tier 3: Storage & Object APIs", "TurboImageHost", "https://turboimagehost.com", "Web / API", "Account", "Type B (Viewer)", "Permanent", "10 MB", "primary_blogger", "Fast multi-image hosting and BBCode generators"),
    (58, "Tier 3: Storage & Object APIs", "CubeUpload", "https://cubeupload.com", "Web / API", "Account", "Type A (Direct)", "Permanent", "5 MB", "firebase_hub", "Lossless image compression-free direct image host"),
    (59, "Tier 3: Storage & Object APIs", "Ultraimg", "https://ultraimg.com", "https://ultraimg.com/api/1/upload", "API Key", "Type B (Viewer)", "Permanent", "20 MB", "primary_blogger", "Chevereto image host with albums and privacy settings"),
    (60, "Tier 3: Storage & Object APIs", "ImgAdult", "https://imgadult.com", "Web / API", "Account", "Type B (Viewer)", "Permanent", "15 MB", "primary_blogger", "General media hosting node with permanent link preservation"),

    # Tier 4 — Public Publishing, Documentation & Static Image Galleries (61-80)
    (61, "Tier 4: Public Galleries & Docs", "GitHub Pages Gallery", "https://pages.github.com", "Git Push", "GitHub", "Type C (Clickable)", "Permanent", "1 GB (Repo)", "primary_blogger", "Interactive responsive image gallery on gazpearce.github.io/cctv-security-hub"),
    (62, "Tier 4: Public Galleries & Docs", "GitLab Pages Mirror", "https://gitlab.com", "Git CI/CD", "GitLab", "Type C (Clickable)", "Permanent", "10 GB", "primary_blogger", "Independent European git mirror hosting forensic tools and diagrams"),
    (63, "Tier 4: Public Galleries & Docs", "Cloudflare Pages", "https://pages.cloudflare.com", "Git Integration", "Cloudflare", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Global edge mirror serving WebP trade assets with immutable cache"),
    (64, "Tier 4: Public Galleries & Docs", "Firebase Hosting Edge", "https://firebase.google.com", "Firebase CLI", "Google OAuth", "Type C (Clickable)", "Permanent", "10 GB", "primary_blogger", "High-speed Google edge CDN on gary-pearce-forensic-hub.web.app"),
    (65, "Tier 4: Public Galleries & Docs", "Vercel Previews", "https://vercel.com", "Git Integration", "GitHub/Google", "Type C (Clickable)", "Permanent", "100 GB/mo", "firebase_hub", "Serverless edge frontend hosting with automated Git deployments"),
    (66, "Tier 4: Public Galleries & Docs", "Netlify Static", "https://netlify.com", "Git Integration", "GitHub/Google", "Type C (Clickable)", "Permanent", "100 GB/mo", "firebase_hub", "Edge static deployment with custom redirects and headers"),
    (67, "Tier 4: Public Galleries & Docs", "Render Static", "https://render.com", "Git Integration", "GitHub/GitLab", "Type C (Clickable)", "Permanent", "100 GB/mo", "firebase_hub", "Static site and asset hosting connected to git repository"),
    (68, "Tier 4: Public Galleries & Docs", "Codeberg Pages", "https://codeberg.page", "Git Integration", "Codeberg", "Type C (Clickable)", "Permanent", "Free/Donation", "github_open_source_repo", "Non-profit open-source git platform hosted in the EU"),
    (69, "Tier 4: Public Galleries & Docs", "SourceHut Pages", "https://sr.ht", "Git/Hg Push", "SourceHut", "Type C (Clickable)", "Permanent", "Free Tier", "github_open_source_repo", "Fast, bloat-free software development platform"),
    (70, "Tier 4: Public Galleries & Docs", "Neocities", "https://neocities.org", "CLI / Web", "API Key", "Type C (Clickable)", "Permanent", "1 GB", "primary_blogger", "Independent web hosting with active retro-web tech community"),
    (71, "Tier 4: Public Galleries & Docs", "Google Sites", "https://sites.google.com", "Google Suite", "Google OAuth", "Type C (Clickable)", "Permanent", "15 GB", "primary_blogger", "Tier-2 Citadel site embedding Google Drive drawings and trade galleries"),
    (72, "Tier 4: Public Galleries & Docs", "Notion Public Pages", "https://notion.so", "Notion API", "Internal Integration", "Type C (Clickable)", "Permanent", "Unlimited", "google_drive_vault", "Publicly shared knowledge base documenting CCTV & Starlink engineering"),
    (73, "Tier 4: Public Galleries & Docs", "GitBook Manuals", "https://gitbook.com", "Git Sync", "GitHub/GitLab", "Type C (Clickable)", "Permanent", "Open Source", "github_open_source_repo", "Technical documentation portal embedding installation guides and photos"),
    (74, "Tier 4: Public Galleries & Docs", "Read the Docs", "https://readthedocs.org", "Webhook / Git", "GitHub/GitLab", "Type C (Clickable)", "Permanent", "Free for OS", "github_open_source_repo", "Sphinx/MkDocs automated technical manual builds"),
    (75, "Tier 4: Public Galleries & Docs", "Docusaurus", "https://docusaurus.io", "Static Build", "Node / Git", "Type C (Clickable)", "Permanent", "Client-Side", "github_open_source_repo", "Modern React documentation framework with image optimization"),
    (76, "Tier 4: Public Galleries & Docs", "MkDocs Material", "https://squidfunk.github.io/mkdocs-material/", "Static Build", "Python / Git", "Type C (Clickable)", "Permanent", "Client-Side", "gitlab_open_source_repo", "Technical documentation generator with lightbox image galleries"),
    (77, "Tier 4: Public Galleries & Docs", "Substack Newsletter", "https://substack.com", "Web / Email", "Account", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Dedicated trade newsletter featuring Yorkshire telecom case studies"),
    (78, "Tier 4: Public Galleries & Docs", "PBase Galleries", "https://pbase.com", "Web / Tool", "Account", "Type B (Viewer)", "Paid / Trial", "500 MB", "primary_blogger", "Traditional photographic community gallery"),
    (79, "Tier 4: Public Galleries & Docs", "Ipernity", "https://ipernity.com", "Web", "Account", "Type B (Viewer)", "Free / Club", "200 MB", "primary_blogger", "Independent non-profit photography sharing network"),
    (80, "Tier 4: Public Galleries & Docs", "Fotki", "https://fotki.com", "Web / FTP", "Account", "Type B (Viewer)", "Free Tier", "Limited", "primary_blogger", "Photo sharing community with photo printing and album features"),

    # Tier 5 — Discovery Candidates & Extended Image Ecosystem (81-100)
    (81, "Tier 5: Extended Ecosystem", "Exposure", "https://exposure.co", "Web Editor", "Account", "Type C (Clickable)", "Trial / Tier", "Story Based", "primary_blogger", "Visual storytelling platform for field installations"),
    (82, "Tier 5: Extended Ecosystem", "Fine Art America", "https://fineartamerica.com", "Web Contributor", "Account", "Type C (Clickable)", "Permanent", "Portfolio", "primary_blogger", "Commercial art and architectural photography marketplace"),
    (83, "Tier 5: Extended Ecosystem", "OpenStreetMap Wiki", "https://wiki.openstreetmap.org", "MediaWiki API", "OSM Account", "Type C (Clickable)", "Permanent", "Community", "primary_blogger", "Community geo-mapping documentation and equipment nodes"),
    (84, "Tier 5: Extended Ecosystem", "Surge.sh Portfolio", "https://surge.sh", "CLI Deploy", "CLI Token", "Type C (Clickable)", "Permanent", "Unlimited", "primary_blogger", "Instant command-line static photo book deployment"),
    (85, "Tier 5: Extended Ecosystem", "Tiiny Host Single-Page", "https://tiiny.host", "Web / DragDrop", "Account", "Type C (Clickable)", "Permanent", "1 Site Free", "primary_blogger", "Single-file interactive image slider landing page"),
    (86, "Tier 5: Extended Ecosystem", "Carrd Card", "https://carrd.co", "Web Builder", "Account", "Type C (Clickable)", "Permanent", "3 Sites Free", "primary_blogger", "Responsive micro-portfolio with gallery grid and Gary Pearce CTAs"),
    (87, "Tier 5: Extended Ecosystem", "Framer Visual Showcase", "https://framer.com", "Web / App", "Account", "Type C (Clickable)", "Permanent", "Free Tier", "primary_blogger", "Fluid spring physics visual portfolio on framer.app"),
    (88, "Tier 5: Extended Ecosystem", "Webflow Agency Grid", "https://webflow.com", "Visual Designer", "Account", "Type C (Clickable)", "Permanent", "2 Projects Free", "primary_blogger", "Cybernetic glassmorphic image showcase on webflow.io"),
    (89, "Tier 5: Extended Ecosystem", "Wix Site Media", "https://wix.com", "Visual Builder", "Account", "Type C (Clickable)", "Permanent", "500 MB Free", "primary_blogger", "Secondary local authority citation with embedded trade gallery"),
    (90, "Tier 5: Extended Ecosystem", "CodePen Interactive Canvas", "https://codepen.io", "Web Editor", "GitHub", "Type C (Clickable)", "Permanent", "Unlimited", "github_open_source_repo", "Interactive HTML/CSS/JS comparison sliders (Before/After)"),
    (91, "Tier 5: Extended Ecosystem", "JSFiddle Interactive Lens", "https://jsfiddle.net", "Web Editor", "GitHub", "Type C (Clickable)", "Permanent", "Unlimited", "github_open_source_repo", "Interactive DORI lens field of view diagram canvas"),
    (92, "Tier 5: Extended Ecosystem", "Observable HQ D3 Graphics", "https://observablehq.com", "Notebook API", "GitHub", "Type C (Clickable)", "Permanent", "Unlimited", "github_open_source_repo", "Interactive D3.js vector visualizations for wind loads and cabling"),
    (93, "Tier 5: Extended Ecosystem", "Google Colab Math Proofs", "https://colab.research.google.com", "Google Suite", "Google OAuth", "Type C (Clickable)", "Permanent", "Free Compute", "google_drive_vault", "Jupyter notebook with embedded CCTV forensic calculations and photos"),
    (94, "Tier 5: Extended Ecosystem", "Kaggle Telemetry Datasets", "https://kaggle.com/datasets", "Kaggle API", "Google OAuth", "Type C (Clickable)", "Permanent", "20 GB", "primary_blogger", "UK Police crime data and camera placement telemetry notebook"),
    (95, "Tier 5: Extended Ecosystem", "Hugging Face Model Visuals", "https://huggingface.co", "Git / Python", "HF Token", "Type C (Clickable)", "Permanent", "Free Spaces", "github_open_source_repo", "Gradio image processing demo highlighting low-light ColorVu apertures"),
    (96, "Tier 5: Extended Ecosystem", "DailyMotion Video Thumbnails", "https://dailymotion.com", "Video Upload API", "Partner Account", "Type C (Clickable)", "Permanent", "Unlimited", "youtube_channel", "1080p field debrief video cards with high-res trade covers"),
    (97, "Tier 5: Extended Ecosystem", "Vimeo Showcase Posters", "https://vimeo.com", "Vimeo API", "OAuth 2.0", "Type C (Clickable)", "Permanent", "Free Tier", "youtube_channel", "Commercial video portfolio with custom video thumbnail cards"),
    (98, "Tier 5: Extended Ecosystem", "Podbean Podcast Artwork", "https://podbean.com", "RSS / API", "Account", "Type C (Clickable)", "Permanent", "5 Hours Free", "primary_blogger", "1400x1400 square cover art for ADI Technical Audio Debriefs"),
    (99, "Tier 5: Extended Ecosystem", "Bluesky Social Posts", "https://bsky.app", "AT Protocol API", "App Password", "Type C (Clickable)", "Permanent", "Decentralized", "primary_blogger", "Live trade field dispatches with multi-image embeds on AT-Proto"),
    (100, "Tier 5: Extended Ecosystem", "Mastodon Fediverse Posts", "https://joinmastodon.org", "ActivityPub REST", "Bearer Token", "Type C (Clickable)", "Permanent", "Decentralized", "primary_blogger", "Federated telecom engineering updates with high-res WebP attachments")
]

for p in raw_platforms:
    registry["platforms"].append({
        "id": p[0],
        "tier": p[1],
        "name": p[2],
        "canonical_url": p[3],
        "api_endpoint_or_method": p[4],
        "auth_type": p[5],
        "capability_type": p[6],
        "retention_policy": p[7],
        "file_or_rate_limit": p[8],
        "google_shield_anchor": p[9],
        "engineering_notes": p[10]
    })

target_file = r"C:\Users\Gary\github-cctv-seo\image_stack_registry.json"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {target_file}")
print(f"Total image platforms registered: {len(registry['platforms'])}")
