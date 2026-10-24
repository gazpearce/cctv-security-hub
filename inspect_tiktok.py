import asyncio
import websockets
import json

async def check():
    uri = 'ws://localhost:9223/devtools/page/76CC99643C9BDB39C51016640626E071'
    async with websockets.connect(uri) as ws:
        js = """(() => {
            const bodyText = document.body.innerText;
            const inputs = Array.from(document.querySelectorAll('input')).map(i => ({
                type: i.type,
                placeholder: i.placeholder,
                value: i.value,
                name: i.name
            }));
            const buttons = Array.from(document.querySelectorAll('button')).map(b => ({
                text: b.innerText.trim(),
                disabled: b.disabled
            }));
            const captcha = !!document.querySelector('.secsdk_captcha_modal, [class*="captcha"], iframe[src*="captcha"]');
            return {
                title: document.title,
                url: window.location.href,
                inputs: inputs,
                buttons: buttons,
                captcha: captcha,
                bodySnippet: bodyText.slice(0, 1000)
            };
        })()"""
        req = {
            'id': 1,
            'method': 'Runtime.evaluate',
            'params': {
                'expression': js,
                'returnByValue': True
            }
        }
        await ws.send(json.dumps(req))
        res = json.loads(await ws.recv())
        print(json.dumps(res['result']['result']['value'], indent=2))

if __name__ == '__main__':
    asyncio.run(check())
