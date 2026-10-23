import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def nav_dailymotion_studio():
    tab_id = '2591DDE87B743DBFF72509D772E7D75B'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Navigate to partner studio
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://studio.dailymotion.com/'}}))
        raw = await ws.recv()
        print('Navigated:', raw)
        
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
    asyncio.run(nav_dailymotion_studio())
