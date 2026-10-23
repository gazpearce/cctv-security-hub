import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def authorize():
    tab_id = 'F7B66244714ACD29CFD67763F83E332A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Find all submit buttons and forms
        expr = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, input[type="submit"]')).map(b => ({
                id: b.id,
                name: b.name,
                value: b.value,
                text: b.innerText ? b.innerText.trim() : '',
                className: b.className
            }));
            return btns;
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        btns = json.loads(raw).get('result', {}).get('result', {}).get('value', [])
        print("Buttons on page:", json.dumps(btns, indent=2))
        
        # Click the authorize button
        expr_click = """
        (() => {
            const btn = document.getElementById('js-oauth-authorize-btn') || Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Authorize'));
            if (btn) {
                btn.click();
                return 'Clicked: ' + btn.innerText;
            }
            return 'Authorize button not found';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr_click, 'returnByValue': True}}))
        raw2 = await ws.recv()
        print("Click result:", raw2)
        
        await asyncio.sleep(8)
        
        # Check destination
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': '({ url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 400) })', 'returnByValue': True}}))
        raw3 = await ws.recv()
        print("Destination:\n", json.dumps(json.loads(raw3).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(authorize())
