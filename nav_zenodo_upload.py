import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def nav_zenodo_upload():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://zenodo.org/uploads/new'}}))
        raw = await ws.recv()
        print('Navigated to upload:', raw)
        
        await asyncio.sleep(4)
        
        expr = """
        (() => {
            return {
                url: window.location.href,
                title: document.title,
                bodyText: document.body.innerText.slice(0, 1000),
                inputs: Array.from(document.querySelectorAll('input')).map(i => ({type: i.type, name: i.name, id: i.id, placeholder: i.placeholder})),
                buttons: Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(nav_zenodo_upload())
