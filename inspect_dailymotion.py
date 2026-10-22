import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect():
    tab_id = '2591DDE87B743DBFF72509D772E7D75B'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const btns = Array.from(document.querySelectorAll('button, a, input[type="file"], input')).map(el => ({
                tag: el.tagName,
                type: el.type,
                id: el.id,
                text: el.innerText ? el.innerText.trim() : '',
                name: el.name,
                placeholder: el.placeholder
            }));
            return {
                url: window.location.href,
                title: document.title,
                textSample: document.body.innerText.slice(0, 500),
                elements: btns.filter(b => b.text || b.type === 'file' || b.id || b.placeholder)
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        data = json.loads(raw)
        print(json.dumps(data.get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(inspect())
