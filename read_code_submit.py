import asyncio
import websockets
import urllib.request
import json
import time
import re

async def read_and_submit():
    time.sleep(2)
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())
    gmail_tab = next(t for t in tabs if 'mail.google.com/mail/u/0/' in t.get('url', ''))
    gh_tab = next(t for t in tabs if 'Confirm access' in t.get('title', ''))
    
    code = None
    async with websockets.connect(gmail_tab['webSocketDebuggerUrl']) as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': 'document.body.innerText', 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        text = res['result']['result']['value']
        
        # Look for verification code pattern
        matches = re.findall(r'(\d{6})', text)
        print('All 6-digit numbers in email:', matches)
        # Search specifically for line containing code
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        for idx, line in enumerate(lines):
            if 'verification code' in line.lower() or 'temporary verification code' in line.lower():
                print(f"Context line: {line}")
                for next_l in lines[idx:idx+5]:
                    c_match = re.findall(r'\b\d{6}\b', next_l)
                    if c_match:
                        code = c_match[0]
                        print("Exact matched code:", code)
                        break
                if code:
                    break

    if not code and matches:
        code = matches[0]

    if code:
        print('SUBMITTING CODE TO GITHUB:', code)
        async with websockets.connect(gh_tab['webSocketDebuggerUrl']) as ws:
            expr = f"""(() => {{
                const input = document.querySelector('input[type=text], input[name*=otp], input[name*=code], input[id*=otp]');
                if (input) {{
                    input.value = '{code}';
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    const submitBtn = Array.from(document.querySelectorAll('button, input[type=submit]')).find(b => (b.innerText || b.value || '').toLowerCase().includes('verify'));
                    if (submitBtn) {{
                        submitBtn.click();
                        return 'Code entered and submit clicked';
                    }}
                    return 'Code entered, button not found';
                }}
                return 'Input not found';
            }})()"""
            await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
            res = json.loads(await ws.recv())
            print(res['result']['result']['value'])

if __name__ == '__main__':
    asyncio.run(read_and_submit())
