import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check_speakerdeck_upload():
    tab_id = 'C48DFADC6D68706DAF5E12B0F783F8AE'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://speakerdeck.com/new'}}))
        raw = await ws.recv()
        print('Navigated:', raw)
        
        await asyncio.sleep(4)
        
        expr = """
        (() => {
            return {
                url: window.location.href,
                title: document.title,
                bodySnippet: document.body.innerText.slice(0, 800),
                inputs: Array.from(document.querySelectorAll('input, select, textarea')).map(e => ({
                    tag: e.tagName,
                    type: e.type,
                    name: e.name,
                    id: e.id,
                    placeholder: e.placeholder
                })),
                buttons: Array.from(document.querySelectorAll('button, input[type="submit"]')).map(b => b.innerText || b.value).filter(Boolean)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(check_speakerdeck_upload())
