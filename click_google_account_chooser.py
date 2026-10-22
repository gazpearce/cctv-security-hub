import asyncio
import json
import urllib.request
import websockets

CDP_BASE = "http://127.0.0.1:9223"

async def click_google_tab(tab):
    title = tab.get("title", "")
    url = tab.get("url", "")
    ws_url = tab.get("webSocketDebuggerUrl")
    print(f"\n[GOOGLE-AUTH] Processing: {title} | {url[:60]}...")
    
    try:
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            js = '''
            (() => {
                const accounts = Array.from(document.querySelectorAll('div[data-identifier], div[role="link"], li[data-authuser]'));
                const aiagent = accounts.find(el => (el.innerText || el.textContent || '').includes('aiagent1510'));
                if (aiagent) {
                    aiagent.click();
                    return { clicked: true, text: 'aiagent1510 clicked' };
                }
                if (accounts.length > 0) {
                    accounts[0].click();
                    return { clicked: true, text: 'first account clicked' };
                }
                return { clicked: false };
            })()
            '''
            msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": js, "returnByValue": True}}
            await ws.send(json.dumps(msg))
            resp = await ws.recv()
            val = json.loads(resp).get("result", {}).get("result", {}).get("value")
            print(f"[GOOGLE-AUTH] Click result: {val}")
            await asyncio.sleep(6)
            
            msg["id"] = 2
            msg["params"]["expression"] = "window.location.href"
            await ws.send(json.dumps(msg))
            r2 = await ws.recv()
            post_url = json.loads(r2).get("result", {}).get("result", {}).get("value")
            print(f"[GOOGLE-AUTH] Post URL: {post_url}")
            return post_url
    except Exception as e:
        print(f"[GOOGLE-AUTH] Error: {e}")
        return None

async def main():
    req = urllib.request.Request(f"{CDP_BASE}/json/list")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
        
    google_tabs = [t for t in tabs if "accounts.google.com/v3/signin/accountchooser" in t.get("url", "")]
    print(f"Found {len(google_tabs)} Google Account Chooser tabs!")
    
    for t in google_tabs:
        await click_google_tab(t)
        await asyncio.sleep(2)

if __name__ == "__main__":
    asyncio.run(main())
