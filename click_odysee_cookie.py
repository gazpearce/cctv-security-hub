import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def click_allow_all():
    tab_id = '1A6B5AF6ECF7A9F5D083FC8879A4D8FF'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Allow All');
            if (btn) {
                btn.click();
                return 'Clicked Allow All';
            }
            return 'Button not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print('Cookie click:', raw)
        
        await asyncio.sleep(4)
        
        expr2 = """
        (() => {
            return {
                url: window.location.href,
                bodyText: document.body.innerText.slice(0, 1000),
                buttons: Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print('State after cookie:', json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(click_allow_all())
