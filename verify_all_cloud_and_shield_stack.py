import urllib.request
import urllib.error
import re
import time

urls_to_test = [
    # Tier 1: Cloud Stacks
    ("Netlify Edge CDN", "https://adi-cctv-security-hub.netlify.app/"),
    ("Surge Global Edge Hub", "https://adi-cctv-security-hub.surge.sh/"),
    ("Surge Starlink Finder", "https://adi-starlink-mount-finder.surge.sh/"),
    ("GitHub Pages Hub", "https://gazpearce.github.io/cctv-security-hub/"),
    ("GitHub Pages Starlink Finder", "https://gazpearce.github.io/starlink-mount-finder/"),
    ("GitHub Pages Crime Checker", "https://gazpearce.github.io/uk-postcode-crime-checker/"),
    ("GitHub Pages CCTV DORI", "https://gazpearce.github.io/cctv-lens-dori-tool/"),
    ("GitHub Pages Wind Load", "https://gazpearce.github.io/starlink-wind-load-calculator/"),
    ("GitHub Pages Ajax Selector", "https://gazpearce.github.io/ajax-smart-alarms-selector/"),
    ("GitHub Pages PoE Drop", "https://gazpearce.github.io/poe-voltage-drop-calculator/"),
    ("Cloudflare Pages Edge", "https://gary-pearce-home-services.pages.dev/"),
    ("Google Firebase Hosting", "https://gary-pearce-forensic-hub.web.app/"),
    ("GitLab Cloud Repository", "https://gitlab.com/aiagent1510/cctv-security-hub"),
    
    # Tier 2: Google Shield Buffer (Rule 45)
    ("Google Shield Blogger Hub", "https://tvandhomesecurity.blogspot.com/"),
    ("Google Drive CAD Vault", "https://drive.google.com/drive/folders/1jkTPHdni9Bki3kwNbna5d5oK2ejPJf88"),
    ("Blogger: Hikvision ColorVu Post", "https://tvandhomesecurity.blogspot.com/2026/10/hikvision-colorvu-vs-infrared-cctv-4k.html"),
    ("Blogger: TV Fireplace Post", "https://tvandhomesecurity.blogspot.com/2026/10/can-you-mount-tv-above-fireplace-safely.html"),
    ("Blogger: Ajax Smart Alarms Post", "https://tvandhomesecurity.blogspot.com/2026/10/ajax-smart-alarms-uk-masterclass-2026.html"),
    ("Blogger: Starlink vs 4G/5G Post", "https://tvandhomesecurity.blogspot.com/2026/10/starlink-vs-4g5g-rural-home-broadband.html"),
    ("Blogger: Starlink Chimney Post", "https://tvandhomesecurity.blogspot.com/2026/10/starlink-installation-uk-chimney-mount.html"),

    # Tier 3: Primary Money Pages
    ("ADI Communications Primary Root", "https://adicommunications.co.uk/"),
    ("ADI Starlink Installation UK", "https://adicommunications.co.uk/starlink-internet-installation/"),
    ("ADI CCTV Installation UK", "https://adicommunications.co.uk/cctv-installation/"),
    ("ADI TV Wall Mounting UK", "https://adicommunications.co.uk/tv-wall-mounting/"),
    ("ADI Network & Data Cabling", "https://adicommunications.co.uk/network-data-cabling/")
]

results = []
print("================================================================================")
print("AUDITING FULL CLOUD STACK -> GOOGLE SHIELD -> ADI COMMUNICATIONS BACKLINK LOOP")
print("================================================================================\n")

for label, url in urls_to_test:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    )
    status = None
    links_to_shield = 0
    links_to_adi = 0
    err_msg = ""
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status = resp.status
            html = resp.read().decode('utf-8', errors='ignore')
            links = re.findall(r'href=[\'"](https?://[^\'"\s>]+)', html)
            for l in links:
                if 'blogspot.com' in l or 'drive.google.com' in l:
                    links_to_shield += 1
                if 'adicommunications.co.uk' in l:
                    links_to_adi += 1
    except urllib.error.HTTPError as e:
        status = e.code
    except Exception as e:
        err_msg = str(e)

    status_str = f"HTTP {status}" if status else f"ERR: {err_msg}"
    print(f"[{status_str:^10}] {label:<35} | Links -> Shield: {links_to_shield:<2} | Links -> ADI: {links_to_adi:<2}")
    results.append({
        "label": label,
        "url": url,
        "status": status,
        "links_to_shield": links_to_shield,
        "links_to_adi": links_to_adi
    })

print("\n================================================================================")
total_tested = len(results)
http_200_count = sum(1 for r in results if r["status"] == 200)
print(f"TOTAL ENDPOINTS TESTED: {total_tested} | HTTP 200 SUCCESS: {http_200_count} ({http_200_count/total_tested*100:.1f}%)")
print("================================================================================")
