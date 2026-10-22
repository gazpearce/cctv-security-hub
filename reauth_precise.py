import asyncio
import json
import urllib.request
import urllib.parse
import websockets

CDP_BASE = "http://127.0.0.1:9223"

async def reauth(name, url):
    quoted = urllib.parse.quote(url, safe="")
    endpoint = f"{CDP_BASE}/json/new?{quoted}"
    req = urllib.request.Request(endpoint, method="PUT")
    with urllib.request.urlopen(req) as resp:
        t = json.loads(resp.read().decode())
    ws_url = t.get("webSocketDebuggerUrl")
    print(f"\n[{name}] Opened tab: {t.get('id')}")
    
    try:
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            await asyncio.sleep(4)
            # Click github button if on login page
            click_js = '''
            (() => {
                const btn = Array.from(document.querySelectorAll('button, a')).find(el => (el.innerText||'').toLowerCase().includes('github'));
                if (btn) { btn.click(); return true; }
                return false;
            })()
            '''
            msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": click_js, "returnByValue": True}}
            await ws.send(json.dumps(msg))
            await ws.recv()
            await asyncio.sleep(5)
            
            # Click EXACT authorize button (value=1)
            auth_js = '''
            (() => {
                const btn = document.querySelector('button[name=authorize][value="1"], input[name=authorize][value="1"], .js-oauth-authorize-btn');
                if (btn) {
                    btn.disabled = false;
                    btn.click();
                    return { clicked: true, text: btn.innerText || btn.value };
                }
                return { clicked: false };
            })()
            '''
            msg["id"] = 2
            msg["params"]["expression"] = auth_js
            await ws.send(json.dumps(msg))
            resp2 = await ws.recv()
            val = json.loads(resp2).get("result", {}).get("result", {}).get("value")
            print(f"[{name}] Authorize click: {val}")
            await asyncio.sleep(6)
            
            msg["id"] = 3
            msg["params"]["expression"] = "window.location.href"
            await ws.send(json.dumps(msg))
            resp3 = await ws.recv()
            final_url = json.loads(resp3).get("result", {}).get("result", {}).get("value")
            print(f"[{name}] Final URL: {final_url}")
            return final_url
    except Exception as e:
        print(f"[{name}] Error: {e}")
        return None

async def main():
    await reauth("Convex", "https://dashboard.convex.dev/login")
    await reauth("Supabase", "https://supabase.com/dashboard/sign-in")

if __name__ == "__main__":
    asyncio.run(main())
