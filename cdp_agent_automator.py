import asyncio
import json
import urllib.request
import urllib.parse
import websockets
import time

CDP_BASE = "http://127.0.0.1:9223"

async def send_cdp_command(ws, method, params=None, msg_id=1):
    msg = {"id": msg_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(msg))
    while True:
        resp = await ws.recv()
        data = json.loads(resp)
        if data.get("id") == msg_id:
            return data.get("result", {})

async def open_tab(url):
    quoted_url = urllib.parse.quote(url, safe="")
    endpoint = f"{CDP_BASE}/json/new?{quoted_url}"
    req = urllib.request.Request(endpoint, method="PUT")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        return data.get("id"), data.get("webSocketDebuggerUrl")

async def close_tab(tab_id):
    endpoint = f"{CDP_BASE}/json/close/{tab_id}"
    try:
        req = urllib.request.Request(endpoint)
        with urllib.request.urlopen(req) as resp:
            pass
    except Exception:
        pass

async def eval_js(ws, expr):
    res = await send_cdp_command(ws, "Runtime.evaluate", {
        "expression": expr,
        "returnByValue": True,
        "awaitPromise": True
    })
    return res.get("result", {}).get("value")

async def automate_signup(name, signup_url):
    print(f"\n==========================================")
    print(f"[CDP-AGENT] Starting onboarding for: {name}")
    print(f"[CDP-AGENT] Opening URL: {signup_url}")
    
    tab_id, ws_url = await open_tab(signup_url)
    if not ws_url:
        print(f"[{name}] Failed to get WebSocket debugger URL")
        return False, "Failed to open tab"
        
    try:
        async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
            # Enable Page and Runtime
            await send_cdp_command(ws, "Page.enable")
            await send_cdp_command(ws, "Runtime.enable")
            
            # Wait for network idle / initial render
            await asyncio.sleep(4)
            
            # Check current URL and title
            state = await eval_js(ws, "({ url: window.location.href, title: document.title })")
            print(f"[{name}] Landed on: {state.get('url')} | Title: {state.get('title')}")
            
            # Look for GitHub button and click it
            click_script = '''
            (() => {
                const candidates = Array.from(document.querySelectorAll('button, a, input[type=submit], div[role=button]'));
                const btn = candidates.find(el => {
                    const txt = (el.innerText || el.textContent || el.value || '').toLowerCase();
                    return txt.includes('github') || txt.includes('git hub') || el.getAttribute('aria-label')?.toLowerCase().includes('github');
                });
                if (btn) {
                    btn.click();
                    return { clicked: true, text: btn.innerText || btn.textContent };
                }
                return { clicked: false };
            })()
            '''
            click_res = await eval_js(ws, click_script)
            if click_res and click_res.get("clicked"):
                print(f"[{name}] Successfully clicked GitHub button: '{click_res.get('text').strip()}'")
                await asyncio.sleep(5)
            else:
                print(f"[{name}] No direct GitHub button found on initial landing page")
                
            # Check if we landed on GitHub OAuth authorization screen
            auth_script = '''
            (() => {
                const url = window.location.href;
                const isGithubAuth = url.includes('github.com/login/oauth/authorize') || url.includes('github.com/login?return_to');
                const authBtn = document.querySelector('button[name=authorize], input[value*="Authorize"], button:not([disabled])');
                const btnText = authBtn ? (authBtn.innerText || authBtn.value || '') : '';
                if (btnText.toLowerCase().includes('authorize')) {
                    authBtn.click();
                    return { authorized: true, url: url };
                }
                return { isGithubAuth: isGithubAuth, authorized: false, url: url };
            })()
            '''
            auth_res = await eval_js(ws, auth_script)
            if auth_res:
                if auth_res.get("authorized"):
                    print(f"[{name}] Found and clicked GitHub 'Authorize' button!")
                    await asyncio.sleep(6)
                elif auth_res.get("isGithubAuth"):
                    print(f"[{name}] Landed on GitHub OAuth page: {auth_res.get('url')}")
                    
            # Check final URL and title
            final_state = await eval_js(ws, "({ url: window.location.href, title: document.title })")
            print(f"[{name}] Final State: URL={final_state.get('url')} | Title={final_state.get('title')}")
            
            return True, final_state.get("url")
            
    except Exception as e:
        print(f"[{name}] Error during automation: {e}")
        return False, str(e)

async def main():
    test_targets = [
        ("Deno Deploy", "https://dash.deno.com/signin"),
        ("Supabase", "https://supabase.com/dashboard/sign-in"),
        ("Render", "https://dashboard.render.com/register"),
        ("Koyeb", "https://app.koyeb.com/auth/signup"),
        ("Zeabur", "https://zeabur.com/login"),
        ("Convex", "https://dashboard.convex.dev/login")
    ]
    
    results = {}
    for name, url in test_targets:
        ok, res_url = await automate_signup(name, url)
        results[name] = {"ok": ok, "final_url": res_url}
        await asyncio.sleep(2)
        
    print("\n\n==========================================")
    print("CDP ONBOARDING RUN COMPLETE. SUMMARY:")
    for k, v in results.items():
        print(f"- {k}: {'SUCCESS' if v['ok'] else 'FAILED'} -> {v['final_url']}")

if __name__ == "__main__":
    asyncio.run(main())
