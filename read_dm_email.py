import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check():
    tab_id = '846D30CA5670110BE1B220763CEEA59A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const rows = Array.from(document.querySelectorAll('tr[role="row"]'));
            const dmRow = rows.find(r => r.innerText.includes('Dailymotion') || r.innerText.includes('372882'));
            if (dmRow) {
                dmRow.click();
                return 'Clicked Dailymotion email';
            }
            return 'Dailymotion email row not found, visible rows: ' + rows.length;
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print(raw)
        
        await asyncio.sleep(3)
        
        # Read opened email body & links
        expr2 = """
        (() => {
            const links = Array.from(document.querySelectorAll('a')).map(a => ({
                href: a.href,
                text: a.innerText.trim()
            })).filter(l => l.href && (l.href.includes('dailymotion') || l.text.includes('Dailymotion') || l.text.includes('Verify') || l.text.includes('confirm')));
            
            return {
                text: document.body.innerText.slice(0, 1500),
                links: links
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        data = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print("Links found:", json.dumps(data.get('links', []), indent=2))
        print("Body snippet:\n", data.get('text', '')[:600])

if __name__ == '__main__':
    asyncio.run(check())
