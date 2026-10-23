import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_odysee_page():
    tab_id = '1A6B5AF6ECF7A9F5D083FC8879A4D8FF'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            // Dismiss onetrust if present
            const acceptBtn = document.getElementById('onetrust-accept-btn-handler');
            let clickedOnetrust = false;
            if (acceptBtn) {
                acceptBtn.click();
                clickedOnetrust = true;
            }
            
            // Check for main content
            const main = document.querySelector('main') || document.querySelector('#app');
            const iframes = Array.from(document.querySelectorAll('iframe')).map(i => i.src);
            return {
                clickedOnetrust: clickedOnetrust,
                mainText: main ? main.innerText.slice(0, 1000) : 'No main',
                iframes: iframes,
                allButtons: Array.from(document.querySelectorAll('button')).map(b => ({id: b.id, text: b.innerText.trim(), class: b.className}))
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(inspect_odysee_page())
