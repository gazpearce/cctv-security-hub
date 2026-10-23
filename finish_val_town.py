import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def finish_val():
    tab_id = 'F7B66244714ACD29CFD67763F83E332A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, input, [role="button"], [role="radio"]')).map(el => ({
                tag: el.tagName,
                type: el.type,
                role: el.getAttribute('role'),
                text: el.innerText ? el.innerText.trim() : ''
            }));
            return btns;
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print("Elements:", json.dumps(json.loads(raw).get('result', {}).get('result', {}).get('value', []), indent=2))
        
        # Click Work specifically
        expr2 = """
        (() => {
            const workBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Work');
            if (workBtn) {
                workBtn.click();
                return 'Clicked Work button';
            }
            return 'Work button not found';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        print(raw2)
        
        await asyncio.sleep(2)
        
        # Click Continue
        expr3 = """
        (() => {
            const cont = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.includes('Continue'));
            if (cont) {
                cont.click();
                return 'Clicked Continue';
            }
            return 'Continue not found';
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': expr3, 'returnByValue': True}}))
        raw3 = await ws.recv()
        print(raw3)
        
        await asyncio.sleep(6)
        
        await ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': '({ url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 400) })', 'returnByValue': True}}))
        raw4 = await ws.recv()
        print("Final State:\n", json.dumps(json.loads(raw4).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(finish_val())
