import urllib.request
import json
import asyncio
import websockets

async def check_circleci():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())
    circle_tab = next(t for t in tabs if 'circleci' in t.get('url', '').lower())
    ws_url = circle_tab['webSocketDebuggerUrl']
    print("Found CircleCI tab:", circle_tab['url'])
    
    async with websockets.connect(ws_url) as ws:
        msg_id = 1
        async def call(method, params=None):
            nonlocal msg_id
            msg_id += 1
            await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get('id') == msg_id:
                    return resp.get('result', {})

        # Check DOM text
        res = await call('Runtime.evaluate', {'expression': 'document.body.innerText'})
        text = res.get('result', {}).get('value', '')
        print('=== CIRCLECI INNER TEXT ===')
        print(text)
        
        # Check current inputs / buttons
        inputs = await call('Runtime.evaluate', {
            'expression': '''(() => {
                const els = Array.from(document.querySelectorAll("input, button, a"));
                return els.map(e => ({
                    tag: e.tagName,
                    type: e.type || "",
                    name: e.name || "",
                    id: e.id || "",
                    value: e.value || "",
                    text: e.innerText || "",
                    href: e.href || ""
                }));
            })()''',
            'returnByValue': True
        })
        print('=== INPUTS / BUTTONS ===')
        print(json.dumps(inputs.get('result', {}).get('value', []), indent=2))

if __name__ == '__main__':
    asyncio.run(check_circleci())
