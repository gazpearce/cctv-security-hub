import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def open_odysee_email():
    tab_id = '846D30CA5670110BE1B220763CEEA59A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Navigate to inbox directly
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://mail.google.com/mail/u/0/#inbox'}}))
        await ws.recv()
        await asyncio.sleep(4)
        
        # Find row containing Odysee and click it
        expr = """
        (() => {
            const rows = Array.from(document.querySelectorAll('tr[role="row"]'));
            const odyseeRow = rows.find(r => r.innerText.includes('Odysee'));
            if (odyseeRow) {
                odyseeRow.click();
                return 'Clicked Odysee row: ' + odyseeRow.innerText.slice(0, 100);
            }
            return 'Odysee row not found among ' + rows.length + ' rows';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print('Row click:', raw)
        
        await asyncio.sleep(4)
        
        # Extract links in the opened email
        expr2 = """
        (() => {
            const links = Array.from(document.querySelectorAll('div[role="main"] a')).map(a => ({
                href: a.href,
                text: a.innerText.trim()
            }));
            return links;
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        links = json.loads(raw2).get('result', {}).get('result', {}).get('value', [])
        print('Links found:', json.dumps(links, indent=2))
        
        for l in links:
            href = l.get('href', '')
            text = l.get('text', '')
            if 'odysee' in href or 'verify' in href.lower() or 'lbry' in href.lower() or 'Verify' in text:
                print('Found verification link:', href)
                import urllib.request
                req = urllib.request.Request(f'http://localhost:9223/json/new?{href}', method='PUT')
                resp = urllib.request.urlopen(req)
                print('Opened verification tab:', resp.read().decode())
                break

if __name__ == '__main__':
    asyncio.run(open_odysee_email())
