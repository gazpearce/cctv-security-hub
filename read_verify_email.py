import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check_email_content():
    tab_id = '846D30CA5670110BE1B220763CEEA59A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const body = document.querySelector('div[role="main"]');
            return {
                title: document.title,
                url: window.location.href,
                text: body ? body.innerText.slice(0, 1500) : document.body.innerText.slice(0, 1500)
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(check_email_content())
