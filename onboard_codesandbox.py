import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def onboard_codesandbox():
    tab_id = 'F7B66244714ACD29CFD67763F83E332A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        print("Navigating to https://codesandbox.io/signin...")
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://codesandbox.io/signin'}}))
        await ws.recv()
        await asyncio.sleep(6)
        
        # Click Sign in with GitHub
        expr = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, a'));
            const ghBtn = btns.find(b => b.innerText && b.innerText.includes('GitHub'));
            if (ghBtn) {
                ghBtn.click();
                return 'Clicked: ' + ghBtn.innerText;
            }
            return 'Button not found, visible: ' + btns.map(b => b.innerText.trim()).filter(Boolean).slice(0, 10).join(' | ');
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print(raw)
        
        await asyncio.sleep(6)
        
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': '({ url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 300) })', 'returnByValue': True}}))
        raw2 = await ws.recv()
        print(json.dumps(json.loads(raw2).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(onboard_codesandbox())
