import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_speakerdeck():
    tab_id = 'C48DFADC6D68706DAF5E12B0F783F8AE'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        await asyncio.sleep(2)
        expr = """
        (() => {
            return {
                url: window.location.href,
                title: document.title,
                bodySnippet: document.body.innerText.slice(0, 500),
                links: Array.from(document.querySelectorAll('a')).map(a => ({href: a.href, text: a.innerText.trim()})).filter(l => l.text)
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(inspect_speakerdeck())
