import json
import asyncio
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

TAB_ID = "76CC99643C9BDB39C51016640626E071"

async def check():
    url = f"ws://127.0.0.1:9223/devtools/page/{TAB_ID}"
    async with websockets.connect(url, max_size=20*1024*1024) as ws:
        expr = """
        (() => {
            const sendBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Send code') || b.innerText.includes('Resend'));
            const phoneInput = document.querySelector('input[name="mobile"]');
            const codeInput = document.querySelector('input[placeholder*="code"]');
            const errors = Array.from(document.querySelectorAll('[role="alert"], [class*="error"], [class*="Error"]')).map(e => e.innerText.trim()).filter(Boolean);
            const dialog = document.querySelector('[role="dialog"]');
            
            return {
                phoneVal: phoneInput ? phoneInput.value : null,
                sendBtnText: sendBtn ? sendBtn.innerText.trim() : null,
                sendBtnDisabled: sendBtn ? sendBtn.disabled : null,
                hasCodeInput: !!codeInput,
                errors,
                dialogText: dialog ? dialog.innerText.substring(0, 200) : null
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        res = json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value')
        print(json.dumps(res, indent=2))

if __name__ == '__main__':
    asyncio.run(check())
