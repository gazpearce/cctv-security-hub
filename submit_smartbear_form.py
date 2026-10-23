import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def submit():
    tab_id = 'F7B66244714ACD29CFD67763F83E332A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const form = document.forms[1];
            if (form) {
                form.querySelector('input[name="firstName"]').value = 'Gary';
                form.querySelector('input[name="lastName"]').value = 'Pearce';
                form.querySelector('input[name="trialFields.phone"]').value = '07860 244 274';
                form.querySelector('input[name="trialFields.company"]').value = 'ADI Communications';
                form.submit();
                return 'Submitted form[1]';
            }
            return 'Form not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print(raw)
        
        await asyncio.sleep(8)
        
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': '({ url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 400) })', 'returnByValue': True}}))
        raw2 = await ws.recv()
        print("Final Destination:\n", json.dumps(json.loads(raw2).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(submit())
