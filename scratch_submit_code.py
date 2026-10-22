import asyncio
import json
import websockets

async def submit_code():
    ws_url = "ws://127.0.0.1:9223/devtools/page/C8AC94E331D5E7707203F724DC068AD7"
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        expr = """
        (() => {
            const inputs = Array.from(document.querySelectorAll('input'));
            const textInput = inputs.find(i => i.type === 'text' || i.type === 'number' || !i.type);
            if (!textInput) return 'No text input found among ' + inputs.length + ' inputs';
            
            textInput.focus();
            textInput.value = '06861167';
            textInput.dispatchEvent(new Event('input', { bubbles: true }));
            textInput.dispatchEvent(new Event('change', { bubbles: true }));
            
            const btns = Array.from(document.querySelectorAll('button, input[type="submit"]'));
            const verifyBtn = btns.find(b => (b.innerText || b.value || '').toLowerCase().includes('verify'));
            if (verifyBtn) {
                verifyBtn.click();
                return 'Filled 06861167 and clicked ' + (verifyBtn.innerText || verifyBtn.value);
            }
            return 'Filled 06861167 but verify button not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        print("Submit action:", res.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(4)
        
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': '({url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 300)})', 'returnByValue': True}}))
        res2 = json.loads(await ws.recv())
        print("Page after submit:", json.dumps(res2.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(submit_code())
