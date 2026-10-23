import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check_inbox_latest():
    tab_id = '846D30CA5670110BE1B220763CEEA59A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Navigate to inbox
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://mail.google.com/mail/u/0/#inbox'}}))
        await ws.recv()
        await asyncio.sleep(4)
        
        expr = """
        (() => {
            const rows = Array.from(document.querySelectorAll('tr[role="row"]')).slice(0, 10).map(r => ({
                sender: (r.querySelector('span[email]') || r.querySelector('.yX.xY') || {}).innerText || '',
                subject: (r.querySelector('.bog') || {}).innerText || '',
                snippet: (r.querySelector('.y2') || {}).innerText || '',
                date: (r.querySelector('.xW') || {}).innerText || ''
            }));
            return rows;
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', [])
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(check_inbox_latest())
