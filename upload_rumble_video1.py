import asyncio
import json
import websockets
import os

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

async def upload_rumble():
    tab_id = "B05DD5FD31627A501BCF11412B0DA3C8"
    video_path = r"C:\Users\Gary\.gemini\antigravity\scratch\Gary_Pearce_Starlink_Gen3_Mini_UK_Masterclass_1080p.mp4"
    
    if not os.path.exists(video_path):
        print(f"Error: Video file not found: {video_path}")
        return
        
    print(f"Connecting to Rumble upload tab {tab_id}...")
    async with websockets.connect(f"ws://127.0.0.1:9223/devtools/page/{tab_id}", max_size=25*1024*1024) as ws:
        # Step 0: Enable DOM
        await send_rpc(ws, 1, 'DOM.enable')
        await send_rpc(ws, 2, 'DOM.getDocument')
        
        # Step 1: Get #Filedata objectId via Runtime.evaluate
        eval_res = await send_rpc(ws, 3, 'Runtime.evaluate', {'expression': "document.getElementById('Filedata')"})
        object_id = eval_res.get('result', {}).get('result', {}).get('objectId')
        print(f"Object ID for #Filedata: {object_id}")
        
        # Step 2: Request nodeId
        req_res = await send_rpc(ws, 4, 'DOM.requestNode', {'objectId': object_id})
        file_node_id = req_res.get('result', {}).get('nodeId')
        print(f"File Node ID: {file_node_id}")
        
        # Step 3: Set file input
        set_res = await send_rpc(ws, 5, 'DOM.setFileInputFiles', {'files': [video_path], 'nodeId': file_node_id})
        print("Set file input result:", set_res)
        
        print("Waiting 5 seconds for video processing and UI update...")
        await asyncio.sleep(5)
        
        # Step 4: Fill Title, Description, Tags, YouTube URL
        title = "Starlink Gen 3 & Mini UK Installation: 90mph Gale Chimney Mounts, Bypass & Speed Test"
        desc = (
            "Official ADI Communications Technical Masterclass by Gary Pearce (25+ Years Hands-On Physical Security & Telecoms Engineer, Direct Mobile: 07860 244 274).\n\n"
            "SpaceX Starlink Gen 3 Standard dish and Starlink Mini installation engineering in the UK: 90mph Pennine gale-tested non-drill chimney lashing cradles, 110° northern orbital cone clearance, router bypass mode, and whole-home domestic Wi-Fi 7 mesh integration.\n\n"
            "• Watch the Complete 4K Field Installation on YouTube: https://www.youtube.com/watch?v=dOFIxVqMxCM\n"
            "• Official YouTube Channel (@CCTV.services): https://www.youtube.com/@CCTV.services\n"
            "• Direct Engineer Field Enquiries: 07860 244 274 (Gary Pearce • ADI Communications)"
        )
        tags = "Starlink Installation UK, SpaceX Starlink Gen 3, Starlink Mini, Non-Drill Chimney Mount, 90mph Gale Tested, Gary Pearce, ADI Communications, Wi-Fi 7 Mesh, Yorkshire Broadband"
        yt_url = "https://www.youtube.com/watch?v=dOFIxVqMxCM"
        
        fill_expr = f"""
        (() => {{
            const t = document.getElementById('title');
            if (t) {{
                t.value = {json.dumps(title)};
                t.dispatchEvent(new Event('input', {{ bubbles: true }}));
                t.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const d = document.getElementById('description');
            if (d) {{
                d.value = {json.dumps(desc)};
                d.dispatchEvent(new Event('input', {{ bubbles: true }}));
                d.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const tg = document.getElementById('tags');
            if (tg) {{
                tg.value = {json.dumps(tags)};
                tg.dispatchEvent(new Event('input', {{ bubbles: true }}));
                tg.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            const yt = document.getElementById('youtubeUrl');
            if (yt) {{
                yt.value = {json.dumps(yt_url)};
                yt.dispatchEvent(new Event('input', {{ bubbles: true }}));
                yt.dispatchEvent(new Event('change', {{ bubbles: true }}));
            }}
            return {{
                title: t ? t.value : null,
                descLen: d ? d.value.length : null,
                tags: tg ? tg.value : null,
                yt: yt ? yt.value : null
            }};
        }})()
        """
        fill_res = await send_rpc(ws, 6, 'Runtime.evaluate', {'expression': fill_expr, 'returnByValue': True})
        print("Metadata filled:", json.dumps(fill_res.get('result', {}).get('result', {}).get('value'), indent=2))
        
        # Check upload status or progress
        check_expr = """
        (() => {
            const progress = document.querySelector('.progress') || document.querySelector('.upload-progress') || document.querySelector('.bar') || document.querySelector('.progress-bar');
            const submitBtn = document.getElementById('submitForm');
            return {
                progressText: progress ? progress.innerText : null,
                submitDisabled: submitBtn ? submitBtn.disabled : null,
                submitValue: submitBtn ? submitBtn.value : null,
                fileVal: document.getElementById('Filedata') ? document.getElementById('Filedata').value : null
            };
        })()
        """
        status_res = await send_rpc(ws, 7, 'Runtime.evaluate', {'expression': check_expr, 'returnByValue': True})
        print("Upload state:", json.dumps(status_res.get('result', {}).get('result', {}).get('value'), indent=2))

if __name__ == '__main__':
    asyncio.run(upload_rumble())
