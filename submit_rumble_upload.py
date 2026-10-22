import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

async def send_rpc(ws, msg_id, method, params=None):
    payload = {'id': msg_id, 'method': method}
    if params:
        payload['params'] = params
    await ws.send(json.dumps(payload))
    while True:
        raw = await ws.recv()
        data = json.loads(raw)
        if data.get('id') == msg_id:
            return data

async def submit_upload():
    tab_id = "B05DD5FD31627A501BCF11412B0DA3C8"
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{tab_id}", max_size=25*1024*1024) as ws:
        # Step 1: Click #submitForm
        print("Clicking #submitForm on Rumble...")
        expr_click = """
        (() => {
            const btn = document.getElementById('submitForm');
            if (btn) {
                btn.click();
                return 'Clicked #submitForm';
            }
            return '#submitForm not found';
        })()
        """
        res = await send_rpc(ws, 1, 'Runtime.evaluate', {'expression': expr_click, 'returnByValue': True})
        print("Click result:", res.get('result', {}).get('result', {}).get('value'))
        
        # Step 2: Poll progress / wait for step 2 form
        for i in range(30):
            await asyncio.sleep(2)
            check_expr = """
            (() => {
                const step2 = document.getElementById('submitForm2');
                const progress = document.querySelector('.progress-bar') || document.querySelector('.bar') || document.querySelector('.progress');
                const visibleStep2 = step2 && step2.offsetParent !== null;
                const terms = document.getElementById('cterms');
                const rights = document.getElementById('crights');
                return {
                    iteration: """ + str(i) + """,
                    progress: progress ? progress.innerText || progress.style.width : null,
                    step2Visible: visibleStep2,
                    termsFound: !!terms,
                    rightsFound: !!rights,
                    currentUrl: window.location.href
                };
            })()
            """
            status = await send_rpc(ws, 10 + i, 'Runtime.evaluate', {'expression': check_expr, 'returnByValue': True})
            val = status.get('result', {}).get('result', {}).get('value', {})
            print(f"[{i*2}s] Status:", json.dumps(val))
            
            if val.get('step2Visible') or val.get('termsFound'):
                print("Step 2 licensing screen detected! Checking terms and submitting...")
                step2_expr = """
                (() => {
                    const terms = document.getElementById('cterms');
                    if (terms) terms.checked = true;
                    const rights = document.getElementById('crights');
                    if (rights) rights.checked = true;
                    
                    // Choose Rumble Player (non-exclusive / personal) if radio exists
                    const radios = Array.from(document.querySelectorAll('input[type="radio"]'));
                    const rumbleOnly = radios.find(r => r.value === 'rumble' || (r.labels && Array.from(r.labels).some(l => l.innerText.includes('Rumble Only') || l.innerText.includes('Personal'))));
                    if (rumbleOnly) rumbleOnly.checked = true;
                    
                    const submit2 = document.getElementById('submitForm2');
                    if (submit2) {
                        submit2.click();
                        return 'Submitted Step 2 successfully';
                    }
                    return 'Terms checked, submit2 not found';
                })()
                """
                sub2_res = await send_rpc(ws, 100, 'Runtime.evaluate', {'expression': step2_expr, 'returnByValue': True})
                print("Step 2 submission:", sub2_res.get('result', {}).get('result', {}).get('value'))
                await asyncio.sleep(5)
                
                # Check final video URL
                final_status = await send_rpc(ws, 101, 'Runtime.evaluate', {'expression': '({url: window.location.href, text: document.body.innerText.slice(0, 500)})', 'returnByValue': True})
                print("Final Rumble page:", json.dumps(final_status.get('result', {}).get('result', {}).get('value'), indent=2))
                break

if __name__ == '__main__':
    asyncio.run(submit_upload())
