import asyncio
import json
import websockets
import re

async def main():
    github_tab = "C8AC94E331D5E7707203F724DC068AD7"
    gmail_tab = "846D30CA5670110BE1B220763CEEA59A"
    
    # 1. Click "Verify via email" in GitHub tab
    print("Clicking 'Verify via email' in GitHub tab...")
    ws_github_url = f"ws://127.0.0.1:9223/devtools/page/{github_tab}"
    async with websockets.connect(ws_github_url, max_size=25*1024*1024) as ws_gh:
        click_expr = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const verifyBtn = btns.find(b => b.innerText.includes('Verify via email'));
            if (verifyBtn) {
                verifyBtn.click();
                return 'Clicked Verify via email';
            }
            return 'Button not found';
        })()
        """
        await ws_gh.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': click_expr, 'returnByValue': True}}))
        res = json.loads(await ws_gh.recv())
        print("GitHub Click:", res.get('result', {}).get('result', {}).get('value'))
        
    print("Waiting 5 seconds for email to arrive...")
    await asyncio.sleep(5)
    
    # 2. Check Gmail tab
    print("Checking Gmail for GitHub code...")
    ws_gmail_url = f"ws://127.0.0.1:9223/devtools/page/{gmail_tab}"
    code = None
    async with websockets.connect(ws_gmail_url, max_size=25*1024*1024) as ws_gm:
        # Navigate to inbox or search for github
        search_expr = """
        (() => {
            window.location.href = 'https://mail.google.com/mail/u/0/#search/from%3Agithub+subject%3Averification';
            return 'Searching Gmail';
        })()
        """
        await ws_gm.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': search_expr, 'returnByValue': True}}))
        await ws_gm.recv()
        await asyncio.sleep(4)
        
        # Read text of search results
        for attempt in range(5):
            read_expr = "document.body.innerText"
            await ws_gm.send(json.dumps({'id': 2 + attempt, 'method': 'Runtime.evaluate', 'params': {'expression': read_expr, 'returnByValue': True}}))
            res = json.loads(await ws_gm.recv())
            text = res.get('result', {}).get('result', {}).get('value', '')
            
            # Find 6-digit or 8-digit verification code
            matches = re.findall(r'\b\d{6,8}\b', text)
            print(f"Attempt {attempt+1}: found possible codes: {matches[:5]}")
            if matches:
                code = matches[0]
                break
            await asyncio.sleep(3)
            
    print(f"Detected GitHub Code: {code}")
    
    if code:
        # 3. Enter code into GitHub
        async with websockets.connect(ws_github_url, max_size=25*1024*1024) as ws_gh:
            enter_code_expr = f"""
            (() => {{
                const input = document.querySelector('input[type="text"]') || document.querySelector('input[name="otp"]');
                if (input) {{
                    input.value = '{code}';
                    input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    input.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    const submitBtn = document.querySelector('button[type="submit"]');
                    if (submitBtn) {{
                        submitBtn.click();
                        return 'Submitted code ' + '{code}';
                    }}
                    return 'Input filled, no submit btn';
                }}
                return 'No input found';
            }})()
            """
            await ws_gh.send(json.dumps({'id': 10, 'method': 'Runtime.evaluate', 'params': {'expression': enter_code_expr, 'returnByValue': True}}))
            res = json.loads(await ws_gh.recv())
            print("Submit result:", res.get('result', {}).get('result', {}).get('value'))
            await asyncio.sleep(3)
            
            await ws_gh.send(json.dumps({'id': 11, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.location.href', 'returnByValue': True}}))
            res_url = json.loads(await ws_gh.recv())
            print("Current GitHub URL:", res_url.get('result', {}).get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(main())
