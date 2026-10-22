import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def test_verify():
    tab_id = '2591DDE87B743DBFF72509D772E7D75B'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Check current HTML / modals
        expr = """
        (() => {
            const verifyBtn = Array.from(document.querySelectorAll('button, a')).find(b => b.innerText && b.innerText.trim() === 'Verify');
            if (verifyBtn) {
                verifyBtn.click();
                return 'Clicked verify: ' + verifyBtn.outerHTML;
            }
            return 'Verify button not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print(raw)
        
        await asyncio.sleep(2)
        
        # Check if an alert, modal, or notification popped up
        expr2 = """
        (() => {
            const modals = Array.from(document.querySelectorAll('.ant-modal, .ant-notification, .ant-message, [role="dialog"]')).map(m => m.innerText);
            return {
                url: window.location.href,
                modals: modals,
                bodySnippet: document.body.innerText.slice(0, 400)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        print(json.dumps(json.loads(raw2).get('result', {}).get('result', {}).get('value', {}), indent=2))

if __name__ == '__main__':
    asyncio.run(test_verify())
