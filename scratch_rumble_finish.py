import asyncio
import json
import websockets

async def finish_rumble():
    tab_id = "B05DD5FD31627A501BCF11412B0DA3C8"
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{tab_id}", max_size=25*1024*1024) as ws:
        # Step 1: Select Technology category and pick thumbnail
        expr = """
        (() => {
            // Select Technology
            const opt = document.querySelector('.select-option[data-value="7"]');
            if (opt) opt.click();
            
            // Choose radio thumbnail if any
            const thumbRadios = document.querySelectorAll('input[type="radio"][name="thumb"]');
            if (thumbRadios.length > 0) {
                thumbRadios[0].checked = true;
                thumbRadios[0].dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            // Make sure visibility is public
            const pub = document.getElementById('visibility_public');
            if (pub) pub.checked = true;
            
            const submitBtn = document.getElementById('submitForm');
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.click();
                return 'Clicked submitForm';
            }
            return 'submitForm not found';
        })()
        """
        await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
        res = json.loads(await ws.recv())
        print("Submit step 1:", res.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(4)
        
        # Step 2: In step 2 licensing form, agree to terms and submit
        step2_expr = """
        (() => {
            const terms = document.getElementById('cterms');
            if (terms) terms.checked = true;
            const rights = document.getElementById('crights');
            if (rights) rights.checked = true;
            
            // Choose Rumble Only / Personal licensing
            const radios = Array.from(document.querySelectorAll('input[type="radio"]'));
            const rumbleOnly = radios.find(r => r.value === 'rumble' || (r.labels && Array.from(r.labels).some(l => l.innerText.includes('Rumble Only') || l.innerText.includes('Personal'))));
            if (rumbleOnly) {
                rumbleOnly.checked = true;
                rumbleOnly.dispatchEvent(new Event('change', { bubbles: true }));
            }
            
            const submit2 = document.getElementById('submitForm2');
            if (submit2) {
                submit2.disabled = false;
                submit2.click();
                return 'Submitted submitForm2';
            }
            return 'submitForm2 not found';
        })()
        """
        await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': step2_expr, 'returnByValue': True}}))
        res2 = json.loads(await ws.recv())
        print("Submit step 2:", res2.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(5)
        
        await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': '({url: window.location.href, title: document.title, text: document.body.innerText.slice(0, 600)})', 'returnByValue': True}}))
        res3 = json.loads(await ws.recv())
        print("Final Status:", json.dumps(res3.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(finish_rumble())
