import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def login_dailymotion_cdp():
    tab_id = '2591DDE87B743DBFF72509D772E7D75B'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Focus input and select all
        focus_expr = """
        (() => {
            const input = document.querySelector('input#username') || document.querySelector('input[name="username"]');
            if (input) {
                input.focus();
                input.select();
                return true;
            }
            return false;
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': focus_expr, 'returnByValue': True}}))
        await ws.recv()
        
        # Type via Input.insertText
        await ws.send(json.dumps({'id': 2, 'method': 'Input.insertText', 'params': {'text': 'aiagent1510@gmail.com'}}))
        await ws.recv()
        
        await asyncio.sleep(1)
        
        # Press Enter key
        await ws.send(json.dumps({'id': 3, 'method': 'Input.dispatchKeyEvent', 'params': {'type': 'rawKeyDown', 'windowsVirtualKeyCode': 13, 'unmodifiedText': '\r', 'text': '\r'}}))
        await ws.recv()
        await ws.send(json.dumps({'id': 4, 'method': 'Input.dispatchKeyEvent', 'params': {'type': 'keyUp', 'windowsVirtualKeyCode': 13}}))
        await ws.recv()
        
        print("Sent keystrokes")
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
        await ws.send(json.dumps({'id': 5, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print('Result:', json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(login_dailymotion_cdp())
