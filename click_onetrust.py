import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def dismiss_onetrust():
    tab_id = '1A6B5AF6ECF7A9F5D083FC8879A4D8FF'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const btn = document.getElementById('accept-recommended-btn-handler');
            if (btn) {
                btn.click();
                return 'Clicked accept-recommended-btn-handler';
            }
            return 'Btn not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print('Click result:', raw)
        
        await asyncio.sleep(3)
        
        expr2 = """
        (() => {
            return {
                url: window.location.href,
                bodyText: document.body.innerText.slice(0, 1000)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print('Page state:', json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(dismiss_onetrust())
