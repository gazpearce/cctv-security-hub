import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def find_pub():
    ws_url = 'ws://127.0.0.1:9223/devtools/page/45AD4F7EB5D4BF0E59AD5CA3F91B7817'
    async with websockets.connect(ws_url) as ws:
        # Check all links
        script = """
        (() => {
            const links = Array.from(document.querySelectorAll('a'));
            return links.map(a => ({href: a.href, text: a.innerText})).filter(x => x.href && !x.href.includes('javascript'));
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': script, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        for l in res.get('result', {}).get('result', {}).get('value', []):
            print(l['href'], '-->', repr(l['text']))

if __name__ == '__main__':
    asyncio.run(find_pub())
