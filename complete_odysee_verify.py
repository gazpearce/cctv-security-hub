import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def complete_odysee_verification():
    tab_id = '1A6B5AF6ECF7A9F5D083FC8879A4D8FF'
    verify_url = 'https://odysee.com/$/verify?auth_token=2X34caUtcKb18qdCDAjW1XRNrhnhwrVo&email=aiagent1510%40gmail.com&needs_recaptcha=true&verification_token=GTNKJ4wectBLVf4hfPcZpAo442K2wrpT'
    
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': verify_url}}))
        raw = await ws.recv()
        print('Navigated to verify link:', raw)
        
        await asyncio.sleep(5)
        
        expr = """
        (() => {
            return {
                url: window.location.href,
                title: document.title,
                bodyText: document.body.innerText.slice(0, 1000),
                buttons: Array.from(document.querySelectorAll('button')).map(b => b.innerText.trim()).filter(Boolean)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print('Verification Page State:', json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(complete_odysee_verification())
