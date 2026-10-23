import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check_zenodo():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'DOM.enable'}))
        await ws.recv()
        
        await ws.send(json.dumps({'id': 2, 'method': 'DOM.getDocument'}))
        doc_raw = await ws.recv()
        print('doc_raw:', doc_raw[:200])
        root_id = json.loads(doc_raw).get('result', {}).get('root', {}).get('nodeId')
        print('root_id:', root_id)
        
        await ws.send(json.dumps({'id': 3, 'method': 'DOM.querySelector', 'params': {'nodeId': root_id, 'selector': 'input[type="file"]'}}))
        q_raw = await ws.recv()
        print('q_raw:', q_raw)

if __name__ == '__main__':
    asyncio.run(check_zenodo())
