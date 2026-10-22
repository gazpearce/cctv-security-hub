import asyncio
import json
import re
import urllib.request
import websockets
import time

CDP_BASE = "http://127.0.0.1:9223"

async def get_latest_verification_data():
    """Reads the active Gmail inbox tab via CDP and extracts verification links and 6-digit codes."""
    req = urllib.request.Request(f"{CDP_BASE}/json/list")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
        
    mail_tab = next((t for t in tabs if t.get("url", "").startswith("https://mail.google.com/")), None)
    if not mail_tab:
        print("[EMAIL-VERIFIER] No active Gmail tab found on port 9223")
        return None
        
    ws_url = mail_tab.get("webSocketDebuggerUrl")
    print(f"[EMAIL-VERIFIER] Inspecting inbox tab: {mail_tab.get('title')}")
    
    try:
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            extract_js = '''
            (() => {
                const rows = Array.from(document.querySelectorAll('tr[role=row], div[role=main] tr'));
                return rows.slice(0, 15).map(r => ({
                    sender: r.querySelector('span[email], td[role=gridcell]:nth-child(4)')?.innerText || '',
                    snippet: (r.innerText || r.textContent || '').replace(/\\s+/g, ' ').trim()
                }));
            })()
            '''
            msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": extract_js, "returnByValue": True}}
            await ws.send(json.dumps(msg))
            resp = await ws.recv()
            emails = json.loads(resp).get("result", {}).get("result", {}).get("value", [])
            
            print(f"[EMAIL-VERIFIER] Found {len(emails)} recent emails in inbox:")
            results = []
            for e in emails:
                snip = e.get("snippet", "")
                # Find 6-digit verification code
                code_match = re.search(r'\b(\d{6})\b', snip)
                # Find verification keywords
                is_verify = any(k in snip.lower() for k in ["verify", "verification", "confirm", "code", "activate", "welcome"])
                if is_verify:
                    code = code_match.group(1) if code_match else None
                    results.append({"text": snip[:100], "code": code})
                    safe_snip = snip[:80].encode("ascii", "replace").decode("ascii")
                    print(f"  -> [MATCH] {safe_snip} | Code: {code}")
                    
            return results
    except Exception as e:
        print(f"[EMAIL-VERIFIER] Error reading inbox: {e}")
        return None

if __name__ == "__main__":
    asyncio.run(get_latest_verification_data())
