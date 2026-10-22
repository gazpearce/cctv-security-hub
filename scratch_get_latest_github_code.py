import asyncio
import json
import websockets
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def get_latest_github_code():
    gmail_tab = "846D30CA5670110BE1B220763CEEA59A"
    ws_url = f"ws://127.0.0.1:9223/devtools/page/{gmail_tab}"
    async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
        # Search for github sudo
        expr = """
        (() => {
            window.location.hash = '#search/from%3Agithub+sudo';
            return 'Searching';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        await ws.recv()
        await asyncio.sleep(4)
        
        # Click the first row
        click_expr = """
        (() => {
            const rows = document.querySelectorAll('tr[role="row"]');
            if (rows.length > 0) {
                rows[0].click();
                return 'Clicked first row';
            }
            return 'No rows';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': click_expr, 'returnByValue': True}}))
        res_click = json.loads(await ws.recv())
        print("Click:", res_click.get('result', {}).get('result', {}).get('value'))
        await asyncio.sleep(3)
        
        # Extract body text
        read_expr = """
        (() => {
            return document.body.innerText;
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': read_expr, 'returnByValue': True}}))
        res_read = json.loads(await ws.recv())
        body = res_read.get('result', {}).get('result', {}).get('value', '')
        
        # Search for code
        # Pattern: Here is your GitHub sudo authentication code: \d{8}
        m = re.search(r'sudo authentication code:\s*(\d{6,8})', body)
        if m:
            print(f"FOUND_CODE: {m.group(1)}")
            return m.group(1)
        else:
            all_digits = re.findall(r'\b\d{8}\b', body)
            print("Possible 8-digit codes:", all_digits[:5])
            if all_digits:
                print(f"FOUND_CODE: {all_digits[0]}")
                return all_digits[0]
            print("Snippet:", body[:1000])
            return None

if __name__ == '__main__':
    asyncio.run(get_latest_github_code())
