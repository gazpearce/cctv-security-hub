import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def fix_doi_radio():
    tab_id = 'C8AC94E331D5E7707203F724DC068AD7'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        expr = """
        (() => {
            // Find "No, I need one" radio or button
            const labels = Array.from(document.querySelectorAll('label, .radio, button')).filter(e => e.innerText.includes('No, I need one') || e.innerText.includes('Get a DOI now'));
            let clicked = [];
            for (const l of labels) {
                l.click();
                const input = l.querySelector('input') || document.querySelector('input[type="radio"]');
                if (input) input.click();
                clicked.push(l.innerText.trim());
            }
            
            // Also check for "Get a DOI now" button
            const getDoiBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.includes('Get a DOI') || b.innerText.includes('reserve'));
            if (getDoiBtn) {
                getDoiBtn.click();
                clicked.push(getDoiBtn.innerText.trim());
            }
            
            return {
                clicked: clicked,
                radios: Array.from(document.querySelectorAll('input[type="radio"]')).map(r => ({checked: r.checked, value: r.value, id: r.id}))
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        raw = await ws.recv()
        val = json.loads(raw).get('result', {}).get('result', {}).get('value', {})
        print('DOI radio click:', json.dumps(val, indent=2))
        
        await asyncio.sleep(2)
        
        # Click Save draft again
        expr_save = """
        (() => {
            const saveBtn = Array.from(document.querySelectorAll('button')).find(b => b.innerText.trim() === 'Save draft');
            if (saveBtn) {
                saveBtn.click();
                return 'Clicked Save draft';
            }
            return 'No save draft';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': expr_save, 'returnByValue': True}}))
        raw2 = await ws.recv()
        print('Save draft response:', raw2)
        
        await asyncio.sleep(3)
        
        expr3 = """
        (() => {
            const errors = Array.from(document.querySelectorAll('.error.message, .ui.negative.message, .ui.red.label')).map(e => e.innerText.trim());
            return {
                errors: errors,
                bodySnippet: document.body.innerText.slice(0, 800)
            };
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': expr3, 'returnByValue': True}}))
        raw3 = await ws.recv()
        val3 = json.loads(raw3).get('result', {}).get('result', {}).get('value', {})
        print('State after fix:', json.dumps(val3, indent=2))

if __name__ == '__main__':
    asyncio.run(fix_doi_radio())
