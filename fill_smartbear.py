import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def fill_smartbear():
    tab_id = 'F7B66244714ACD29CFD67763F83E332A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const fn = document.querySelector('input[name="firstName"]');
            if (fn) { fn.value = 'Gary'; fn.dispatchEvent(new Event('input', { bubbles: true })); fn.dispatchEvent(new Event('change', { bubbles: true })); }
            const ln = document.querySelector('input[name="lastName"]');
            if (ln) { ln.value = 'Pearce'; ln.dispatchEvent(new Event('input', { bubbles: true })); ln.dispatchEvent(new Event('change', { bubbles: true })); }
            const ph = document.querySelector('input[name="trialFields.phone"]');
            if (ph) { ph.value = '07860 244 274'; ph.dispatchEvent(new Event('input', { bubbles: true })); ph.dispatchEvent(new Event('change', { bubbles: true })); }
            const comp = document.querySelector('input[name="trialFields.company"]');
            if (comp) { comp.value = 'ADI Communications'; comp.dispatchEvent(new Event('input', { bubbles: true })); comp.dispatchEvent(new Event('change', { bubbles: true })); }
            
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText && b.innerText.trim() === 'Start Trial');
            if (btn) {
                btn.click();
                return 'Filled details and clicked Start Trial';
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
        print("Final State:\n", json.dumps(json.loads(raw2).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(fill_smartbear())
