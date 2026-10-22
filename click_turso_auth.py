import asyncio
import websockets
import urllib.request
import json
import time

async def auth_turso():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())
    turso_tab = next(t for t in tabs if 'clerk.turso.tech' in t.get('url', '') or 'Authorize application' in t.get('title', ''))
    async with websockets.connect(turso_tab['webSocketDebuggerUrl']) as ws:
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
                return 'Clicked Authorize Turso';
            }
            return 'Button not found';
        })()"""
        res = await call('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        print(res.get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(auth_turso())
