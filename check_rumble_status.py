import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    tab_id = 'B05DD5FD31627A501BCF11412B0DA3C8'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const btn = document.getElementById('submitForm');
            const btn2 = document.getElementById('submitForm2');
            const direct = document.getElementById('direct');
            return {
                url: window.location.href,
                submitDisabled: btn ? btn.disabled : null,
                submit2Present: !!btn2,
                directVal: direct ? direct.value : null,
                textSnippet: document.body.innerText.slice(0, 300)
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print(json.dumps(json.loads(raw).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(check())
