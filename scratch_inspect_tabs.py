import urllib.request
import json
import sys

def inspect_tabs():
    resp = urllib.request.urlopen('http://localhost:9223/json')
    tabs = json.loads(resp.read().decode('utf-8'))
    interesting = ['github', 'rumble', 'dailymotion', 'odysee', 'vimeo', 'archive.org', 'resend', 'medium', 'notion', 'hashnode', 'substack', 'reddit', 'x.com', 'twitter', 'grok']
    
    print(f"Total open tabs: {len(tabs)}")
    found = []
    for t in tabs:
        url = t.get('url', '').lower()
        if any(k in url for k in interesting):
            found.append(t)
            
    for t in found:
        safe_title = t.get('title', '').encode('ascii', errors='replace').decode()
        print(f"ID: {t.get('id')} | Title: {safe_title[:45]} | URL: {t.get('url')[:80]}")

if __name__ == '__main__':
    inspect_tabs()
