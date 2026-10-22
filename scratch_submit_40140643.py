import asyncio
import json
import websockets

async def submit_exact_otp():
    gh_tab = "C8AC94E331D5E7707203F724DC068AD7"
    code = "40140643"
    print(f"Submitting {code} to GitHub...")
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{gh_tab}", max_size=25*1024*1024) as ws:
        expr = f"""
        (() => {{
            const input = document.getElementById('sudo_email_otp') || document.querySelector('input[name="sudo_email_otp"]');
            if (!input) return 'Input not found';
            input.focus();
            input.value = '{code}';
            input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            input.dispatchEvent(new Event('change', {{ bubbles: true }}));
            
            const form = input.closest('form');
            const submitBtn = form ? form.querySelector('button[type="submit"]') : document.querySelector('button[type="submit"]');
            if (submitBtn) {{
                submitBtn.click();
                return 'Submitted OTP ' + '{code}';
            }}
            return 'Submit button not found';
        }})()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        print("Submit result:", res.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(4)
        
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': '({url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 300)})', 'returnByValue': True}}))
        res2 = json.loads(await ws.recv())
        print("Resulting page:", json.dumps(res2.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(submit_exact_otp())
