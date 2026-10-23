import asyncio
import json
import websockets
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

async def verify_odysee():
    tab_id = '846D30CA5670110BE1B220763CEEA59A'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Search for odysee in Gmail
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://mail.google.com/mail/u/0/#search/from%3Aodysee'}}))
        await ws.recv()
        await asyncio.sleep(4)
        
        # Click the first search result row
        expr = """
        (() => {
            const row = document.querySelector('tr[role="row"]');
            if (row) {
                row.click();
                return 'Clicked row';
            }
            return 'Row not found';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print('Click row:', raw)
        
        await asyncio.sleep(4)
        
        # Extract link
        expr2 = """
        (() => {
            const links = Array.from(document.querySelectorAll('div[role="main"] a')).map(a => a.href);
            const verifyLink = links.find(h => h.includes('odysee.com') || h.includes('verify'));
            return {
                allLinks: links,
                verifyLink: verifyLink
            };
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print('Extracted:', json.dumps(val, indent=2))
        
        verify_url = val.get('verifyLink')
        if verify_url:
            print('Navigating to verify URL:', verify_url)
            # Create new tab to open verify URL
            # or navigate in this tab or another tab
            import urllib.request
            req = urllib.request.Request(f'http://localhost:9223/json/new?{verify_url}', method='PUT')
            resp = urllib.request.urlopen(req)
            new_tab = json.loads(resp.read().decode())
            print('Created new tab for verification:', new_tab.get('id'), new_tab.get('url'))

if __name__ == '__main__':
    asyncio.run(verify_odysee())
