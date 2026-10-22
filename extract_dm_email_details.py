import asyncio
import json
import re
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    tab_id = '846D30CA5670110BE1B220763CEEA59A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const el = document.querySelector('.ii.gt') || document.querySelector('[role="main"]');
            return {
                text: el ? el.innerText : 'not found',
                html: el ? el.innerHTML : 'not found'
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print("EMAIL BODY TEXT:\n", val.get('text'))
        links = re.findall(r'href=[\'"](https?://[^\'"]+)', val.get('html', ''))
        print("\nALL LINKS:")
        for l in set(links):
            print(" -", l)

if __name__ == '__main__':
    asyncio.run(check())
