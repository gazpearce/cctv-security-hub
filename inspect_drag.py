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

async def inspect_drag():
    uri = 'ws://localhost:9223/devtools/page/76CC99643C9BDB39C51016640626E071'
    async with websockets.connect(uri) as ws:
        js = """(() => {
            // find slider handle and track
            const handle = document.querySelector('[class*="secsdk-captcha-drag-icon"], [class*="drag-icon"], div[class*="secsdk_captcha_drag"]');
            // find all elements in the modal
            const modal = document.querySelector('.secsdk_captcha_modal, [class*="captcha"]');
            const allElements = Array.from(modal.querySelectorAll('*')).map(el => ({
                tag: el.tagName,
                className: el.className,
                rect: el.getBoundingClientRect()
            })).filter(el => el.rect.width > 0 && el.rect.height > 0);
            return {
                handleRect: handle ? handle.getBoundingClientRect() : null,
                elements: allElements.slice(0, 30)
            };
        })()"""
        res = await send_cmd(ws, 'Runtime.evaluate', {'expression': js, 'returnByValue': True}, msg_id=1)
        print(json.dumps(res['result']['result']['value'], indent=2))

if __name__ == '__main__':
    asyncio.run(inspect_drag())
