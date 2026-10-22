import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    tab_id = '2591DDE87B743DBFF72509D772E7D75B'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Network.enable'}))
        await ws.recv()
        
        # Click the button
        expr = """
        (() => {
            const b = document.querySelector('.src-common-components-email-confirmation-banner-index-module__button--roEdx');
            if (b) { b.click(); return 'Clicked'; }
            return 'Not found';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print("Click result:", raw)
        
        # Listen for network events for 5 seconds
        for _ in range(20):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=0.5)
                data = json.loads(msg)
                method = data.get('method', '')
                if 'Network.requestWillBeSent' in method:
                    req = data.get('params', {}).get('request', {})
                    print("REQUEST:", req.get('method'), req.get('url'))
                elif 'Network.responseReceived' in method:
                    resp = data.get('params', {}).get('response', {})
                    print("RESPONSE:", resp.get('status'), resp.get('url'))
            except asyncio.TimeoutError:
                pass

if __name__ == '__main__':
    asyncio.run(check())
