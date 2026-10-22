import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def prepare_dailymotion():
    tab_id = '2591DDE87B743DBFF72509D772E7D75B'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            let res = [];
            // Accept cookies if present
            const acceptBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Accept');
            if (acceptBtn) {
                acceptBtn.click();
                res.push('Accepted cookies');
            }
            
            // Check verify email button
            const verifyBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Verify');
            if (verifyBtn) {
                verifyBtn.click();
                res.push('Clicked Verify email');
            }
            return res.join(', ') || 'No actions taken';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print(raw)

if __name__ == '__main__':
    asyncio.run(prepare_dailymotion())
