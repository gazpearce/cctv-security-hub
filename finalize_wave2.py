import asyncio
import json
import urllib.request
import websockets

CDP_BASE = "http://127.0.0.1:9223"

async def finalize_tab(tab_url_match, click_selector_js, description):
    req = urllib.request.Request(f"{CDP_BASE}/json/list")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
        
    target_tab = next((t for t in tabs if tab_url_match.lower() in t.get("url", "").lower() or tab_url_match.lower() in t.get("title", "").lower()), None)
    if not target_tab:
        print(f"[{description}] Tab not found for match: {tab_url_match}")
        return False
        
    print(f"[{description}] Found tab: {target_tab.get('title')} ({target_tab.get('url')[:60]}...)")
    ws_url = target_tab.get("webSocketDebuggerUrl")
    
    try:
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": click_selector_js, "returnByValue": True}}
            await ws.send(json.dumps(msg))
            resp = await ws.recv()
            res = json.loads(resp).get("result", {}).get("result", {}).get("value")
            print(f"[{description}] Action result: {res}")
            await asyncio.sleep(6)
            
            # Check post-action URL
            msg["id"] = 2
            msg["params"]["expression"] = "window.location.href"
            await ws.send(json.dumps(msg))
            resp2 = await ws.recv()
            post_url = json.loads(resp2).get("result", {}).get("result", {}).get("value")
            print(f"[{description}] Post URL: {post_url}")
            return True
    except Exception as e:
        print(f"[{description}] Error: {e}")
        return False

async def main():
    # 1. Kaggle - Click Google account in account chooser
    kaggle_js = '''
    (() => {
        const acc = document.querySelector('div[data-identifier="aiagent1510@gmail.com"], li[data-authuser="0"], div[role="link"]');
        if (acc) { acc.click(); return { clicked: true, text: 'Clicked aiagent1510 account' }; }
        const anyAcc = document.querySelector('div[role="link"]');
        if (anyAcc) { anyAcc.click(); return { clicked: true, text: 'Clicked first account' }; }
        return { clicked: false };
    })()
    '''
    await finalize_tab("kaggle.com", kaggle_js, "Kaggle Google Auth")
    
    # 2. Deno Deploy - Click GitHub button on console.deno.com
    deno_js = '''
    (() => {
        const btn = Array.from(document.querySelectorAll('button, a')).find(el => (el.innerText||'').toLowerCase().includes('github'));
        if (btn) { btn.click(); return { clicked: true, text: btn.innerText }; }
        return { clicked: false };
    })()
    '''
    await finalize_tab("console.deno.com", deno_js, "Deno Console Signin")
    
    # 3. Turso - Click GitHub on app.turso.tech
    turso_js = '''
    (() => {
        const btn = Array.from(document.querySelectorAll('button, a')).find(el => (el.innerText||'').toLowerCase().includes('github'));
        if (btn) { btn.click(); return { clicked: true, text: btn.innerText }; }
        return { clicked: false };
    })()
    '''
    await finalize_tab("turso.tech", turso_js, "Turso App Signin")
    
    # 4. Upstash - Click GitHub on console.upstash.com
    upstash_js = '''
    (() => {
        const btn = Array.from(document.querySelectorAll('button, a')).find(el => (el.innerText||'').toLowerCase().includes('github'));
        if (btn) { btn.click(); return { clicked: true, text: btn.innerText }; }
        return { clicked: false };
    })()
    '''
    await finalize_tab("upstash.com", upstash_js, "Upstash Signin")

if __name__ == "__main__":
    asyncio.run(main())
