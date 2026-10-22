import asyncio
import json
import urllib.request
import websockets
import time

CDP_BASE = "http://127.0.0.1:9223"

async def send_cmd(ws, method, params=None, msg_id=1):
    msg = {"id": msg_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(msg))
    while True:
        resp = await ws.recv()
        data = json.loads(resp)
        if data.get("id") == msg_id:
            return data.get("result", {})

async def process_oauth_tab(tab):
    title = tab.get("title", "")
    url = tab.get("url", "")
    ws_url = tab.get("webSocketDebuggerUrl")
    
    print(f"\n[AUTH-CLICKER] Processing tab: '{title}'")
    print(f"[AUTH-CLICKER] URL: {url[:100]}...")
    
    try:
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            # Check form and authorize button
            js_script = '''
            (() => {
                const btn = document.querySelector('.js-oauth-authorize-btn, button[name=authorize], input[value*="Authorize"]');
                const form = document.querySelector('form.js-oauth-application-form, form[action*="/authorize"]');
                if (btn) {
                    btn.disabled = false;
                    btn.click();
                    return { found: true, method: 'click', text: btn.innerText || btn.value };
                }
                if (form) {
                    form.submit();
                    return { found: true, method: 'submit' };
                }
                return { found: false };
            })()
            '''
            res = await send_cmd(ws, "Runtime.evaluate", {
                "expression": js_script,
                "returnByValue": True
            }, msg_id=1)
            val = res.get("result", {}).get("value", {})
            print(f"[AUTH-CLICKER] Action result: {val}")
            
            # Wait for redirect
            await asyncio.sleep(6)
            
            # Check final URL and title
            state_res = await send_cmd(ws, "Runtime.evaluate", {
                "expression": "({ url: window.location.href, title: document.title })",
                "returnByValue": True
            }, msg_id=2)
            final_state = state_res.get("result", {}).get("value", {})
            print(f"[AUTH-CLICKER] Post-action URL: {final_state.get('url')}")
            print(f"[AUTH-CLICKER] Post-action Title: {final_state.get('title')}")
            return final_state
    except Exception as e:
        print(f"[AUTH-CLICKER] Error: {e}")
        return None

async def main():
    # 1. Fetch all tabs
    req = urllib.request.Request(f"{CDP_BASE}/json/list")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
        
    oauth_tabs = [t for t in tabs if "github.com/login/oauth/authorize" in t.get("url", "") or "Authorize" in t.get("title", "")]
    print(f"Found {len(oauth_tabs)} OAuth authorization tabs waiting in browser!")
    
    results = []
    for t in oauth_tabs:
        res = await process_oauth_tab(t)
        results.append((t.get("title"), res))
        await asyncio.sleep(2)
        
    print("\n\n==========================================")
    print("ALL WAITING OAUTH TABS PROCESSED!")
    for title, r in results:
        url = r.get("url") if r else "N/A"
        t = r.get("title") if r else "N/A"
        print(f"- {title} -> {t} ({url[:80]}...)")

if __name__ == "__main__":
    asyncio.run(main())
