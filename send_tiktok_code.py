import json
import asyncio
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

TAB_ID = "76CC99643C9BDB39C51016640626E071"
PHONE_NUMBER = "7830638337"

async def send_code():
    url = f"ws://127.0.0.1:9223/devtools/page/{TAB_ID}"
    async with websockets.connect(url, max_size=20*1024*1024) as ws:
        # Step 1: Navigate to phone login (code mode)
        print("Navigating to https://www.tiktok.com/login/phone-or-email/phone ...")
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://www.tiktok.com/login/phone-or-email/phone'}}))
        await ws.recv()
        await asyncio.sleep(3.0)

        # Step 2: Ensure UK-44 is selected
        sel_uk_js = """
        (() => {
            const currentLabel = document.querySelector('.tiktok-1llsm0k-de495bb3--DivAreaLabelContainer') || document.querySelector('[role="button"][aria-label*="country code"]');
            if (currentLabel && currentLabel.innerText.includes('+44')) {
                return 'UK-44 already active';
            }
            if (currentLabel) {
                currentLabel.click();
            }
            const ukEl = document.getElementById('UK-44');
            if (ukEl) {
                ukEl.click();
                return 'Clicked UK-44';
            }
            return 'Opened country dropdown';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': sel_uk_js, 'returnByValue': True}}))
        res_uk = json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value')
        print(f"Country step 1: {res_uk}")
        await asyncio.sleep(1.0)

        # If dropdown was just opened, click UK-44
        if res_uk == 'Opened country dropdown':
            click_uk = """
            (() => {
                const ukEl = document.getElementById('UK-44');
                if (ukEl) {
                    ukEl.scrollIntoView({ block: 'center' });
                    ukEl.click();
                    return 'Clicked UK-44 in dropdown';
                }
                return 'UK-44 not found';
            })()
            """
            await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': click_uk, 'returnByValue': True}}))
            res_uk2 = json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value')
            print(f"Country step 2: {res_uk2}")
            await asyncio.sleep(1.0)

        # Step 3: Type phone number with CDP keystrokes/insertText
        print(f"Typing phone number: {PHONE_NUMBER}...")
        focus_phone_js = """
        (() => {
            const inp = document.querySelector('input[name="mobile"], input[placeholder*="Phone"]');
            if (inp) {
                inp.focus();
                inp.value = '';
                inp.dispatchEvent(new Event('input', { bubbles: true }));
                inp.dispatchEvent(new Event('change', { bubbles: true }));
                return true;
            }
            return false;
        })()
        """
        await ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': focus_phone_js, 'returnByValue': True}}))
        await ws.recv()
        await asyncio.sleep(0.3)

        for char in PHONE_NUMBER:
            await ws.send(json.dumps({'id': 5, 'method': 'Input.insertText', 'params': {'text': char}}))
            await ws.recv()
            await asyncio.sleep(0.05)

        await asyncio.sleep(1.0)

        # Step 4: Check "Send code" button status
        check_send_btn = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Send code') || b.innerText.includes('Resend'));
            return {
                text: btn ? btn.innerText.trim() : 'Not found',
                disabled: btn ? btn.disabled : null
            };
        })()
        """
        await ws.send(json.dumps({'id': 6, 'method': 'Runtime.evaluate', 'params': {'expression': check_send_btn, 'returnByValue': True}}))
        btn_status = json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value')
        print(f"Send code button status: {btn_status}")

        # Step 5: Click "Send code" button
        if btn_status and not btn_status.get('disabled') and btn_status.get('text') != 'Not found':
            print("Clicking Send code button...")
            click_send_js = """
            (() => {
                const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Send code'));
                if (btn) {
                    btn.click();
                    return 'Clicked Send code';
                }
                return 'Button not found';
            })()
            """
            await ws.send(json.dumps({'id': 7, 'method': 'Runtime.evaluate', 'params': {'expression': click_send_js, 'returnByValue': True}}))
            res_click = json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value')
            print(f"Click response: {res_click}")
            await asyncio.sleep(3.0)

            # Step 6: Verify confirmation or captcha
            verify_js = """
            JSON.stringify({
                body: document.body.innerText.substring(0, 400),
                sendBtnText: Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('code') || b.innerText.includes('Resend')) ? Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('code') || b.innerText.includes('Resend')).innerText.trim() : null,
                hasCaptcha: !!document.querySelector('#captcha-verify-image, [class*="captcha"], iframe[src*="captcha"]')
            })
            """
            await ws.send(json.dumps({'id': 8, 'method': 'Runtime.evaluate', 'params': {'expression': verify_js, 'returnByValue': True}}))
            verify_res = json.loads(json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value'))
            print("\nOutcome after Send code:")
            print(f"Send button text: {verify_res.get('sendBtnText')}")
            print(f"Has Captcha:      {verify_res.get('hasCaptcha')}")
            print(f"Body snippet:\n{verify_res.get('body')}")
        else:
            print("Send code button is disabled or not found.")

if __name__ == '__main__':
    asyncio.run(send_code())
