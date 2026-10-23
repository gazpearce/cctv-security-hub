import asyncio
import json
import websockets
import sys

async def check():
    tab_id = 'C48DFADC6D68706DAF5E12B0F783F8AE'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': '({url: window.location.href, title: document.title})', 'returnByValue': True}}))
        raw = await ws.recv()
        print(json.loads(raw).get('result', {}).get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(check())
