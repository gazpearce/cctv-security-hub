import asyncio
import json
import websockets
import sys

sys.stdout.reconfigure(encoding='utf-8')

DECKS = [
    {
        'pdf': r'C:\Users\Gary\github-cctv-seo\stack_assets\documents\Ajax_Smart_Alarms_Grade2_Compliance_Yorkshire_Manual.pdf',
        'title': 'Ajax Smart Alarms UK Grade 2 Compliance & 868MHz Jeweller Anti-Jamming Manual',
        'desc': 'Comprehensive field engineering manual for Ajax Smart Alarms in the UK: Grade 2 EN 50131 certification, 868MHz Jeweller multi-channel hopping vs 433MHz jammers, MotionCam outdoor verification, and Dual-SIM 4G failover.\\n\\nAuthored by Gary Pearce, ADI Communications (25+ yrs experience, 07860 244 274).\\n\\nDemonstration Video: https://www.youtube.com/@CCTV.services\\nSecurity Hub: https://tvandhomesecurity.blogspot.com/',
        'cat': 'Technology'
    },
    {
        'pdf': r'C:\Users\Gary\github-cctv-seo\stack_assets\documents\UK_Commercial_Intruder_Alarms_Grade2_and_Grade3_Specification.pdf',
        'title': 'UK Commercial Intruder Alarms Grade 2 & Grade 3 Engineering Specification',
        'desc': 'Technical trade specification for UK commercial and high-value residential intruder alarm systems: PD 6662:2017 and BS EN 50131 standards, dual-path signalling (DP2/DP3), and Grade 3 perimeter seismic detection.\\n\\nAuthored by Gary Pearce, ADI Communications (25+ yrs experience, 07860 244 274).\\n\\nWatch Video Overview: https://www.youtube.com/@CCTV.services\\nEngineering Hub: https://tvandhomesecurity.blogspot.com/',
        'cat': 'Technology'
    },
    {
        'pdf': r'C:\Users\Gary\github-cctv-seo\stack_assets\documents\Ethernet_Upstairs_Without_Running_Cables_Field_Guide.pdf',
        'title': 'How to Get Ethernet Upstairs Without Running Visible Cables: UK Trade Guide',
        'desc': 'Practical trade comparison of Powerline AV2 vs MoCA 2.5 coax adapters vs external solid copper Cat6 cavity wall drops with drip loops for multi-storey British brick homes.\\n\\nAuthored by Gary Pearce, ADI Communications (25+ yrs experience, 07860 244 274).\\n\\nWatch Demonstration: https://www.youtube.com/@CCTV.services\\nTechnical Buffer: https://tvandhomesecurity.blogspot.com/',
        'cat': 'How-to & DIY'
    }
]

async def upload_batch():
    tab_id = 'C48DFADC6D68706DAF5E12B0F783F8AE'
    async with websockets.connect(f'ws://127.0.0.1:9223/devtools/page/{tab_id}') as ws:
        for idx, deck in enumerate(DECKS, 1):
            print(f"--- Uploading Deck {idx}/{len(DECKS)}: {deck['title']} ---")
            
            # 1. Navigate to /new
            await ws.send(json.dumps({'id': 1, 'method': 'Page.navigate', 'params': {'url': 'https://speakerdeck.com/new'}}))
            await ws.recv()
            await asyncio.sleep(4)
            
            # 2. Get objectId
            await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': "document.querySelector('input#upload-field')"}}))
            raw = await ws.recv()
            obj_id = json.loads(raw).get('result', {}).get('result', {}).get('objectId')
            
            # 3. Attach PDF
            await ws.send(json.dumps({'id': 3, 'method': 'DOM.setFileInputFiles', 'params': {'files': [deck['pdf']], 'objectId': obj_id}}))
            await ws.recv()
            await asyncio.sleep(4)
            
            # 4. Fill fields
            fill_code = f"""
            (() => {{
                const title = document.querySelector('input#talk_name') || document.querySelector('input[name="talk[name]"]');
                if (title) {{
                    title.value = {json.dumps(deck['title'])};
                    title.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    title.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                
                const desc = document.querySelector('textarea#talk_description') || document.querySelector('textarea[name="talk[description]"]');
                if (desc) {{
                    desc.value = {json.dumps(deck['desc'])};
                    desc.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    desc.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                
                const cat = document.querySelector('select#talk_category_id');
                if (cat) {{
                    const opt = Array.from(cat.options).find(o => o.text.includes({json.dumps(deck['cat'])}));
                    if (opt) {{
                        cat.value = opt.value;
                        cat.dispatchEvent(new Event('change', {{ bubbles: true }}));
                    }}
                }}
                
                const videoUrl = document.querySelector('input#talk_video_url');
                if (videoUrl) {{
                    videoUrl.value = 'https://www.youtube.com/@CCTV.services';
                    videoUrl.dispatchEvent(new Event('input', {{ bubbles: true }}));
                    videoUrl.dispatchEvent(new Event('change', {{ bubbles: true }}));
                }}
                return true;
            }})()
            """
            await ws.send(json.dumps({'id': 4, 'method': 'Runtime.evaluate', 'params': {'expression': fill_code, 'returnByValue': True}}))
            await ws.recv()
            await asyncio.sleep(2)
            
            # 5. Click Save
            save_code = """
            (() => {
                const btn = Array.from(document.querySelectorAll('button, input[type="submit"]')).find(b => {
                    const t = (b.innerText || b.value || '').trim();
                    return t === 'Save this deck' || t === 'Save';
                });
                if (btn) {
                    btn.click();
                    return 'Clicked';
                }
                return 'Not found';
            })()
            """
            await ws.send(json.dumps({'id': 5, 'method': 'Runtime.evaluate', 'params': {'expression': save_code, 'returnByValue': True}}))
            await ws.recv()
            await asyncio.sleep(6)
            
            # 6. Check resulting URL
            await ws.send(json.dumps({'id': 6, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.location.href', 'returnByValue': True}}))
            raw_url = await ws.recv()
            live_url = json.loads(raw_url).get('result', {}).get('result', {}).get('value')
            print(f"Published Deck {idx}: {live_url}")
            await asyncio.sleep(3)

if __name__ == '__main__':
    asyncio.run(upload_batch())
