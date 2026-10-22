import asyncio
import json
import urllib.request
import urllib.parse
import websockets

CDP_BASE = "http://127.0.0.1:9223"

async def open_admin_mail():
    url = "https://mail.google.com/mail/u/?authuser=admin@adicommunications.co.uk"
    quoted = urllib.parse.quote(url, safe="")
    endpoint = f"{CDP_BASE}/json/new?{quoted}"
    req = urllib.request.Request(endpoint, method="PUT")
    with urllib.request.urlopen(req) as resp:
        tab = json.loads(resp.read().decode())
    print("Opened mail tab:", tab.get("id"))
    ws_url = tab.get("webSocketDebuggerUrl")
    async with websockets.connect(ws_url, max_size=20*1024*1024) as ws:
        await asyncio.sleep(6)
        msg = {
            "id": 1,
            "method": "Runtime.evaluate",
            "params": {"expression": "({ url: window.location.href, title: document.title })", "returnByValue": True}
        }
        await ws.send(json.dumps(msg))
        resp = await ws.recv()
        state = json.loads(resp).get("result", {}).get("result", {}).get("value")
        print("Mail state:", state)

if __name__ == "__main__":
    asyncio.run(open_admin_mail())
