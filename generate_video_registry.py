import json
import os

registry = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "version": "1.0.0",
    "last_updated": "2026-10-22T09:05:00+01:00",
    "title": "ADI Communications & Gary Pearce — Master Video, Document & Multi-Media Stacking Registry",
    "description": "Comprehensive directory of 50 video, presentation, document, and audio platforms categorized by hosting capability, syndication API, Docker infrastructure, and Rule 45 Google Shield links.",
    "classification_standard": {
        "video_hosting": "Upload video and receive a public watch page or embeddable HLS/DASH stream.",
        "video_syndication": "Publish video with rich description, chapters, and clickable backlink to Google Shield properties.",
        "video_infrastructure": "Free/open-source Docker and self-hosted tools to transcode, store, and stream without external fees."
    },
    "rule_45_shield_anchors": {
        "primary_blogger": "https://tvandhomesecurity.blogspot.com/",
        "google_drive_vault": "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88",
        "youtube_verified": "https://www.youtube.com/@CCTV.services",
        "firebase_hub": "https://gary-pearce-forensic-hub.web.app/",
        "buffer_posts": {
            "cctv_colorvu_dori": "https://adicommunications.co.uk/news/hikvision-colorvu-vs-infrared-night-vision/",
            "starlink_chimney_apex": "https://adicommunications.co.uk/news/starlink-chimney-mount-vs-roof-apex/",
            "ajax_wireless_alarm": "https://adicommunications.co.uk/news/ajax-wireless-alarm-grade-2-installation/",
            "ethernet_upstairs": "https://adicommunications.co.uk/news/how-to-get-ethernet-upstairs-without-running-cables/",
            "tv_above_fireplace": "https://adicommunications.co.uk/news/tv-above-fireplace-safe-installation/"
        }
    },
    "platforms": []
}

raw_platforms = [
    # Tier 1 — Public Video Platforms with Upload APIs (1-8)
    (1, "Tier 1: Public Video Platforms", "YouTube", "https://youtube.com", "YouTube Data API v3", "OAuth 2.0", "Public Watch Page & Embed", "Permanent", "10,000 units/day", "primary_blogger", "Channel @CCTV.services; high DA entity hub with timestamped chapters"),
    (2, "Tier 1: Public Video Platforms", "Dailymotion", "https://dailymotion.com", "REST Video Upload API", "OAuth 2.0", "Public Video Page & Embed", "Permanent", "96 videos/day", "youtube_verified", "Secondary public video parasite passing high referral trust"),
    (3, "Tier 1: Public Video Platforms", "Vimeo", "https://vimeo.com", "Vimeo REST API", "OAuth 2.0 / Bearer", "Clean Showcase Page", "Permanent", "500MB/week free", "youtube_verified", "Professional trade portfolio player with high visual fidelity"),
    (4, "Tier 1: Public Video Platforms", "PeerTube", "https://joinpeertube.org", "PeerTube REST API / CLI", "OAuth 2.0 / User Token", "Federated Watch Page", "Permanent", "Instance Dependent", "primary_blogger", "Decentralized ActivityPub video network with WebTorrent P2P streaming"),
    (5, "Tier 1: Public Video Platforms", "Internet Archive Video", "https://archive.org", "S3-Compatible Upload API", "IAS3 Access Keys", "Public Item Archive Page", "Permanent", "Unlimited (Fair Use)", "primary_blogger", "Permanent historical archival with Dublin Core XML schemas (DA 96)"),
    (6, "Tier 1: Public Video Platforms", "Rumble", "https://rumble.com", "Rumble Video API", "Account Key", "Public Watch Page", "Permanent", "Unlimited", "youtube_verified", "Independent video network with search discovery and embeddable player"),
    (7, "Tier 1: Public Video Platforms", "Odysee / LBRY", "https://odysee.com", "LBRY SDK / API", "Auth Token", "Blockchain-Indexed Page", "Permanent", "Unlimited", "youtube_verified", "Decentralized blockchain video indexed by search engines"),
    (8, "Tier 1: Public Video Platforms", "Twitch", "https://twitch.tv", "Twitch Helix API", "OAuth 2.0", "Public Channel / VODs", "14 Days (VOD)", "Broadcaster", "youtube_verified", "Live hardware testing, live cable sweeps, and RF jammer spectrum demos"),

    # Tier 2 — Video Hosting, Delivery APIs & Specialized Clouds (9-25)
    (9, "Tier 2: Specialized Video APIs", "VCDN", "https://vcdn.me", "REST API / SDK", "API Key", "Public Video Playback", "Permanent", "Free Tier", "firebase_hub", "Free video hosting with public playback and developer SDKs"),
    (10, "Tier 2: Specialized Video APIs", "VdoHide", "https://vdohide.com", "Remote Upload API", "Account Token", "Embed & Watch Page", "Permanent", "Free Tier", "firebase_hub", "Free video hosting, responsive embeds, and bulk remote uploads"),
    (11, "Tier 2: Specialized Video APIs", "UFOLOAD", "https://ufoload.com", "API / FTP / WebDAV", "Account Key", "Direct Video Link", "Permanent", "Free Tier", "firebase_hub", "High-capacity file and video storage with FTP automation"),
    (12, "Tier 2: Specialized Video APIs", "Uqload", "https://uqload.vc", "Remote Upload API", "Account Key", "Public Video Embed", "Permanent", "Free Tier", "firebase_hub", "Video hosting and remote upload API for streaming distribution"),
    (13, "Tier 2: Specialized Video APIs", "Vidguard", "https://vidguard.to", "REST API", "Account Key", "Streaming Player", "Permanent", "Free Tier", "firebase_hub", "Fast video file streaming engine with direct API upload support"),
    (14, "Tier 2: Specialized Video APIs", "VidMoly", "https://vidmoly.me", "REST / Web", "Account", "Public Video Page", "Permanent", "Free Tier", "firebase_hub", "Public video hosting with high retention for technical debriefs"),
    (15, "Tier 2: Specialized Video APIs", "Vidoza", "https://vidoza.net", "Upload API", "Account Token", "Public Video Link", "Permanent", "Free Tier", "firebase_hub", "Remote video upload and streaming API with embed codes"),
    (16, "Tier 2: Specialized Video APIs", "Viddler", "https://viddler.com", "REST API", "API Key", "Hosted Video Page", "Permanent", "Free Allowance", "firebase_hub", "Enterprise video portal with developer API support"),
    (17, "Tier 2: Specialized Video APIs", "Streamable", "https://streamable.com", "Streamable REST API", "Basic Auth", "Public Clip Page", "90 Days (Free)", "10 mins/file", "firebase_hub", "Fast 1080p short video clip sharing and responsive embeds"),
    (18, "Tier 2: Specialized Video APIs", "Jumpshare", "https://jumpshare.com", "API / App", "Account", "Shareable Video Page", "Permanent", "2 GB Free", "firebase_hub", "Visual file sharing and screencast recordings with instant links"),
    (19, "Tier 2: Specialized Video APIs", "Loom", "https://loom.com", "Loom SDK / App", "OAuth", "Public Watch Page", "Permanent", "25 videos free", "primary_blogger", "Screen and webcam video debriefs documenting client site diagnostics"),
    (20, "Tier 2: Specialized Video APIs", "Cloudinary Video", "https://cloudinary.com", "Upload & Admin API", "API Key / Secret", "Transcoded HLS / MP4", "Permanent", "25 credits/mo", "firebase_hub", "Automated video transcoding, dynamic watermarks, and fast CDN delivery"),
    (21, "Tier 2: Specialized Video APIs", "Mux Video", "https://mux.com", "Mux Video REST API", "Token / Secret", "Hosted Stream & Player", "Free Trial / Usage", "$100 Credit", "firebase_hub", "Developer video API delivering broadcast-grade HLS streaming"),
    (22, "Tier 2: Specialized Video APIs", "api.video", "https://api.video", "api.video REST API", "API Key", "Public Player & HLS", "Permanent", "Free Sandbox", "firebase_hub", "End-to-end video infrastructure API with instant playback"),
    (23, "Tier 2: Specialized Video APIs", "Wistia", "https://wistia.com", "Wistia Upload API", "API Password", "Showcase Page & Embed", "Permanent", "3 videos free", "primary_blogger", "High-conversion video marketing player with interactive lead capture"),
    (24, "Tier 2: Specialized Video APIs", "VEED.io", "https://veed.io", "Web / API", "Account", "Public Share Link", "Permanent", "10 mins export", "youtube_verified", "Browser-based video creation, automatic British subtitles, and editing"),
    (25, "Tier 2: Specialized Video APIs", "Kapwing", "https://kapwing.com", "Web / Tool", "Account", "Shareable Video Page", "Permanent", "Free Tier", "youtube_verified", "Browser video studio for fast trade video aspect ratio conversions"),

    # Tier 3 — Open-Source Docker Video Servers & Infrastructure (26-35)
    (26, "Tier 3: Docker Video Infrastructure", "PeerTube Docker", "https://github.com/Chocobozzz/PeerTube", "REST API & CLI", "Localhost / Server", "Self-Hosted Watch Page", "Permanent", "Local Disk", "primary_blogger", "Self-hosted federated video platform with ActivityPub sync"),
    (27, "Tier 3: Docker Video Infrastructure", "MediaCMS Docker", "https://github.com/mediacms-io/mediacms", "REST API", "Localhost / Server", "Public Video Portal", "Permanent", "Local Disk", "primary_blogger", "Open-source YouTube alternative CMS with transcode queues and categories"),
    (28, "Tier 3: Docker Video Infrastructure", "Hovod", "https://github.com/Synapsr/Hovod", "REST Uploads", "Localhost / Server", "Self-Hosted HLS Player", "Permanent", "Local Disk", "firebase_hub", "Lightweight video hosting platform with automatic HLS transcoding"),
    (29, "Tier 3: Docker Video Infrastructure", "Owncast", "https://github.com/owncast/owncast", "RTMP Ingest / Web", "Localhost / Server", "Live Stream Player & Chat", "Permanent", "Local Disk", "youtube_verified", "Self-hosted live streaming server for live technical Q&A and field demos"),
    (30, "Tier 3: Docker Video Infrastructure", "OvenMediaEngine", "https://github.com/AirenSoft/OvenMediaEngine", "WebRTC / HLS / OVT", "Localhost / Server", "Sub-Second Live Video", "Permanent", "Local Disk", "firebase_hub", "Ultra-low latency streaming server for real-time camera CCTV feeds"),
    (31, "Tier 3: Docker Video Infrastructure", "SRS (Simple RTMP Server)", "https://github.com/ossrs/srs", "RTMP / WebRTC / HLS", "Localhost / Server", "Video Streaming Core", "Permanent", "Local Disk", "firebase_hub", "High-performance industrial video streaming engine"),
    (32, "Tier 3: Docker Video Infrastructure", "Restreamer", "https://github.com/datarhei/restreamer", "Web / API", "Localhost / Server", "Multi-Destination Stream", "Permanent", "Local Disk", "youtube_verified", "Routes a single local live camera feed simultaneously to YouTube and Twitch"),
    (33, "Tier 3: Docker Video Infrastructure", "Tube Archivist", "https://github.com/tubearchivist/tubearchivist", "Docker / Index", "Localhost / Server", "Video Archive Index", "Permanent", "Local Disk", "google_drive_vault", "Self-hosted YouTube and video backup index with elastic search"),
    (34, "Tier 3: Docker Video Infrastructure", "Jellyfin Media Server", "https://jellyfin.org", "REST API / DLNA", "Localhost / Server", "Private Media Library", "Permanent", "Local Disk", "firebase_hub", "Free software media system for managing and streaming high-bitrate video"),
    (35, "Tier 3: Docker Video Infrastructure", "FFmpeg Engine", "https://ffmpeg.org", "CLI / Python Subprocess", "Local Binary", "Video Transcoder & Slicer", "Permanent", "Local Disk", "firebase_hub", "Core engine for H.264/H.265 transcoding, WebP poster extraction, and audio muxing"),

    # Tier 4 — Presentation, Document & Infographic Stacking (36-45)
    (36, "Tier 4: Document & Slide Stacking", "Google Slides", "https://slides.google.com", "Google Slides API", "Google OAuth", "Public Presentation Embed", "Permanent", "15 GB (Google)", "primary_blogger", "16:9 interactive technical presentation deck embedded in Blogger and Sites"),
    (37, "Tier 4: Document & Slide Stacking", "SlideShare", "https://slideshare.net", "Web / Upload", "LinkedIn/Scribd", "Public Slide Document", "Permanent", "Unlimited", "primary_blogger", "High-DA slide directory for telecom and physical security whitepapers"),
    (38, "Tier 4: Document & Slide Stacking", "Speaker Deck", "https://speakerdeck.com", "Web / PDF Upload", "GitHub/Account", "Public PDF Slide Page", "Permanent", "Unlimited", "primary_blogger", "Clean developer-friendly presentation platform with high search authority"),
    (39, "Tier 4: Document & Slide Stacking", "Google Drive PDF Vault", "https://drive.google.com", "Google Drive API", "Google OAuth", "Public PDF Viewer (DA 100)", "Permanent", "15 GB (Google)", "primary_blogger", "Folder 1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88 hosting downloadable technical manuals"),
    (40, "Tier 4: Document & Slide Stacking", "Scribd", "https://scribd.com", "Web Upload", "Account", "Public Document Page", "Permanent", "Unlimited", "primary_blogger", "High-authority document repository for engineering schematics and guides"),
    (41, "Tier 4: Document & Slide Stacking", "Internet Archive Documents", "https://archive.org", "S3 API / CLI", "IAS3 Keys", "Permanent PDF Archive", "Permanent", "Unlimited", "primary_blogger", "Permanent public domain trade specifications and compliance records"),
    (42, "Tier 4: Document & Slide Stacking", "Observable HQ Visuals", "https://observablehq.com", "Notebook API", "GitHub", "Interactive D3.js Charts", "Permanent", "Unlimited", "primary_blogger", "Interactive lens field of view and wind vector computation graphs"),
    (43, "Tier 4: Document & Slide Stacking", "Tableau Public", "https://public.tableau.com", "Tableau Desktop / Web", "Account", "Public Interactive Dashboard", "Permanent", "10 GB", "primary_blogger", "UK Police recorded crime analytics and camera density correlation dashboards"),
    (44, "Tier 4: Document & Slide Stacking", "Flourish Studio", "https://flourish.studio", "Web / Embed", "Account", "Interactive Infographic", "Permanent", "Free Tier", "primary_blogger", "Responsive animated charts comparing Starlink vs Fibre speeds and latency"),
    (45, "Tier 4: Document & Slide Stacking", "Google Drawings", "https://docs.google.com/drawings", "Google API", "Google OAuth", "Scalable Vector Diagram", "Permanent", "15 GB", "primary_blogger", "Directly embeddable architectural system diagrams and cavity wall drop schematics"),

    # Tier 5 — Audio, Podcast & Feed Syndication Stacks (46-50)
    (46, "Tier 5: Audio & Syndication Stacks", "YouTube Podcasts", "https://podcasts.google.com", "YouTube Studio / RSS", "Google OAuth", "Google Search Podcast Hub", "Permanent", "Unlimited", "primary_blogger", "Official show on Channel UCt7VpJGmZZ12hdg2sCgjQag with search carousels"),
    (47, "Tier 5: Audio & Syndication Stacks", "Spotify for Creators", "https://creators.spotify.com", "Spotify Podcasters API", "Spotify Account", "Global Spotify Show Page", "Permanent", "Unlimited", "primary_blogger", "Global audio footprint streaming dual-engineer technical debriefs"),
    (48, "Tier 5: Audio & Syndication Stacks", "SoundCloud", "https://soundcloud.com", "SoundCloud REST API", "OAuth 2.0", "Waveform Audio Embed", "Permanent", "3 hours free", "primary_blogger", "Embeddable audio waveforms for quick website engineering briefings"),
    (49, "Tier 5: Audio & Syndication Stacks", "Podbean Podcast RSS", "https://podbean.com", "Podbean API / RSS", "Account", "Public Podcast Feed Page", "Permanent", "5 hours free", "primary_blogger", "Automated distribution feed syndicating to Apple Podcasts and Amazon Music"),
    (50, "Tier 5: Audio & Syndication Stacks", "RSSHub & n8n Feed", "https://github.com/DIYgod/RSSHub", "RSSHub Engine", "Localhost / Server", "Automated RSS Pipeline", "Permanent", "Localhost", "primary_blogger", "Automated feed engine broadcasting new posts and videos to syndication networks")
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
        "quota_or_rate_limit": p[8],
        "google_shield_anchor": p[9],
        "engineering_notes": p[10]
    })

target_file = r"C:\Users\Gary\github-cctv-seo\video_stack_registry.json"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(registry, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {target_file}")
print(f"Total video and multi-media platforms registered: {len(registry['platforms'])}")
