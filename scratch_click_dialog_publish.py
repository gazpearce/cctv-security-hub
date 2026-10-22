import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def click_pub():
    ws_url = 'ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817'
    async with websockets.connect(ws_url) as ws:
        script = """
        (() => {
            const dialog = document.querySelector('*[role="dialog"]');
            if (!dialog) return 'No dialog found';
            const btns = Array.from(dialog.querySelectorAll('button'));
            const pubBtn = btns.find(b => b.innerText.trim() === 'Publish');
            if (pubBtn) {
                pubBtn.click();
                return 'Clicked Publish in dialog';
            }
            return 'Publish button not found in dialog. Buttons: ' + btns.map(b => b.innerText).join(', ');
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': script}}))
        res = json.loads(await ws.recv())
        print(res.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(6)
        
        # Check URL and title after publish
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': 'JSON.stringify({url: window.location.href, title: document.title})'}}))
        res2 = json.loads(await ws.recv())
        print("After publish:", res2.get('result', {}).get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(click_pub())
