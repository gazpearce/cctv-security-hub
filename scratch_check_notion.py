import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    ws_url = "ws://127.0.0.1:9223/devtools/page/52BC33CC388F8391F3CCC729E1E70F7F"
    async with websockets.connect(ws_url) as ws:
        script = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, [role="button"]'));
            const shareBtn = btns.find(b => b.innerText.trim() === 'Share');
            if (shareBtn) {
                shareBtn.click();
                return 'Clicked Share button in Notion';
            }
            return 'Share button not found. Buttons: ' + btns.map(b => b.innerText.trim()).filter(Boolean).slice(0, 10).join(', ');
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': script}}))
        res = json.loads(await ws.recv())
        print(res.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(2)
        
        check_menu = """
        (() => {
            const popovers = Array.from(document.querySelectorAll('[role="dialog"], [role="menu"], .notion-scroller'));
            return Array.from(document.querySelectorAll('button, a, input')).map(el => el.innerText || el.value || el.placeholder).filter(Boolean).slice(0, 30);
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': check_menu, 'returnByValue': True}}))
        res2 = json.loads(await ws.recv())
        print("Menu items:", res2.get('result', {}).get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(check())
