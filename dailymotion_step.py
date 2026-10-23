import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def login_dailymotion():
    tab_id = '2591DDE87B743DBFF72509D772E7D75B'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const input = document.querySelector('input#username') || document.querySelector('input[name="username"]');
            if (!input) return 'Username input not found';
            
            input.focus();
            const nativeInputValueSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, "value").set;
            nativeInputValueSetter.call(input, 'aiagent1510@gmail.com');
            input.dispatchEvent(new Event('input', { bubbles: true }));
            input.dispatchEvent(new Event('change', { bubbles: true }));
            
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Continue');
            if (btn) {
                btn.removeAttribute('disabled');
                btn.click();
                return 'Filled with native setter and clicked Continue. disabled=' + btn.disabled;
            }
            return 'Continue button not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print('Step 1:', raw)
        
        await asyncio.sleep(4)
        
        expr2 = """
        (() => {
            return {
                url: window.location.href,
                bodyText: document.body.innerText.slice(0, 1000),
                inputs: Array.from(document.querySelectorAll('input')).map(i => ({type: i.type, name: i.name, id: i.id, placeholder: i.placeholder, value: i.value})),
                buttons: Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print('Step 2:', json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(login_dailymotion())
