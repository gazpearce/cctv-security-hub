import asyncio
import websockets
import urllib.request
import json
import time

async def auth_sentry():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())
    sentry_tab = next((t for t in tabs if 'Authorize Sentry' in t.get('title', '') or 'sentry' in t.get('url', '').lower()), None)
    if not sentry_tab:
        print("Tab not found")
        return
    print("Connecting to:", sentry_tab['url'])
    async with websockets.connect(sentry_tab['webSocketDebuggerUrl']) as ws:
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
            const btn = document.querySelector('button[name="authorize"][value="1"], .js-oauth-authorize-btn') || Array.from(document.querySelectorAll('button')).find(b => b.innerText.toLowerCase().includes('authorize'));
            if (btn) {
                btn.disabled = false;
                btn.click();
                return 'Clicked Authorize Sentry';
            }
            return 'Button not found';
        })()"""
        res = await call('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        print(res.get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(auth_sentry())
