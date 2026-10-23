import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def save_zenodo_draft():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        # Click "Save draft"
        expr = """
        (() => {
            const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save draft');
            if (saveBtn) {
                saveBtn.click();
                return 'Clicked Save draft';
            }
            return 'Save draft button not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        print('Save draft:', raw)
        
        await asyncio.sleep(4)
        
        # Check current URL, error messages or success banner
        expr2 = """
        (() => {
            const errors = Array.from(document.querySelectorAll('.error.message, .ui.negative.message, .ui.red.label')).map(e => e.innerText.trim());
            const success = Array.from(document.querySelectorAll('.success.message, .ui.positive.message')).map(e => e.innerText.trim());
            const doi = Array.from(document.querySelectorAll('*')).find(e => e.innerText && e.innerText.includes('10.5281/zenodo.'));
            return {
                url: window.location.href,
                errors: errors,
                success: success,
                doiText: doi ? doi.innerText.slice(0, 100) : null,
                bodySnippet: document.body.innerText.slice(0, 1000)
            };
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr2, 'returnByValue': True}}))
        raw2 = await ws.recv()
        val = json.loads(raw2).get('result', {}).get('result', {}).get('value', {})
        print('State after save draft:', json.dumps(val, indent=2))

if __name__ == '__main__':
    asyncio.run(save_zenodo_draft())
