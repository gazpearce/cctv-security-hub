import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def test_upload():
    tab_id = '2591DDE87B743DBFF72509D772E7D75B'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Click "Add video" or "Start uploading your content"
        expr = """
        (() => {
            const addBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Add video' || b.innerText.trim() === 'Start uploading your content');
            if (addBtn) {
                addBtn.click();
                return 'Clicked: ' + addBtn.innerText;
            }
            return 'Button not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print(raw)
        
        await asyncio.sleep(2)
        
        # Check what appeared
        expr2 = """
        (() => {
            const inputs = Array.from(document.querySelectorAll('input[type="file"]')).map(i => ({
                id: i.id,
                name: i.name,
                accept: i.accept,
                className: i.className
            }));
            return {
                url: window.location.href,
                fileInputs: inputs,
                bodyText: document.body.innerText.slice(0, 600)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        print(json.dumps(json.loads(raw2).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(test_upload())
