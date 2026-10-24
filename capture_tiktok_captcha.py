import asyncio
import websockets
import json
import base64

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

async def capture_captcha():
    uri = 'ws://localhost:9223/devtools/page/76CC99643C9BDB39C51016640626E071'
    async with websockets.connect(uri) as ws:
        await send_cmd(ws, 'Page.enable', msg_id=1)
        
        # Take screenshot
        res = await send_cmd(ws, 'Page.captureScreenshot', {'format': 'png'}, msg_id=2)
        img_data = base64.b64decode(res['result']['data'])
        with open('tiktok_captcha.png', 'wb') as f:
            f.write(img_data)
        print("Successfully saved screenshot to tiktok_captcha.png")

        # Inspect captcha DOM elements
        js = """(() => {
            const modal = document.querySelector('.secsdk_captcha_modal, [class*="captcha"]');
            const slider = document.querySelector('[class*="secsdk-captcha-drag-icon"], [class*="drag"], .secsdk_captcha_drag');
            const images = Array.from(document.querySelectorAll('img')).map(i => ({
                src: i.src.slice(0, 100),
                width: i.width,
                height: i.height,
                alt: i.alt,
                className: i.className
            }));
            const text = document.querySelector('.secsdk_captcha_modal, [class*="captcha"]')?.innerText;
            return {
                modalFound: !!modal,
                sliderFound: !!slider,
                sliderRect: slider ? slider.getBoundingClientRect() : null,
                modalText: text,
                images: images
            };
        })()"""
        res2 = await send_cmd(ws, 'Runtime.evaluate', {'expression': js, 'returnByValue': True}, msg_id=3)
        print("Captcha details:")
        print(json.dumps(res2['result']['result']['value'], indent=2))

if __name__ == '__main__':
    asyncio.run(capture_captcha())
