import asyncio
import websockets
import json

async def send_cmd(ws, method, params=None, msg_id=1):
    req = {'id': msg_id, 'method': method}
    if params:
        req['params'] = params
    await ws.send(json.dumps(req))
    while True:
        resp_raw = await asyncio.wait_for(ws.recv(), timeout=10.0)
        resp = json.loads(resp_raw)
        if resp.get('id') == msg_id:
            return resp

async def check():
    uri = 'ws://localhost:9223/devtools/page/060955F628A8EDF2463EFA1C799AB983'
    async with websockets.connect(uri) as ws:
        js = """(() => {
            return {
                url: window.location.href,
                title: document.title,
                text: document.body.innerText.slice(0, 1000)
            };
        })()"""
        res = await send_cmd(ws, 'Runtime.evaluate', {'expression': js, 'returnByValue': True}, msg_id=1)
        print(json.dumps(res['result']['result']['value'], indent=2))

if __name__ == '__main__':
    asyncio.run(check())
