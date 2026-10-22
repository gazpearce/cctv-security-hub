import asyncio
import json
import websockets

async def submit_exact_otp():
    ws_url = "ws://127.0.0.1:9223/devtools/page/C8AC94E331D5E7707203F724DC068AD7"
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        expr = """
        (() => {
            const input = document.getElementById('sudo_email_otp') || document.querySelector('input[name="sudo_email_otp"]');
            if (!input) return 'sudo_email_otp input not found';
            
            input.focus();
            input.value = '06861167';
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            
            const form = input.closest('form');
            if (form) {
                const btn = form.querySelector('button[type="submit"]');
                if (btn) {
                    btn.click();
                    return 'Clicked submit button in form with OTP 06861167';
                }
                form.submit();
                return 'Submitted form directly';
            }
            return 'Form not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        print("Submit result:", res.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(5)
        
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': '({url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 400)})', 'returnByValue': True}}))
        res2 = json.loads(await ws.recv())
        print("After OTP result:", json.dumps(res2.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(submit_exact_otp())
