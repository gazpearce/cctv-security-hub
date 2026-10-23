import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def search_and_open_odysee():
    tab_id = '846D30CA5670110BE1B220763CEEA59A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Search for odysee in Gmail search box
        expr = """
        (() => {
            const q = document.querySelector('input[name="q"]') || document.querySelector('input[aria-label="Search mail"]');
            if (q) {
                q.focus();
                q.value = 'odysee';
                q.dispatchEvent(new Event('input', { bubbles: true }));
                return 'Filled search box';
            }
            return 'Search box not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print('Search input:', raw)
        
        # Press Enter
        await ws.send(json.dumps({'id': 2, 'method': 'Input.dispatchKeyEvent', 'params': {'type': 'rawKeyDown', 'windowsVirtualKeyCode': 13, 'unmodifiedText': '\r', 'text': '\r'}}))
        await ws.recv()
        await ws.send(json.dumps({'id': 3, 'method': 'Input.dispatchKeyEvent', 'params': {'type': 'keyUp', 'windowsVirtualKeyCode': 13}}))
        await ws.recv()
        
        await asyncio.sleep(4)
        
        # Click the row
        expr2 = """
        (() => {
            const row = document.querySelector('tr[role="row"]');
            if (row) {
                const text = row.innerText;
                row.click();
                return 'Clicked row: ' + text.slice(0, 100);
            }
            return 'No row found';
        })()
        """
        await ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        print('Click row:', raw2)
        
        await asyncio.sleep(4)
        
        # Extract links in email
        expr3 = """
        (() => {
            const links = Array.from(document.querySelectorAll('div[role="main"] a')).map(a => ({
                href: a.href,
                text: a.innerText.trim()
            }));
            return links;
        })()
        """
        await ws.send(json.dumps({'id': 5, 'method': 'Runtime.evaluate', 'params': {'expression': expr3, 'returnByValue': True}}))
        raw3 = await ws.recv()
        links = json.loads(raw3).get('result', {}).get('result', {}).get('value', [])
        print('Links in email:', json.dumps(links, indent=2))
        
        for l in links:
            href = l.get('href', '')
            if 'odysee' in href or 'verify' in href.lower() or 'lbry' in href.lower():
                print('Found verification target:', href)
                # Open in new tab
                import urllib.request
                req = urllib.request.Request(f'http://localhost:9223/json/new?{href}', method='PUT')
                resp = urllib.request.urlopen(req)
                print('Opened verification tab:', resp.read().decode())
                break

if __name__ == '__main__':
    asyncio.run(search_and_open_odysee())
