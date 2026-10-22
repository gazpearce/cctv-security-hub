import asyncio
import json
import urllib.request
import urllib.parse
import websockets
import time

CDP_BASE = "http://127.0.0.1:9223"

WAVE3_TARGETS = [
    ("Netlify", "https://app.netlify.com/start", "github"),
    ("Glitch", "https://glitch.com/signin", "github"),
    ("Replit", "https://replit.com/login", "github"),
    ("CodeSandbox", "https://codesandbox.io/signin", "github"),
    ("StackBlitz", "https://stackblitz.com/", "github"),
    ("Fleek IPFS", "https://app.fleek.xyz/", "github"),
    ("Postman Cloud", "https://identity.getpostman.com/signup", "google"),
    ("Sentry.io", "https://sentry.io/signup/", "github"),
    ("Sevalla", "https://my.sevalla.com/login", "github"),
    ("Bitbucket", "https://bitbucket.org/account/signin/", "google")
]

async def send_cmd(ws, method, params=None, msg_id=1):
    msg = {"id": msg_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(msg))
    while True:
        resp = await ws.recv()
        data = json.loads(resp)
        if data.get("id") == msg_id:
            return data.get("result", {})

async def open_tab(url):
    quoted = urllib.parse.quote(url, safe="")
    endpoint = f"{CDP_BASE}/json/new?{quoted}"
    req = urllib.request.Request(endpoint, method="PUT")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        return data.get("id"), data.get("webSocketDebuggerUrl")

async def eval_js(ws, expr):
    res = await send_cmd(ws, "Runtime.evaluate", {
        "expression": expr,
        "returnByValue": True,
        "awaitPromise": True
    })
    return res.get("result", {}).get("value")

async def process_target(name, signup_url, provider):
    print(f"\n==========================================")
    print(f"[WAVE-3] Onboarding: {name} (Provider: {provider})")
    print(f"[WAVE-3] URL: {signup_url}")
    
    tab_id, ws_url = await open_tab(signup_url)
    if not ws_url:
        return False, "Failed to open tab"
        
    try:
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            await send_cmd(ws, "Page.enable")
            await send_cmd(ws, "Runtime.enable")
            await asyncio.sleep(5)
            
            # Click provider button
            click_script = f'''
            (() => {{
                const target = "{provider}".toLowerCase();
                const candidates = Array.from(document.querySelectorAll('button, a, input[type=submit], div[role=button], span'));
                const btn = candidates.find(el => {{
                    const txt = (el.innerText || el.textContent || el.value || '').toLowerCase();
                    return txt.includes(target) || el.getAttribute('aria-label')?.toLowerCase().includes(target);
                }});
                if (btn) {{
                    const clickable = btn.closest('button, a, div[role=button]') || btn;
                    clickable.click();
                    return {{ clicked: true, text: clickable.innerText || clickable.textContent }};
                }}
                return {{ clicked: false }};
            }})()
            '''
            click_res = await eval_js(ws, click_script)
            if click_res and click_res.get("clicked"):
                print(f"[{name}] Clicked {provider.upper()} button: '{click_res.get('text').strip()[:40]}'")
                await asyncio.sleep(6)

            # Handle GitHub Authorize screen if arrived
            auth_script = '''
            (() => {
                const btn = document.querySelector('button[name=authorize][value="1"], input[name=authorize][value="1"], .js-oauth-authorize-btn');
                if (btn) {
                    btn.disabled = false;
                    btn.click();
                    return { authorized: true, text: btn.innerText || btn.value };
                }
                return { authorized: false };
            })()
            '''
            auth_res = await eval_js(ws, auth_script)
            if auth_res and auth_res.get("authorized"):
                print(f"[{name}] Found and clicked GitHub Authorize button: '{auth_res.get('text')}'")
                await asyncio.sleep(6)

            final_state = await eval_js(ws, "({ url: window.location.href, title: document.title })")
            final_url = final_state.get("url", "")
            final_title = final_state.get("title", "")
            print(f"[{name}] Final State: URL={final_url} | Title={final_title}")
            return True, final_url
    except Exception as e:
        print(f"[{name}] Error: {e}")
        return False, str(e)

async def main():
    results = {}
    for name, url, provider in WAVE3_TARGETS:
        ok, res_url = await process_target(name, url, provider)
        results[name] = {"ok": ok, "url": res_url}
        await asyncio.sleep(2)
        
    print("\n\n==========================================")
    print("WAVE 3 ONBOARDING SWEEP COMPLETE. SUMMARY:")
    for k, v in results.items():
        print(f"- {k}: {'ACCESSED' if v['ok'] else 'FAILED'} -> {v['url']}")

if __name__ == "__main__":
    asyncio.run(main())
