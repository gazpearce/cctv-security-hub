import asyncio
import websockets
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def check_tiktok():
    tab_id = '76CC99643C9BDB39C51016640626E071'
    try:
        async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}', max_size=10*1024*1024) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.location.href'}}))
            res = json.loads(await ws.recv())
            current_url = res.get('result', {}).get('result', {}).get('value')
            print('Current TikTok URL:', current_url)
            
            expr_check = 'Boolean(document.querySelector("header img, a[href*=\'upload\'], a[href*=\'@\']"))'
            await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr_check}}))
            res2 = json.loads(await ws.recv())
            is_logged_in = res2.get('result', {}).get('result', {}).get('value')
            print('Is Logged In:', is_logged_in)
    except Exception as e:
        print('Error:', e)

if __name__ == '__main__':
    asyncio.run(check_tiktok())
