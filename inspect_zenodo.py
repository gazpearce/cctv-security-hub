import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_zenodo():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            return {
                url: window.location.href,
                title: document.title,
                bodyText: document.body.innerText.slice(0, 800),
                links: Array.from(document.querySelectorAll('a')).map(a => ({href: a.href, text: a.innerText.trim()})).filter(l => l.text)
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(inspect_zenodo())
