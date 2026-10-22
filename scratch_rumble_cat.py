import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def select_category_and_submit():
    tab_id = "B05DD5FD31627A501BCF11412B0DA3C8"
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{tab_id}", max_size=25*1024*1024) as ws:
        # Step 1: Open dropdown and click option 7 (Technology)
        expr = """
        (() => {
            const input = document.querySelector('input[name="primary-category"]');
            const hidden = document.getElementById('category_primary');
            const opt = document.querySelector('.select-option[data-value="7"]');
            
            if (input) {
                input.focus();
                input.dispatchEvent(new MouseEvent('click', { bubbles: true }));
            }
            
            if (opt) {
                opt.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                opt.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));
                opt.dispatchEvent(new MouseEvent('click', { bubbles: true }));
            }
            
            // Also directly set hidden and input if Rumble script supports it
            if (hidden) {
                hidden.value = '7';
                hidden.dispatchEvent(new Event('change', { bubbles: true }));
                hidden.dispatchEvent(new Event('input', { bubbles: true }));
            }
            if (input) {
                input.value = 'Technology';
                input.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            return {
                hiddenVal: hidden ? hidden.value : null,
                inputVal: input ? input.value : null,
                optFound: !!opt
            };
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        print("Selection result:", json.dumps(res.get('result', {}).get('result', {}).get('value'), indent=2))
        
        await asyncio.sleep(2)
        
        # Step 2: Click submitForm
        print("Clicking submitForm...")
        submit_expr = """
        (() => {
            const btn = document.getElementById('submitForm');
            if (btn) {
                btn.click();
                return 'Clicked submitForm';
            }
            return 'submitForm not found';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': submit_expr, 'returnByValue': True}}))
        res2 = json.loads(await ws.recv())
        print("Submit result:", res2.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(4)
        
        # Step 3: Check if step 2 licensing appeared
        check_expr = """
        (() => {
            const form2 = document.getElementById('submitForm2');
            const terms = document.getElementById('cterms');
            const rights = document.getElementById('crights');
            return {
                url: window.location.href,
                step2FormFound: !!form2,
                step2Visible: form2 ? form2.offsetParent !== null : false,
                bodySnippet: document.body.innerText.slice(0, 400)
            };
        })()
        """
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': check_expr, 'returnByValue': True}}))
        res3 = json.loads(await ws.recv())
        print("After submitForm:", json.dumps(res3.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(select_category_and_submit())
