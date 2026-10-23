import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def onboard_hn():
    tab_id = 'F7B66244714ACD29CFD67763F83E332A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, a, [role="button"]')).map(el => ({
                tag: el.tagName,
                className: el.className,
                href: el.href,
                ariaLabel: el.getAttribute('aria-label'),
                text: el.innerText ? el.innerText.trim() : ''
            }));
            return btns.filter(b => b.ariaLabel || (b.href && (b.href.includes('github') || b.href.includes('google') || b.href.includes('oauth'))));
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        btns = json.loads(raw).get('result', {}).get('result', {}).get('value', [])
        print("Social btns:", json.dumps(btns, indent=2))
        
        # Click the GitHub or Google button
        expr_click = """
        (() => {
            const btn = Array.from(document.querySelectorAll('button, a')).find(b => {
                const label = (b.getAttribute('aria-label') || '').toLowerCase();
                const text = (b.innerText || '').toLowerCase();
                const href = (b.href || '').toLowerCase();
                return label.includes('github') || text.includes('github') || href.includes('github');
            });
            if (btn) {
                btn.click();
                return 'Clicked GitHub button';
            }
            return 'GitHub button not found';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr_click, 'returnByValue': True}}))
        raw2 = await ws.recv()
        print("Click result:", raw2)
        
        await asyncio.sleep(8)
        
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': '({ url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 300) })', 'returnByValue': True}}))
        raw3 = await ws.recv()
        print("Destination:\n", json.dumps(json.loads(raw3).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(onboard_hn())
