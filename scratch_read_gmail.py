import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def read_gmail():
    gm_tab = "846D30CA5670110BE1B220763CEEA59A"
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{gm_tab}", max_size=25*1024*1024) as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': 'document.body.innerText', 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        text = res.get('result', {}).get('result', {}).get('value', '')
        print("GMAIL_LENGTH:", len(text))
        print("GMAIL_PREVIEW:\n", text[:2500])

if __name__ == '__main__':
    asyncio.run(read_gmail())
