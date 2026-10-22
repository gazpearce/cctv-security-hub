import urllib.request
import json
import asyncio
import websockets
import time

CHROME_DEBUG_PORT = 9223

def open_new_tab(url):
    req = urllib.request.Request(f"http://127.0.0.1:{CHROME_DEBUG_PORT}/json/new?{url}", method="PUT")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

def get_tabs():
    req = urllib.request.Request(f"http://127.0.0.1:{CHROME_DEBUG_PORT}/json")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())

async def cdp_call(ws, method, params=None):
    msg_id = int(time.time() * 1000) % 1000000
    await ws.send(json.dumps({'id': msg_id, 'method': method, 'params': params or {}}))
    while True:
        resp = json.loads(await ws.recv())
        if resp.get('id') == msg_id:
            return resp.get('result', {})

async def onboard_wave5():
    # Target 1: Kaggle (DA 91)
    print("\n--- Launching Kaggle ---")
    k_tab = open_new_tab("https://www.kaggle.com/account/login")
    await asyncio.sleep(4)
    
    tabs = get_tabs()
    k_live = next((t for t in tabs if 'kaggle' in t.get('url', '').lower()), None)
    if k_live:
        print("Kaggle live URL:", k_live['url'])
        async with websockets.connect(k_live['webSocketDebuggerUrl']) as ws:
            # Click Sign in with Google
            expr = """(() => {
                const btn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').toLowerCase().includes('google'));
                if (btn) {
                    btn.click();
                    return 'Clicked Google on Kaggle';
                }
                return 'Google button not found on Kaggle';
            })()"""
            res = await cdp_call(ws, 'Runtime.evaluate', {'expression': expr, 'returnByValue': True})
            print(res.get('result', {}).get('value'))
    
    await asyncio.sleep(4)
    
    # Handle Google Chooser if opened
    tabs = get_tabs()
    chooser = next((t for t in tabs if 'accountchooser' in t.get('url', '').lower() and 'kaggle' in t.get('url', '').lower()), None)
    if chooser:
        print("Found Kaggle Google Chooser, selecting aiagent1510...")
        async with websockets.connect(chooser['webSocketDebuggerUrl']) as ws:
            expr = """(() => {
                const el = Array.from(document.querySelectorAll('div, li, span')).find(e => e.innerText && e.innerText.trim() === 'aiagent1510@gmail.com');
                if (el) {
                    const clickTarget = el.closest('li, [role=link], [role=button], div[data-identifier]') || el;
                    clickTarget.click();
                    return 'Clicked aiagent1510';
                }
                return 'Account element not found';
            })()"""
            res = await cdp_call(ws, 'Runtime.evaluate', {'expression': expr, 'returnByValue': True})
            print(res.get('result', {}).get('value'))

    # Target 2: Prisma Data Platform (DA 88)
    print("\n--- Launching Prisma Data Platform ---")
    p_tab = open_new_tab("https://console.prisma.io/login")
    await asyncio.sleep(4)
    
    tabs = get_tabs()
    p_live = next((t for t in tabs if 'prisma' in t.get('url', '').lower()), None)
    if p_live:
        print("Prisma live URL:", p_live['url'])
        async with websockets.connect(p_live['webSocketDebuggerUrl']) as ws:
            # Click Sign in with GitHub
            expr = """(() => {
                const btn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').toLowerCase().includes('github'));
                if (btn) {
                    btn.click();
                    return 'Clicked GitHub on Prisma';
                }
                return 'GitHub button not found on Prisma';
            })()"""
            res = await cdp_call(ws, 'Runtime.evaluate', {'expression': expr, 'returnByValue': True})
            print(res.get('result', {}).get('value'))

    await asyncio.sleep(4)

    # Target 3: Make.com (DA 88)
    print("\n--- Launching Make.com ---")
    m_tab = open_new_tab("https://us1.make.com/login")
    await asyncio.sleep(4)
    
    tabs = get_tabs()
    m_live = next((t for t in tabs if 'make.com' in t.get('url', '').lower()), None)
    if m_live:
        print("Make.com live URL:", m_live['url'])
        async with websockets.connect(m_live['webSocketDebuggerUrl']) as ws:
            expr = """(() => {
                const btn = Array.from(document.querySelectorAll('button, a')).find(b => (b.innerText || '').toLowerCase().includes('google'));
                if (btn) {
                    btn.click();
                    return 'Clicked Google on Make.com';
                }
                return 'Google button not found on Make.com';
            })()"""
            res = await cdp_call(ws, 'Runtime.evaluate', {'expression': expr, 'returnByValue': True})
            print(res.get('result', {}).get('value'))

if __name__ == '__main__':
    asyncio.run(onboard_wave5())
