import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    tab_id = '4F7ED913AEDC12A93DB007D4E7665B1F'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const el = document.querySelector('[data-testid="age-verification-container"]');
            return {
                text: el ? el.innerText : 'not found',
                html: el ? el.innerHTML : 'not found'
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print("TEXT:", val.get('text'))
        print("HTML:\n", val.get('html')[:1000])

if __name__ == '__main__':
    asyncio.run(check())
