import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def nav_write():
    ws_url = "ws://127.0.0.1:9223/devtools/page/D554E1EBFF4A9880047E634AA7A9937D"
    async with websockets.connect(ws_url) as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://medium.com/new-story'}}))
        await ws.recv()
        await asyncio.sleep(4)
        script = """
        (() => {
            return {
                url: window.location.href,
                title: document.title,
                text: document.body.innerText.slice(0, 400),
                elements: Array.from(document.querySelectorAll('h3, [contenteditable="true"], textarea, button')).map(el => ({
                    tag: el.tagName,
                    placeholder: el.getAttribute('data-placeholder') || el.placeholder,
                    text: el.innerText.trim()
                })).filter(x => x.text || x.placeholder)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': script, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        print(json.dumps(res.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(nav_write())
