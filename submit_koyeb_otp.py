import asyncio
import websockets
import urllib.request
import json
import time

async def submit():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())
    koyeb_tab = next((t for t in tabs if 'koyeb' in t.get('url', '').lower()), None)
    async with websockets.connect(koyeb_tab['webSocketDebuggerUrl']) as ws:
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
            const input = document.querySelector('input[data-test="otp-input"]');
            if (input) {
                const nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeSetter.call(input, '927551');
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
                const form = input.closest('form');
                if (form) {
                    if (form.requestSubmit) form.requestSubmit();
                    else form.submit();
                }
                return 'Native setter called on otp-input';
            }
            return 'Input not found';
        })()"""
        res = await call('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        print("Submit result:", res.get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(submit())
