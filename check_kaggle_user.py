import asyncio
import websockets
import urllib.request
import json

async def check_k_user():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())
    k_tab = next(t for t in tabs if 'kaggle' in t.get('url', '').lower() and t.get('type') == 'page')
    async with websockets.connect(k_tab['webSocketDebuggerUrl']) as ws:
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
            const avatar = document.querySelector('img[alt*="User avatar"], [data-testid="user-avatar"], a[href*="/profile"], [aria-label*="User Profile"]');
            const signIn = Array.from(document.querySelectorAll('a, button')).find(b => (b.innerText || '').toLowerCase().includes('sign in'));
            return {
                avatar: avatar ? avatar.outerHTML : null,
                signIn: signIn ? signIn.innerText : null
            };
        })()"""
        res = await call('Runtime.evaluate', {'expression': expr, 'returnByValue': True})
        print(json.dumps(res.get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(check_k_user())
