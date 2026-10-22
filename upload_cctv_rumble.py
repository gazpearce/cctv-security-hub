import asyncio
import json
import websockets
import os
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

async def upload_cctv_rumble():
    tab_id = "B05DD5FD31627A501BCF11412B0DA3C8"
    video_path = r"C:\Users\Gary\.gemini\antigravity\scratch\Gary_Pearce_Hikvision_ColorVu_CCTV_UK_Masterclass_1080p.mp4"
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        return
        
    print(f"Connecting to Rumble upload tab {tab_id} for Video 3 (Hikvision ColorVu CCTV)...")
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{tab_id}", max_size=25*1024*1024) as ws:
        # Step 0: Navigate to upload page
        print("Navigating to https://rumble.com/upload.php...")
        await send_rpc(ws, 1, 'Page.navigate', {'url': 'https://rumble.com/upload.php'})
        await asyncio.sleep(5)
        
        # Step 1: Enable DOM & get document
        await send_rpc(ws, 2, 'DOM.enable')
        await send_rpc(ws, 3, 'DOM.getDocument')
        
        # Step 2: Get #Filedata node
        eval_res = await send_rpc(ws, 4, 'Runtime.evaluate', {'expression': "document.getElementById('Filedata')"})
        object_id = eval_res.get('result', {}).get('result', {}).get('objectId')
        req_res = await send_rpc(ws, 5, 'DOM.requestNode', {'objectId': object_id})
        file_node_id = req_res.get('result', {}).get('nodeId')
        print(f"File Node ID: {file_node_id}")
        
        # Step 3: Set file
        await send_rpc(ws, 6, 'DOM.setFileInputFiles', {'files': [video_path], 'nodeId': file_node_id})
        print("File attached: Gary_Pearce_Hikvision_ColorVu_CCTV_UK_Masterclass_1080p.mp4")
        
        await asyncio.sleep(4)
        
        # Step 4: Fill Metadata
        title = "Hikvision ColorVu vs Infrared CCTV UK: Night Vision, DORI Standards & 4K Police Evidence"
        desc = (
            "Official ADI Communications Technical Masterclass by Gary Pearce (25+ Years Hands-On Physical Security & Telecoms Engineer, Direct Mobile: 07860 244 274).\n\n"
            "Why 850nm infrared night vision fails Crown Prosecution Service (CPS) court admissibility standards, how Hikvision ColorVu G2 F1.0 super-apertures capture 24/7 colour in pitch darkness, BS EN 62676-4 DORI identification targets (250 px/m), and solid copper Cat6 PoE cabling.\n\n"
            "• Watch the Complete 4K Field Installation on YouTube: https://www.youtube.com/watch?v=50q89TsNN3w\n"
            "• Official YouTube Channel (@CCTV.services): https://www.youtube.com/@CCTV.services\n"
            "• Direct Engineer Field Enquiries: 07860 244 274 (Gary Pearce • ADI Communications)"
        )
        tags = "F1.0 super-apertures, 850nm IR flare spiderwebs, BS EN 62676-4 DORI 250 px/m, Solid copper Cat6 PoE, WD Purple NVR, Gary Pearce, ADI Communications, Bradford CCTV Specialist"
        yt_url = "https://www.youtube.com/watch?v=50q89TsNN3w"
        
        fill_expr = f"""
        (() => {{
            const t = document.getElementById('title');
            if (t) {{ t.value = {json.dumps(title)}; t.dispatchEvent(new Event('input', {{ bubbles: true }})); t.dispatchEvent(new Event('change', {{ bubbles: true }})); }}
            const d = document.getElementById('description');
            if (d) {{ d.value = {json.dumps(desc)}; d.dispatchEvent(new Event('input', {{ bubbles: true }})); d.dispatchEvent(new Event('change', {{ bubbles: true }})); }}
            const tg = document.getElementById('tags');
            if (tg) {{ tg.value = {json.dumps(tags)}; tg.dispatchEvent(new Event('input', {{ bubbles: true }})); tg.dispatchEvent(new Event('change', {{ bubbles: true }})); }}
            const yt = document.getElementById('youtubeUrl');
            if (yt) {{ yt.value = {json.dumps(yt_url)}; yt.dispatchEvent(new Event('input', {{ bubbles: true }})); yt.dispatchEvent(new Event('change', {{ bubbles: true }})); }}
            
            // Select Technology category (value 7)
            const input = document.querySelector('input[name="primary-category"]');
            const hidden = document.getElementById('category_primary');
            const opt = document.querySelector('.select-option[data-value="7"]');
            if (input) {{ input.focus(); input.dispatchEvent(new MouseEvent('click', {{ bubbles: true }})); }}
            if (opt) {{
                opt.dispatchEvent(new MouseEvent('mousedown', {{ bubbles: true }}));
                opt.dispatchEvent(new MouseEvent('mouseup', {{ bubbles: true }}));
                opt.dispatchEvent(new MouseEvent('click', {{ bubbles: true }}));
            }}
            if (hidden) {{ hidden.value = '7'; hidden.dispatchEvent(new Event('change', {{ bubbles: true }})); }}
            if (input) {{ input.value = 'Technology'; input.dispatchEvent(new Event('change', {{ bubbles: true }})); }}
            
            return 'Metadata and Category filled';
        }})()
        """
        fill_res = await send_rpc(ws, 7, 'Runtime.evaluate', {'expression': fill_expr, 'returnByValue': True})
        print("Fill status:", fill_res.get('result', {}).get('result', {}).get('value'))
        
        # Step 5: Wait for upload to complete (45.8 MB takes ~40-60s)
        print("Waiting for CCTV video upload to finish...")
        for i in range(45):
            await asyncio.sleep(2)
            check_expr = """
            (() => {
                const text = document.body.innerText;
                const m = text.match(/(\\d+%\\s*\\([^)]*\\)\\s*Uploading)/);
                const is100 = text.includes('100%');
                return {
                    progress: m ? m[0] : (is100 ? '100% Complete' : 'Processing/Ready'),
                    submitDisabled: document.getElementById('submitForm') ? document.getElementById('submitForm').disabled : null
                };
            })()
            """
            status = await send_rpc(ws, 20 + i, 'Runtime.evaluate', {'expression': check_expr, 'returnByValue': True})
            val = status.get('result', {}).get('result', {}).get('value', {})
            print(f"[{i*2}s] Upload:", json.dumps(val))
            if '100%' in str(val.get('progress')):
                print("Upload reached 100%!")
                break
                
        # Step 6: Click submitForm
        print("Submitting Step 1 form...")
        await send_rpc(ws, 70, 'Runtime.evaluate', {'expression': "document.getElementById('submitForm').click()", 'returnByValue': True})
        await asyncio.sleep(4)
        
        # Step 7: Agree to terms in Step 2 and submit
        print("Agreeing to licensing terms and submitting Step 2...")
        step2_expr = """
        (() => {
            const terms = document.getElementById('cterms');
            if (terms) { terms.checked = true; terms.dispatchEvent(new Event('change', { bubbles: true })); }
            const rights = document.getElementById('crights');
            if (rights) { rights.checked = true; rights.dispatchEvent(new Event('change', { bubbles: true })); }
            
            const submit2 = document.getElementById('submitForm2');
            if (submit2) {
                submit2.disabled = false;
                submit2.click();
                return 'Clicked submitForm2';
            }
            return 'submitForm2 not found';
        })()
        """
        sub2_res = await send_rpc(ws, 71, 'Runtime.evaluate', {'expression': step2_expr, 'returnByValue': True})
        print("Step 2 result:", sub2_res.get('result', {}).get('result', {}).get('value'))
        
        await asyncio.sleep(8)
        
        # Step 8: Get published URL
        final_expr = """
        (() => {
            const direct = document.getElementById('direct');
            const embed = document.getElementById('embed');
            return {
                url: window.location.href,
                directShareUrl: direct ? direct.value : null,
                embedCode: embed ? embed.value : null,
                snippet: document.body.innerText.slice(0, 300)
            };
        })()
        """
        final_res = await send_rpc(ws, 72, 'Runtime.evaluate', {'expression': final_expr, 'returnByValue': True})
        print("CCTV ColorVu Published Video:\n", json.dumps(final_res.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(upload_cctv_rumble())
