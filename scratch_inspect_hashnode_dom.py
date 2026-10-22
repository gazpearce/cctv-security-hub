import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect():
    ws_url = 'ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817'
    async with websockets.connect(ws_url) as ws:
        script = """(() => {
            return Array.from(document.querySelectorAll('button, a, [role="button"]')).map(el => ({
                tag: el.tagName,
                text: el.innerText.trim(),
                aria: el.getAttribute('aria-label'),
                classes: el.className
            })).filter(x => x.text || x.aria);
        })()"""
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': script, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        items = res.get('result', {}).get('result', {}).get('value', [])
        for item in items:
            print(item)

if __name__ == '__main__':
    asyncio.run(inspect())
