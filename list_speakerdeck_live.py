import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def list_user_decks():
    tab_id = 'C48DFADC6D68706DAF5E12B0F783F8AE'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://speakerdeck.com/aiagent1510'}}))
        await ws.recv()
        await asyncio.sleep(4)
        
        expr = """
        (() => {
            const decks = Array.from(document.querySelectorAll('.deck-preview, .talk-preview, a')).filter(a => a.href && a.href.includes('/aiagent1510/') && !a.href.endsWith('/bookmarks') && !a.href.endsWith('/stars') && !a.href.endsWith('/followers') && !a.href.endsWith('/following')).map(a => ({
                href: a.href,
                title: a.innerText.trim()
            })).filter(d => d.title.length > 5);
            return {
                url: window.location.href,
                decks: decks
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(list_user_decks())
