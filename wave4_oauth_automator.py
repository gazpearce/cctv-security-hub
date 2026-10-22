import asyncio
import websockets
import urllib.request
import json
import time

async def cdp_call(ws, method, params=None):
    msg_id = int(time.time() * 1000) % 1000000
    await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == msg_id:
            return resp.get('result', {})

async def process_platform(tab, name, click_expr, wait_secs=5):
    print(f"\n=================== Processing {name} ===================")
    print("Initial URL:", tab['url'])
    try:
        async with websockets.connect(tab['webSocketDebuggerUrl']) as ws:
            res = await cdp_call(ws, 'Runtime.evaluate', {'expression': click_expr, 'returnByValue': True})
            print("Action result:", res.get('result', {}).get('value'))
            await asyncio.sleep(wait_secs)
            
            # Check final URL and title
            url_res = await cdp_call(ws, 'Runtime.evaluate', {'expression': 'window.location.href', 'returnByValue': True})
            title_res = await cdp_call(ws, 'Runtime.evaluate', {'expression': 'document.title', 'returnByValue': True})
            print(f"Final {name} URL: {url_res.get('result', {}).get('value')} | Title: {title_res.get('result', {}).get('value')}")
            return url_res.get('result', {}).get('value')
    except Exception as e:
        print(f"Error on {name}: {e}")
        return None

async def run_wave4():
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())
    
    # 1. Turso
    turso_tab = next((t for t in tabs if 'turso' in t.get('url', '').lower()), None)
    if turso_tab:
        turso_expr = """(() => {
            const ghBtn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').toLowerCase().includes('github'));
            if (ghBtn) {
                ghBtn.click();
                return 'Clicked GitHub on Turso';
            }
            return 'GitHub button not found on Turso';
        })()"""
        await process_platform(turso_tab, "Turso", turso_expr, 6)

    # Refresh tabs
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())

    # 2. Upstash
    upstash_tab = next((t for t in tabs if 'upstash' in t.get('url', '').lower()), None)
    if upstash_tab:
        upstash_expr = """(() => {
            const ghBtn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').toLowerCase().includes('github'));
            if (ghBtn) {
                ghBtn.click();
                return 'Clicked GitHub on Upstash';
            }
            return 'GitHub button not found on Upstash';
        })()"""
        await process_platform(upstash_tab, "Upstash", upstash_expr, 6)

    # Refresh tabs
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())

    # 3. CodeSandbox
    cs_tab = next((t for t in tabs if 'codesandbox' in t.get('url', '').lower()), None)
    if cs_tab:
        cs_expr = """(() => {
            const ghBtn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').toLowerCase().includes('github'));
            if (ghBtn) {
                ghBtn.click();
                return 'Clicked GitHub on CodeSandbox';
            }
            return 'GitHub button not found on CodeSandbox';
        })()"""
        await process_platform(cs_tab, "CodeSandbox", cs_expr, 6)

    # Refresh tabs
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())

    # 4. StackBlitz
    sb_tab = next((t for t in tabs if 'stackblitz' in t.get('url', '').lower()), None)
    if sb_tab:
        sb_expr = """(() => {
            const signIn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').toLowerCase().includes('sign in'));
            if (signIn) {
                signIn.click();
                return 'Clicked Sign In on StackBlitz';
            }
            return 'Sign In button not found on StackBlitz';
        })()"""
        await process_platform(sb_tab, "StackBlitz", sb_expr, 6)

    # Refresh tabs
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())

    # 5. Northflank
    nf_tab = next((t for t in tabs if 'northflank' in t.get('url', '').lower()), None)
    if nf_tab:
        nf_expr = """(() => {
            const ghBtn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').toLowerCase().includes('github'));
            if (ghBtn) {
                ghBtn.click();
                return 'Clicked GitHub on Northflank';
            }
            return 'GitHub button not found on Northflank';
        })()"""
        await process_platform(nf_tab, "Northflank", nf_expr, 6)

    # Refresh tabs
    tabs = json.loads(urllib.request.urlopen('http://127.0.0.1:9223/json').read())

    # 6. Fleek
    fleek_tab = next((t for t in tabs if 'fleek' in t.get('url', '').lower()), None)
    if fleek_tab:
        fleek_expr = """(() => {
            const ghBtn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').toLowerCase().includes('github') || (b.innerText || '').toLowerCase().includes('sign in'));
            if (ghBtn) {
                ghBtn.click();
                return 'Clicked on Fleek';
            }
            return 'Button not found on Fleek';
        })()"""
        await process_platform(fleek_tab, "Fleek", fleek_expr, 6)

if __name__ == '__main__':
    asyncio.run(run_wave4())
