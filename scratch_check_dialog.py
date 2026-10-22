import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    ws_url = 'ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817'
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.location.href'}}))
        print('URL:', json.loads(await ws.recv())['result']['result']['value'])
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': 'document.querySelector("*[role=dialog]") ? document.querySelector("*[role=dialog]").innerText : "No dialog"'}}))
        print('Dialog:', json.loads(await ws.recv())['result']['result']['value'])
        # Also check all visible text in modals or overlays
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': '''
            (() => {
                const dialogs = Array.from(document.querySelectorAll('[role="dialog"], [data-state="open"]'));
                return dialogs.map(d => ({
                    role: d.getAttribute('role'),
                    text: d.innerText.slice(0, 300)
                }));
            })()
        ''', 'returnByValue': True}}))
        print('Dialogs:', json.loads(await ws.recv()).get('result', {}).get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(check())
