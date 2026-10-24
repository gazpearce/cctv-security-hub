import asyncio
import websockets
import json
import sys

async def send_cmd(ws, method, params=None, msg_id=1):
    req = {'id': msg_id, 'method': method}
    if params:
        req['params'] = params
    await ws.send(json.dumps(req))
    while True:
        resp_raw = await asyncio.wait_for(ws.recv(), timeout=10.0)
        resp = json.loads(resp_raw)
        if resp.get('id') == msg_id:
            return resp

async def enter_code(code):
    uri = 'ws://localhost:9223/devtools/page/76CC99643C9BDB39C51016640626E071'
    async with websockets.connect(uri) as ws:
        # Focus code input
        focus_js = """(() => {
            const input = document.querySelector('input[placeholder*="code"], input[placeholder*="6-digit"]');
            if (input) {
                input.focus();
                input.value = '';
                return true;
            }
            return false;
        })()"""
        res = await send_cmd(ws, 'Runtime.evaluate', {'expression': focus_js, 'returnByValue': True}, msg_id=1)
        if not res['result']['result']['value']:
            print("Could not find code input field!")
            return

        # Insert code via Input.insertText
        await send_cmd(ws, 'Input.insertText', {'text': code}, msg_id=2)
        print(f"Entered code {code}")

        # Wait 500ms
        await asyncio.sleep(0.5)

        # Click Log In button
        click_js = """(() => {
            const btns = Array.from(document.querySelectorAll('button'));
            const loginBtn = btns.find(b => b.innerText.trim() === 'Log in' && !b.disabled);
            if (loginBtn) {
                loginBtn.click();
                return 'Clicked Log in';
            }
            return 'Log in button still disabled or not found';
        })()"""
        res3 = await send_cmd(ws, 'Runtime.evaluate', {'expression': click_js, 'returnByValue': True}, msg_id=3)
        print(res3['result']['result']['value'])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python enter_tiktok_code.py <6-digit-code>")
    else:
        asyncio.run(enter_code(sys.argv[1]))
