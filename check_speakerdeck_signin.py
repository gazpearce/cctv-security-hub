import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def nav_speakerdeck_signup():
    tab_id = 'C48DFADC6D68706DAF5E12B0F783F8AE'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://speakerdeck.com/signin'}}))
        raw = await ws.recv()
        await asyncio.sleep(3)
        
        expr = """
        (() => {
            return {
                url: window.location.href,
                bodySnippet: document.body.innerText.slice(0, 800),
                links: Array.from(document.querySelectorAll('a, button')).map(e => ({tag: e.tagName, text: e.innerText.trim(), href: e.href || ''})).filter(x => x.text)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(nav_speakerdeck_signup())
