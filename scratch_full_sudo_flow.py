import asyncio
import json
import websockets
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def full_flow():
    gh_tab = "C8AC94E331D5E7707203F724DC068AD7"
    gm_tab = "846D30CA5670110BE1B220763CEEA59A"
    
    # 1. Click 'Verify via email' in GitHub
    print("Step 1: Clicking 'Verify via email' in GitHub...")
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{gh_tab}", max_size=25*1024*1024) as ws_gh:
        click_expr = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const b = btns.find(el => el.innerText.includes('Verify via email'));
            if (b) {
                b.click();
                return 'Clicked button: ' + b.innerText;
            }
            return 'Button not found';
        })()
        """
        await ws_gh.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': click_expr, 'returnByValue': True}}))
        res = json.loads(await ws_gh.recv())
        print("Click result:", res.get('result', {}).get('result', {}).get('value'))
        
    print("Step 2: Waiting 8 seconds for new email to arrive in Gmail...")
    await asyncio.sleep(8)
    
    # 2. Get code from Gmail
    new_code = None
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{gm_tab}", max_size=25*1024*1024) as ws_gm:
        for attempt in range(6):
            print(f"Checking Gmail attempt {attempt+1}...")
            # Reload search
            await ws_gm.send(json.dumps({'id': 10 + attempt*3, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.location.hash = "#search/from%3Agithub+sudo";', 'returnByValue': True}}))
            await ws_gm.recv()
            await asyncio.sleep(3)
            
            # Click first row
            await ws_gm.send(json.dumps({'id': 11 + attempt*3, 'method': 'Runtime.evaluate', 'params': {'expression': 'document.querySelectorAll("tr[role=\\"row\\"]")[0]?.click()', 'returnByValue': True}}))
            await ws_gm.recv()
            await asyncio.sleep(2)
            
            # Read text
            await ws_gm.send(json.dumps({'id': 12 + attempt*3, 'method': 'Runtime.evaluate', 'params': {'expression': 'document.body.innerText', 'returnByValue': True}}))
            res_body = json.loads(await ws_gm.recv())
            body = res_body.get('result', {}).get('result', {}).get('value', '')
            
            m = re.findall(r'sudo authentication code:\s*(\d{6,8})', body)
            if m:
                # Get the first match
                candidate = m[0]
                if candidate != '06861167':
                    new_code = candidate
                    print(f"FOUND NEW CODE: {new_code}")
                    break
                else:
                    print(f"Only saw old code {candidate}, waiting...")
            await asyncio.sleep(3)
            
    if not new_code:
        print("Could not obtain new code. Aborting.")
        return
        
    # 3. Enter new code into GitHub
    print(f"Step 3: Entering new code {new_code} into GitHub...")
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{gh_tab}", max_size=25*1024*1024) as ws_gh:
        submit_expr = f"""
        (() => {{
            const input = document.getElementById('sudo_email_otp') || document.querySelector('input[name="sudo_email_otp"]');
            if (!input) return 'Input not found';
            input.focus();
            input.value = '{new_code}';
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            
            const form = input.closest('form');
            const submitBtn = form ? form.querySelector('button[type="submit"]') : document.querySelector('button[type="submit"]');
            if (submitBtn) {{
                submitBtn.click();
                return 'Submitted OTP ' + '{new_code}';
            }}
            return 'Submit button not found';
        }})()
        """
        await ws_gh.send(json.dumps({'id': 100, 'method': 'Runtime.evaluate', 'params': {'expression': submit_expr, 'returnByValue': True}}))
        res_sub = json.loads(await ws_gh.recv())
        print("Submission result:", res_sub.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(5)
        
        await ws_gh.send(json.dumps({'id': 101, 'method': 'Runtime.evaluate', 'params': {'expression': '({url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 300)})', 'returnByValue': True}}))
        res_after = json.loads(await ws_gh.recv())
        print("GitHub page after submission:", json.dumps(res_after.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(full_flow())
