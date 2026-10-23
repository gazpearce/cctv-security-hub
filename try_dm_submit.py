import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def try_submit():
    tab_id = '2591DDE87B743DBFF72509D772E7D75B'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const form = document.querySelector('form');
            if (form) {
                form.requestSubmit ? form.requestSubmit() : form.submit();
                return 'Called form submit';
            }
            return 'No form';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print('Submit result:', raw)
        
        await asyncio.sleep(4)
        
        expr2 = """
        (() => {
            return {
                url: window.location.href,
                bodyText: document.body.innerText.slice(0, 800),
                inputs: Array.from(document.querySelectorAll('input')).map(i => ({type: i.type, name: i.name, id: i.id, placeholder: i.placeholder, value: i.value})),
                buttons: Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print('After submit:', json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(try_submit())
