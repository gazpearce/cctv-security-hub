import asyncio
import json
import websockets
import sys

async def handle_github_oauth(target_id):
    ws_url = f"ws://127.0.0.1:9223/devtools/page/{target_id}"
    print(f"Connecting to {ws_url}...")
    try:
        async with websockets.connect(ws_url, max_size=25*1024*1024) as ws:
            # Check page title and button
            expr = """
            (() => {
                const btn = document.querySelector('button#js-oauth-authorize-btn') || 
                            document.querySelector('button[name="authorize"]') ||
                            document.querySelector('button[type="submit"].js-oauth-authorize-btn') ||
                            document.querySelector('button.btn-primary');
                return {
                    title: document.title,
                    url: window.location.href,
                    buttonText: btn ? btn.innerText.trim() : null,
                    buttonFound: !!btn
                };
            })()
            """
            await ws.send(json.dumps({'id': 1, 'method': 'Runtime.evaluate', 'params': {'expression': expr, 'returnByValue': True}}))
            res = json.loads(await ws.recv())
            val = res.get('result', {}).get('result', {}).get('value', {})
            print("Status:", json.dumps(val, indent=2))
            
            if val.get('buttonFound') and 'Authorize' in (val.get('buttonText') or ''):
                print(f"Clicking button: {val.get('buttonText')}...")
                click_expr = """
                (() => {
                    const btn = document.querySelector('button#js-oauth-authorize-btn') || 
                                document.querySelector('button[name="authorize"]') ||
                                document.querySelector('button[type="submit"].js-oauth-authorize-btn') ||
                                document.querySelector('button.btn-primary');
                    if (btn) {
                        btn.click();
                        return 'Clicked successfully';
                    }
                    return 'Not clicked';
                })()
                """
                await ws.send(json.dumps({'id': 2, 'method': 'Runtime.evaluate', 'params': {'expression': click_expr, 'returnByValue': True}}))
                res2 = json.loads(await ws.recv())
                print("Click result:", res2.get('result', {}).get('result', {}).get('value'))
                await asyncio.sleep(4)
                
                # Check new url
                await ws.send(json.dumps({'id': 3, 'method': 'Runtime.evaluate', 'params': {'expression': 'window.location.href', 'returnByValue': True}}))
                res3 = json.loads(await ws.recv())
                print("New URL:", res3.get('result', {}).get('result', {}).get('value'))
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else '77C5B12D0511BE742784797468F7EE9D'
    asyncio.run(handle_github_oauth(target))
