import asyncio
import websockets
import urllib.request
import json
import time
import re

async def github_sudo_flow():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())
    gh_tab = next(t for t in tabs if 'github.com/login/oauth/authorize' in t.get('url', ''))
    gmail_tab = next(t for t in tabs if 'mail.google.com' in t.get('url', ''))
    
    print("Found GitHub tab:", gh_tab['url'])
    print("Found Gmail tab:", gmail_tab['url'])
    
    # 1. Click "Verify via email" on GitHub
    async with websockets.connect(gh_tab['webSocketDebuggerUrl']) as ws:
        msg_id = 1
        async def call(method, params=None):
            nonlocal msg_id
            msg_id += 1
            await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get('id') == msg_id:
                    return resp.get('result', {})

        expr = """(() => {
            const btn = Array.from(document.querySelectorAll('button, input[type=submit]')).find(b => (b.innerText || b.value || '').toLowerCase().includes('verify via email'));
            if (btn) {
                btn.click();
                return 'Clicked ' + (btn.innerText || btn.value);
            }
            return 'Button not found';
        })()"""
        res = await call('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        print("Click result:", res.get('result', {}).get('value'))

    print("Waiting 5 seconds for GitHub email to arrive...")
    await asyncio.sleep(5)
    
    # 2. Check Gmail for GitHub verification code
    code = None
    for attempt in range(6):
        print(f"Checking Gmail (attempt {attempt+1}/6)...")
        async with websockets.connect(gmail_tab['webSocketDebuggerUrl']) as ws:
            msg_id = 100
            async def call_m(method, params=None):
                nonlocal msg_id
                msg_id += 1
                await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get('id') == msg_id:
                        return resp.get('result', {})

            # Refresh / click inbox or get innerText
            res = await call_m('Runtime.evaluate', {'expression': 'document.body.innerText', 'returnByValue': True})
            text = res.get('result', {}).get('value', '')
            
            # Look for github verification code pattern (usually 6 digits, e.g. [GitHub] Please verify your device or code)
            m = re.findall(r'\b\d{6}\b', text)
            print("Found 6-digit candidates in Gmail text:", m[:5])
            
            # Check for GitHub subject in recent rows
            rows_expr = """(() => {
                const rows = Array.from(document.querySelectorAll('tr'));
                return rows.slice(0, 10).map(r => r.innerText);
            })()"""
            rows = await call_m('Runtime.evaluate', {'expression': rows_expr, 'returnByValue': True})
            for r in rows.get('result', {}).get('value', []):
                if 'github' in r.lower():
                    print("Recent GitHub email row:", r[:120])
                    digits = re.findall(r'\b\d{6}\b', r)
                    if digits:
                        code = digits[0]
                        break
            if code:
                break
        await asyncio.sleep(4)

    if not code and m:
        # Fallback to most recent candidate
        code = m[0]
        
    print("Detected Code:", code)
    
    # 3. Enter code on GitHub tab if found
    if code:
        async with websockets.connect(gh_tab['webSocketDebuggerUrl']) as ws:
            msg_id = 200
            async def call_g(method, params=None):
                nonlocal msg_id
                msg_id += 1
                await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
                while True:
                    resp = json.loads(await ws.recv())
                    if resp.get('id') == msg_id:
                        return resp.get('result', {})

            enter_code_expr = f"""(() => {{
                const input = document.querySelector('input[type=text], input[name*=otp], input[name*=code], input[id*=otp]');
                if (input) {{
                    input.value = '{code}';
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    const submitBtn = document.querySelector('button[type=submit], input[type=submit]');
                    if (submitBtn) submitBtn.click();
                    return 'Entered code and clicked submit';
                }}
                return 'Input not found';
            }})()"""
            res = await call_g('Runtime.evaluate', {'expression': enter_code_expr, 'returnByValue': True})
            print("Code submit result:", res.get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(github_sudo_flow())
