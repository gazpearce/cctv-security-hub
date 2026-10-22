import asyncio
import json
import websockets

async def submit_rtd():
    tab_id = "77C5B12D0511BE742784797468F7EE9D"
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{tab_id}", max_size=25*1024*1024) as ws:
        expr = """
        (() => {
            const form = document.querySelector('form');
            if (form) {
                form.submit();
                return 'Form submitted';
            }
            return 'Form not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        print("Submit RTD:", res.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(4)
        
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': '({url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 300)})', 'returnByValue': True}}))
        res2 = json.loads(await ws.recv())
        print("After RTD:", json.dumps(res2.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(submit_rtd())
