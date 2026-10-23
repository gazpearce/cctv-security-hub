import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def finish_rep():
    tab_id = 'F7B66244714ACD29CFD67763F83E332A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const input = document.querySelector('input');
            if (input) {
                input.value = 'admin@adicommunications.co.uk';
                input.dispatchEvent(new Event('input', { bubbles: true }));
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && (b.innerText.includes('Save') || b.innerText.includes('Continue') || b.innerText.includes('Next')));
            if (btn) {
                btn.click();
                return 'Clicked ' + btn.innerText;
            }
            return 'Btn not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print(raw)
        
        await asyncio.sleep(6)
        
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': '({ url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 400) })', 'returnByValue': True}}))
        raw2 = await ws.recv()
        print(json.dumps(json.loads(raw2).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(finish_rep())
