import urllib.request
import json
import asyncio
import websockets

async def check_captcha():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())
    circle_tab = next(t for t in tabs if 'circleci' in t.get('url', '').lower())
    ws_url = circle_tab['webSocketDebuggerUrl']
    
    async with websockets.connect(ws_url) as ws:
        msg_id = 1
        async def call(method, params=None):
            nonlocal msg_id
            msg_id += 1
            await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
            while True:
                resp = json.loads(await ws.recv())
                if resp.get('id') == msg_id:
                    return resp.get('result', {})

        # List iframes
        frames = await call('Page.getFrameTree')
        print("=== FRAMES ===")
        print(json.dumps(frames, indent=2)[:1000])

if __name__ == '__main__':
    asyncio.run(check_captcha())
