import asyncio
import json
import urllib.request
import websockets
import sys
sys.stdout.reconfigure(encoding='utf-8')

CDP_BASE = "http://127.0.0.1:9223"
EMAIL = "admin@adicommunications.co.uk"
PASSWORD = "Joshuajack7787!!"
CODE = "C7ZV19FFTDXMXG1JSMVRG3C2"

async def do_auth():
    req = urllib.request.Request(f"{CDP_BASE}/json/list")
    with urllib.request.urlopen(req) as resp:
        tabs = json.loads(resp.read().decode())
    target = next((t for t in tabs if "auth.circleci.com" in t.get("url", "") or "app.circleci.com" in t.get("url", "")), None)
    if not target:
        print("CircleCI auth tab not found")
        return
        
    ws_url = target.get("webSocketDebuggerUrl")
    print("Connected to CircleCI tab:", target.get("url")[:80])
    
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        # Step 1: Fill email
        fill_email_js = f'''
        (() => {{
            const inp = document.querySelector('#username, input[name=username], input[type=email]');
            if (inp) {{
                inp.value = "{EMAIL}";
                inp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                inp.dispatchEvent(new Event('change', {{ bubbles: true }}));
                return {{ filled: true, val: inp.value }};
            }}
            return {{ filled: false }};
        }})()
        '''
        msg = {"id": 1, "method": "Runtime.evaluate", "params": {"expression": fill_email_js, "returnByValue": True}}
        await ws.send(json.dumps(msg))
        r1 = await ws.recv()
        print("Email fill result:", json.loads(r1).get("result", {}).get("result", {}).get("value"))
        
        # Click Continue
        click_cont_js = '''
        (() => {
            const btn = document.querySelector('button[type=submit], button[name=action]');
            if (btn) { btn.click(); return { clicked: true, text: btn.innerText }; }
            return { clicked: false };
        })()
        '''
        msg["id"] = 2
        msg["params"]["expression"] = click_cont_js
        await ws.send(json.dumps(msg))
        r2 = await ws.recv()
        print("Continue click:", json.loads(r2).get("result", {}).get("result", {}).get("value"))
        
        # Wait 4s for password / code step
        await asyncio.sleep(5)
        
        # Step 2: Check current URL & inputs
        inspect_js = '''
        (() => {
            return {
                url: window.location.href,
                title: document.title,
                inputs: Array.from(document.querySelectorAll('input')).map(i => ({ type: i.type, name: i.name, id: i.id, placeholder: i.placeholder })),
                buttons: Array.from(document.querySelectorAll('button, input[type=submit]')).map(b => (b.innerText || b.value || '').trim())
            };
        })()
        '''
        msg["id"] = 3
        msg["params"]["expression"] = inspect_js
        await ws.send(json.dumps(msg))
        r3 = await ws.recv()
        state = json.loads(r3).get("result", {}).get("result", {}).get("value")
        print("Password/Code page state:", state)
        
        # Step 3: Fill password or recovery code
        fill_pass_js = f'''
        (() => {{
            const passInp = document.querySelector('input[type=password], #password, input[name=password]');
            if (passInp) {{
                passInp.value = "{PASSWORD}";
                passInp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                passInp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            const codeInp = document.querySelector('input[name*="code"], input[name*="otp"], #code, input[placeholder*="code"], input[autocomplete="one-time-code"]');
            if (codeInp) {{
                codeInp.value = "{CODE}";
                codeInp.dispatchEvent(new Event('input', {{ bubbles: true }}));
                codeInp.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            
            return {{ passFound: !!passInp, codeFound: !!codeInp }};
        }})()
        '''
        msg["id"] = 4
        msg["params"]["expression"] = fill_pass_js
        await ws.send(json.dumps(msg))
        r4 = await ws.recv()
        print("Credentials filled:", json.loads(r4).get("result", {}).get("result", {}).get("value"))
        
        # Click submit
        msg["id"] = 5
        msg["params"]["expression"] = click_cont_js
        await ws.send(json.dumps(msg))
        r5 = await ws.recv()
        print("Submit click:", json.loads(r5).get("result", {}).get("result", {}).get("value"))
        
        await asyncio.sleep(6)
        
        msg["id"] = 6
        msg["params"]["expression"] = "({ url: window.location.href, title: document.title, body: (document.body.innerText || '').slice(0, 500) })"
        await ws.send(json.dumps(msg))
        r6 = await ws.recv()
        final_info = json.loads(r6).get("result", {}).get("result", {}).get("value")
        print("Final State after submit:", final_info)

if __name__ == "__main__":
    asyncio.run(do_auth())
