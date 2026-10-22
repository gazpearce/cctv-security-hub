import asyncio
import json
import websockets
import sys

async def eval_tab(tab_id, expr):
    ws_url = f"ws://127.0.0.1:9223/devtools/page/{tab_id}"
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        val = res.get('result', {}).get('result', {}).get('value')
        print(f"Result for {tab_id}:")
        sys.stdout.reconfigure(encoding='utf-8')
        if isinstance(val, (dict, list)):
            print(json.dumps(val, indent=2))
        else:
            print(str(val)[:2000])

if __name__ == '__main__':
    tab_id = sys.argv[1]
    expr = sys.argv[2]
    asyncio.run(eval_tab(tab_id, expr))
