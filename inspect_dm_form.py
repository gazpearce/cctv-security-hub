import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def inspect_dailymotion_dom():
    tab_id = '2591DDE87B743DBFF72509D772E7D75B'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            const form = document.querySelector('form');
            const iframes = Array.from(document.querySelectorAll('iframe')).map(f => f.src);
            const btn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Continue');
            return {
                hasForm: !!form,
                formAction: form ? form.action : null,
                formHTML: form ? form.outerHTML.slice(0, 1000) : null,
                btnDisabled: btn ? btn.disabled : null,
                btnClass: btn ? btn.className : null,
                iframes: iframes
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print(json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(inspect_dailymotion_dom())
