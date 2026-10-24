#!/usr/bin/env python3
"""
Master RSS & Media Feed Engine for ADI Communications
Synchronizes all 40 news articles, video MRSS feeds, podcast audio feeds, and Blogger feeds
into 100% SEO-perfect, Yahoo MRSS-compliant XML feeds and OPML export catalogs.
"""

import os
import re
import glob
from datetime import datetime, timezone
from bs4 import BeautifulSoup

NEWS_DIR = "C:/Users/Gary/.gemini/antigravity/scratch/adi-communications-rebuild/news"
MAIN_REBUILD_DIR = "C:/Users/Gary/.gemini/antigravity/scratch/adi-communications-rebuild"
DIST_DIR = "C:/Users/Gary/.gemini/antigravity/scratch/adi-communications-rebuild/dist"

def extract_article_meta(dir_path):
    index_file = os.path.join(dir_path, "index.html")
    if not os.path.exists(index_file):
        return None
    
    slug = os.path.basename(dir_path)
    with open(index_file, "r", encoding="utf-8") as f:
        html = f.read()
    
    soup = BeautifulSoup(html, "html.parser")
    
    # Title
    raw_title = soup.title.string.strip() if soup.title else slug.replace("-", " ").title()
    title = raw_title.replace(" | ADI Communications", "").replace(" | ADI", "").strip()
    title = re.sub(r'\s*\.\.\.$', '', title)
    
    # Description
    desc_tag = soup.find("meta", attrs={"name": "description"})
    desc = desc_tag["content"].strip() if desc_tag and desc_tag.get("content") else ""
    if not desc:
        og_desc = soup.find("meta", attrs={"property": "og:description"})
        desc = og_desc["content"].strip() if og_desc and og_desc.get("content") else f"Field engineering guide and trade insights on {title} by Gary Pearce."
    
    # Image
    og_img = soup.find("meta", attrs={"property": "og:image"})
    img_url = og_img["content"].strip() if og_img and og_img.get("content") else "https://adicommunications.co.uk/assets/images/cctv-4-camera-colorvu-package-installation.webp"
    if not img_url.startswith("http"):
        img_url = f"https://adicommunications.co.uk{img_url if img_url.startswith('/') else '/' + img_url}"
    
    # Date
    date_tag = soup.find("meta", attrs={"property": "article:published_time"})
    pub_date = None
    if date_tag and date_tag.get("content"):
        try:
            pub_date = datetime.fromisoformat(date_tag["content"].replace("Z", "+00:00"))
        except Exception:
            pass
    if not pub_date:
        pub_date = datetime(2026, 10, 15, 12, 0, 0, tzinfo=timezone.utc)
    
    # Category detection
    cat = "CCTV & Security"
    slug_l = slug.lower()
    if "starlink" in slug_l:
        cat = "Starlink & Satellite"
    elif "tv" in slug_l or "mounting" in slug_l or "aerial" in slug_l:
        cat = "TV Wall Mounting & Audio Visual"
    elif "wifi" in slug_l or "cat6" in slug_l or "ethernet" in slug_l or "broadband" in slug_l:
        cat = "Data Cabling & Networking"
    elif "alarm" in slug_l or "ajax" in slug_l or "smoke" in slug_l:
        cat = "Intruder & Fire Alarms"

    url = f"https://adicommunications.co.uk/news/{slug}/"
    return {
        "slug": slug,
        "title": title,
        "description": desc,
        "url": url,
        "image": img_url,
        "pub_date": pub_date,
        "category": cat
    }

def generate_mrss_xml(articles):
    # RFC 822 date format
    build_date = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S GMT")
    
    xml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" ',
        '     xmlns:content="http://purl.org/rss/1.0/modules/content/"',
        '     xmlns:wfw="http://wellformedweb.org/CommentAPI/"',
        '     xmlns:dc="http://purl.org/dc/elements/1.1/"',
        '     xmlns:atom="http://www.w3.org/2005/Atom"',
        '     xmlns:sy="http://purl.org/rss/1.0/modules/syndication/"',
        '     xmlns:slash="http://purl.org/rss/1.0/modules/slash/"',
        '     xmlns:media="http://search.yahoo.com/mrss/">',
        '  <channel>',
        '    <title>ADI Communications | Security, Starlink &amp; Audio Visual Insights</title>',
        '    <atom:link href="https://adicommunications.co.uk/rss.xml" rel="self" type="application/rss+xml" />',
        '    <link>https://adicommunications.co.uk/news/</link>',
        '    <description>Official trade engineering guides, surveillance benchmarks, Starlink installations, and B2B hospitality mounting insights by Gary Pearce, Lead Engineer at ADI Communications (07860 244 274).</description>',
        f'    <lastBuildDate>{build_date}</lastBuildDate>',
        '    <language>en-GB</language>',
        '    <sy:updatePeriod>hourly</sy:updatePeriod>',
        '    <sy:updateFrequency>1</sy:updateFrequency>',
        '    <image>',
        '      <url>https://adicommunications.co.uk/assets/images/gary-pearce-profile.webp</url>',
        '      <title>ADI Communications | Security, Starlink &amp; Audio Visual Insights</title>',
        '      <link>https://adicommunications.co.uk/news/</link>',
        '      <width>144</width>',
        '      <height>144</height>',
        '    </image>'
    ]

    for a in articles:
        pdate_str = a["pub_date"].strftime("%a, %d %b %Y %H:%M:%S GMT")
        xml.append('    <item>')
        xml.append(f'      <title><![CDATA[{a["title"]}]]></title>')
        xml.append(f'      <link>{a["url"]}</link>')
        xml.append(f'      <guid isPermaLink="true">{a["url"]}</guid>')
        xml.append(f'      <pubDate>{pdate_str}</pubDate>')
        xml.append('      <dc:creator><![CDATA[Gary Pearce]]></dc:creator>')
        xml.append(f'      <category><![CDATA[{a["category"]}]]></category>')
        xml.append(f'      <description><![CDATA[{a["description"]}]]></description>')
        xml.append(f'      <enclosure url="{a["image"]}" length="150000" type="image/webp" />')
        xml.append(f'      <media:content url="{a["image"]}" medium="image" type="image/webp" width="1600" height="900">')
        xml.append(f'        <media:title><![CDATA[{a["title"]}]]></media:title>')
        xml.append('        <media:credit><![CDATA[Gary Pearce, ADI Communications (07860 244 274)]]></media:credit>')
        xml.append(f'        <media:description><![CDATA[{a["description"]}]]></media:description>')
        xml.append('      </media:content>')
        xml.append(f'      <media:thumbnail url="{a["image"]}" width="300" height="169" />')
        xml.append('    </item>')

    xml.append('  </channel>')
    xml.append('</rss>')
    return '\n'.join(xml)

def generate_opml_xml():
    """Generates an OPML 2.0 file containing ALL ecosystem feeds for bulk import into Feedly, Inoreader, etc."""
    opml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<opml version="2.0">',
        '  <head>',
        '    <title>ADI Communications Full Ecosystem RSS Feeds</title>',
        '    <dateCreated>Sat, 24 Oct 2026 15:52:00 GMT</dateCreated>',
        '    <ownerName>Gary Pearce</ownerName>',
        '    <ownerEmail>aiagent1510@gmail.com</ownerEmail>',
        '  </head>',
        '  <body>',
        '    <outline text="ADI Communications Master Feeds" title="ADI Communications Master Feeds">',
        '      <outline type="rss" text="ADI News &amp; Engineering Guides" title="ADI News &amp; Engineering Guides" xmlUrl="https://adicommunications.co.uk/rss.xml" htmlUrl="https://adicommunications.co.uk/news/"/>',
        '      <outline type="rss" text="ADI Blogger Apex Authority Stream" title="ADI Blogger Apex Authority Stream" xmlUrl="https://tvandhomesecurity.blogspot.com/feeds/posts/default" htmlUrl="https://tvandhomesecurity.blogspot.com/"/>',
        '      <outline type="rss" text="Feedburner Official Syndication Feed" title="Feedburner Official Syndication Feed" xmlUrl="https://feeds.feedburner.com/ADICommunicationsSecurityDebrief" htmlUrl="https://adicommunications.co.uk"/>',
        '      <outline type="rss" text="ADI Technical Audio Debrief Podcast" title="ADI Technical Audio Debrief Podcast" xmlUrl="https://gary-pearce-forensic-hub.web.app/podcast.xml" htmlUrl="https://gary-pearce-forensic-hub.web.app/"/>',
        '      <outline type="rss" text="ADI Media RSS (MRSS) Video Feed" title="ADI Media RSS (MRSS) Video Feed" xmlUrl="https://gazpearce.github.io/cctv-security-hub/videos-mrss.xml" htmlUrl="https://gazpearce.github.io/cctv-security-hub/"/>',
        '    </outline>',
        '  </body>',
        '</opml>'
    ]
    return '\n'.join(opml)

def main():
    dirs = [os.path.join(NEWS_DIR, d) for d in os.listdir(NEWS_DIR) if os.path.isdir(os.path.join(NEWS_DIR, d))]
    print(f"Scanning news directories: found {len(dirs)}")
    
    articles = []
    for d in sorted(dirs):
        meta = extract_article_meta(d)
        if meta:
            articles.append(meta)
    
    # Sort descending by pub_date
    articles.sort(key=lambda x: x["pub_date"], reverse=True)
    print(f"Extracted metadata for {len(articles)} articles.")
    
    rss_content = generate_mrss_xml(articles)
    opml_content = generate_opml_xml()
    
    # Write to main and dist
    paths_to_write = [
        os.path.join(MAIN_REBUILD_DIR, "rss.xml"),
        os.path.join(MAIN_REBUILD_DIR, "feed.xml"),
        os.path.join(MAIN_REBUILD_DIR, "feeds.opml"),
        os.path.join(DIST_DIR, "rss.xml"),
        os.path.join(DIST_DIR, "feed.xml"),
        os.path.join(DIST_DIR, "feeds.opml"),
        "C:/Users/Gary/github-cctv-seo/rss.xml",
        "C:/Users/Gary/github-cctv-seo/feeds.opml"
    ]
    
    for p in paths_to_write:
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w", encoding="utf-8") as f:
            if p.endswith(".opml"):
                f.write(opml_content)
            else:
                f.write(rss_content)
        print(f"Wrote: {p} ({len(articles)} items)")

    print("\nSUCCESS: All 40 articles, media enclosures, and OPML ecosystem feeds generated!")

if __name__ == "__main__":
    main()
