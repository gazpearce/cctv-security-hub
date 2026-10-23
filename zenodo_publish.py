import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def publish_zenodo():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Click Publish button
        expr = """
        (() => {
            const pubBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Publish');
            if (pubBtn) {
                pubBtn.click();
                return 'Clicked Publish button';
            }
            return 'Publish button not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print('Publish click:', raw)
        
        await asyncio.sleep(2)
        
        # Check confirmation modal and click its Publish/Confirm button
        expr_modal = """
        (() => {
            const modal = document.querySelector('.modal, .ui.modal, div[role="dialog"]');
            if (!modal) return 'No confirmation modal found';
            
            // Find confirm publish button in modal
            const btns = Array.from(modal.querySelectorAll('button'));
            const confirmBtn = btns.find(b => b.innerText.trim() === 'Publish' || b.innerText.trim().includes('Confirm') || b.className.includes('positive') || b.className.includes('primary'));
            if (confirmBtn) {
                confirmBtn.click();
                return 'Clicked modal confirm: ' + confirmBtn.innerText;
            }
            return 'Modal found but no confirm button: ' + btns.map(b => b.innerText).join(', ');
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr_modal, 'returnByValue': True}}))
        raw2 = await ws.recv()
        print('Modal confirm:', raw2)
        
        await asyncio.sleep(5)
        
        expr_final = """
        (() => {
            return {
                url: window.location.href,
                title: document.title,
                bodySnippet: document.body.innerText.slice(0, 1000)
            };
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': expr_final, 'returnByValue': True}}))
        raw3 = await ws.recv()
        val3 = json.loads(raw3).get('result', {}).get('result', {}).get('value', {})
        print('Final State after publish:', json.dumps(val3, indent=2))

if __name__ == '__main__':
    asyncio.run(publish_zenodo())
