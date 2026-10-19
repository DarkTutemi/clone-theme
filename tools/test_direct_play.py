import asyncio
import json
import subprocess
import time
import urllib.request
import websockets

async def check():
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--remote-debugging-port=9231",
        "--no-first-run",
        "--no-default-browser-check",
        "http://localhost:4000/preview"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(3)
    try:
        tabs = json.loads(urllib.request.urlopen("http://localhost:9231/json").read())
        target_ws = [t["webSocketDebuggerUrl"] for t in tabs if t.get("type") == "page" and "localhost:4000" in t.get("url", "")][0]
        async with websockets.connect(target_ws) as ws:
            async def send(method, params=None):
                msg_id = int(time.time() * 1000) % 1000000
                await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get("method") == "Runtime.consoleAPICalled":
                        args = [a.get("value", a.get("description", "")) for a in res.get("params", {}).get("args", [])]
                        print("CONSOLE:", res.get("params", {}).get("type"), args)
                    if res.get("id") == msg_id:
                        return res.get("result", {})

            await send("Page.enable")
            await send("Runtime.enable")
            
            # Inject a test play on video 1
            test_res = await send("Runtime.evaluate", {
                "expression": """(() => {
                    const vid = document.querySelector('.video-wrapperrrr video');
                    const btn = document.querySelector('.video-wrapperrrr .play-button');
                    // Ensure src is on vid
                    if (!vid.src) {
                        const s = vid.querySelector('source');
                        if (s) vid.src = s.src;
                    }
                    vid.muted = true; // start muted for safe autoplay in all browsers
                    return vid.play().then(() => {
                        btn.style.display = 'none';
                        return { ok: true, src: vid.src, paused: vid.paused };
                    }).catch(e => ({ ok: false, err: e.message }));
                })()""",
                "awaitPromise": True,
                "returnByValue": True
            })
            print("Direct play with src evaluation:", test_res.get("result", {}).get("value"))
            
            await asyncio.sleep(3)
            
            res = await send("Runtime.evaluate", {
                "expression": """(() => {
                    const vid = document.querySelector('.video-wrapperrrr video');
                    const btn = document.querySelector('.video-wrapperrrr .play-button');
                    return {
                        paused: vid.paused,
                        currentTime: vid.currentTime,
                        duration: vid.duration,
                        readyState: vid.readyState,
                        btnDisplay: btn ? btn.style.display : null
                    };
                })()""",
                "returnByValue": True
            })
            print("After 3s playing:", res.get("result", {}).get("value"))
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(check())
