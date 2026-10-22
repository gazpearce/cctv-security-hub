import urllib.request
import re

articles = [
    "https://medium.com/@garypearce.homesecurity/hikvision-or-dahua-honest-breakdown-after-installing-both-for-years-9ae766765cfc",
    "https://medium.com/@garypearce.homesecurity/how-do-i-reset-a-forgotten-password-on-a-hikvision-nvr-5c86e09c5963",
    "https://medium.com/@garypearce.homesecurity/what-cctv-actually-costs-in-halifax-from-someone-who-fits-it-ceca7360a09b",
    "https://medium.com/@garypearce.homesecurity/why-copper-clad-aluminium-cca-cat6-cables-ruin-uk-poe-cctv-systems-5068e3d30f65",
    "https://medium.com/@garypearce.homesecurity/best-no-subscription-cctv-system-uk-gary-pearce-real-installer-advice-931b80981ed6"
]

for url in articles:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        links = re.findall(r'href=[\'"]([^\'"]+)[\'"]', html)
        adi_links = [l for l in links if 'adicommunications' in l.lower()]
        print(f"Article: {url.split('/')[-1][:30]}")
        print(f"  Total links: {len(links)}, ADI links: {adi_links}")
    except Exception as e:
        print(f"Error fetching {url}: {e}")
