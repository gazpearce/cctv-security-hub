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
            const btn = document.querySelector('button[name="authorize"][value="1"]');
            if (btn) {
                const form = btn.closest('form');
                if (form) {
                    let hidden = form.querySelector('input[type="hidden"][name="authorize"]');
                    if (!hidden) {
                        hidden = document.createElement('input');
                        hidden.type = 'hidden';
                        hidden.name = 'authorize';
                        form.appendChild(hidden);
                    }
                    hidden.value = '1';
                    form.submit();
                    return 'Form submitted with authorize=1';
                }
            }
            return 'Btn not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print(raw)
        
        await asyncio.sleep(8)
        
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': '({ url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 400) })', 'returnByValue': True}}))
        raw2 = await ws.recv()
        print(json.dumps(json.loads(raw2).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(submit())
