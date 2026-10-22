import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect():
    ws_url = "ws://127.0.0.1:9223/devtools/page/D554E1EBFF4A9880047E634AA7A9937D"
    async with websockets.connect(ws_url) as ws:
        script = """
        (() => {
            const all = Array.from(document.querySelectorAll('h3, p, div[data-selectable-paragraph], [contenteditable="true"]'));
            return all.map(el => ({
                tag: el.tagName,
                classes: el.className,
                placeholder: el.getAttribute('data-placeholder'),
                text: el.innerText.slice(0, 100)
            }));
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': script, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        for x in res.get('result', {}).get('result', {}).get('value', []):
            print(x)

if __name__ == '__main__':
    asyncio.run(inspect())
