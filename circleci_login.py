import asyncio
import json
import urllib.request
import urllib.parse
import websockets
import time

CDP_BASE = "http://127.0.0.1:9223"
TARGET_URL = "https://app.circleci.com/organization/circleci/AhN4FFZ8QAdsUijAEmhUvc"
LOGIN_CODE = "C7ZV19FFTDXMXG1JSMVRG3C2"
PASSWORD = "Joshuajack7787!!"
EMAILS = ["admin@adicommunications.co.uk", "aiagent1510@gmail.com"]

async def send_cmd(ws, method, params=None, msg_id=1):
    msg = {"id": msg_id, "method": method, "params": params or {}}
    await ws.send(json.dumps(msg))
    while True:
        resp = await ws.recv()
        data = json.loads(resp)
        if data.get("id") == msg_id:
            return data.get("result", {})

async def eval_js(ws, expr, msg_id=1):
    res = await send_cmd(ws, "Runtime.evaluate", {
        "expression": expr,
        "returnByValue": True,
        "awaitPromise": True
    }, msg_id=msg_id)
    return res.get("result", {}).get("value")

async def login_circleci():
    print(f"[CIRCLECI] Opening target URL: {TARGET_URL}")
    quoted = urllib.parse.quote(TARGET_URL, safe="")
    endpoint = f"{CDP_BASE}/json/new?{quoted}"
    req = urllib.request.Request(endpoint, method="PUT")
    with urllib.request.urlopen(req) as resp:
        tab = json.loads(resp.read().decode())
        
    tab_id = tab.get("id")
    ws_url = tab.get("webSocketDebuggerUrl")
    print(f"[CIRCLECI] Opened tab {tab_id}, connecting to debugger...")
    
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        await send_cmd(ws, "Page.enable", msg_id=1)
        await send_cmd(ws, "Runtime.enable", msg_id=2)
        
        # Wait for page to load
        await asyncio.sleep(6)
        
        state = await eval_js(ws, "({ url: window.location.href, title: document.title })", msg_id=3)
        print(f"[CIRCLECI] Current URL: {state.get('url')}")
        print(f"[CIRCLECI] Current Title: {state.get('title')}")
        
        # Inspect form fields and buttons on page
        inspect_script = '''
        (() => {
            return {
                inputs: Array.from(document.querySelectorAll('input')).map(i => ({
                    type: i.type,
                    name: i.name,
                    id: i.id,
                    placeholder: i.placeholder,
                    value: i.value
                })),
                buttons: Array.from(document.querySelectorAll('button, a, input[type=submit]')).map(b => ({
                    text: (b.innerText || b.value || '').trim(),
                    type: b.type
                }))
            };
        })()
        '''
        dom_info = await eval_js(ws, inspect_script, msg_id=4)
        print(f"[CIRCLECI] Page Inputs: {dom_info.get('inputs')}")
        print(f"[CIRCLECI] Page Buttons: {dom_info.get('buttons')[:10]}")
        
        # Check if already logged in or needs login
        curr_url = state.get("url", "")
        if "circleci.com/organization" in curr_url and "login" not in curr_url:
            print("[CIRCLECI] Already logged in to organization dashboard!")
            return True, curr_url
            
        # If GitHub SSO is available, try GitHub first
        click_gh = '''
        (() => {
            const btn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText||'').toLowerCase().includes('github'));
            if (btn) { btn.click(); return { clicked: true, text: btn.innerText }; }
            return { clicked: false };
        })()
        '''
        gh_res = await eval_js(ws, click_gh, msg_id=5)
        if gh_res and gh_res.get("clicked"):
            print(f"[CIRCLECI] Clicked GitHub SSO button: {gh_res.get('text')}")
            await asyncio.sleep(6)
            
            # Check if GitHub Authorize appeared
            auth_script = '''
            (() => {
                const btn = document.querySelector('button[name=authorize][value="1"], input[name=authorize][value="1"], .js-oauth-authorize-btn');
                if (btn) { btn.disabled = false; btn.click(); return { authorized: true }; }
                return { authorized: false };
            })()
            '''
            auth_res = await eval_js(ws, auth_script, msg_id=6)
            if auth_res and auth_res.get("authorized"):
                print("[CIRCLECI] Clicked GitHub Authorize for CircleCI!")
                await asyncio.sleep(6)
                
        # Check if password / 2FA / code input exists
        fill_code_script = f'''
        (() => {{
            const code = "{LOGIN_CODE}";
            const pass = "{PASSWORD}";
            const email = "{EMAILS[0]}";
            
            const emailInp = document.querySelector('input[type=email], input[name=email], input[autocomplete=username]');
            if (emailInp) {{
                emailInp.value = email;
                emailInp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                emailInp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            const passInp = document.querySelector('input[type=password], input[name=password]');
            if (passInp) {{
                passInp.value = pass;
                passInp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                passInp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            const codeInp = document.querySelector('input[name*="code"], input[placeholder*="code"], input[autocomplete="one-time-code"], input[name*="otp"], input[type=tel]');
            if (codeInp) {{
                codeInp.value = code;
                codeInp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                codeInp.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return {{ filledCode: true }};
            }}
            return {{ filledCode: false, emailFilled: !!emailInp, passFilled: !!passInp }};
        }})()
        '''
        fill_res = await eval_js(ws, fill_code_script, msg_id=7)
        print(f"[CIRCLECI] Fill form result: {fill_res}")
        
        # Submit if form button available
        submit_script = '''
        (() => {
            const btn = Array.from(document.querySelectorAll('button, input[type=submit]')).find(b => {
                const t = (b.innerText || b.value || '').toLowerCase();
                return t.includes('sign in') || t.includes('log in') || t.includes('continue') || t.includes('verify') || t.includes('submit');
            });
            if (btn) { btn.click(); return { clicked: true, text: btn.innerText || btn.value }; }
            return { clicked: false };
        })()
        '''
        sub_res = await eval_js(ws, submit_script, msg_id=8)
        print(f"[CIRCLECI] Submit click result: {sub_res}")
        
        await asyncio.sleep(6)
        final_state = await eval_js(ws, "({ url: window.location.href, title: document.title })", msg_id=9)
        print(f"[CIRCLECI] Final URL: {final_state.get('url')}")
        print(f"[CIRCLECI] Final Title: {final_state.get('title')}")
        return True, final_state.get("url")

if __name__ == "__main__":
    asyncio.run(login_circleci())
