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
        "--remote-debugging-port=9232",
        "--no-first-run",
        "--no-default-browser-check",
        "http://localhost:4000/preview"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(3)
    try:
        tabs = json.loads(urllib.request.urlopen("http://localhost:9232/json").read())
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
            
            # 1. Test Inline Play
            print("--- Testing Inline Click ---")
            await send("Runtime.evaluate", {"expression": "document.querySelector('.video-wrapperrrr').click()"})
            await asyncio.sleep(3)
            
            inline_state = await send("Runtime.evaluate", {
                "expression": """(() => {
                    const vid = document.querySelector('.video-wrapperrrr video');
                    const btn = document.querySelector('.video-wrapperrrr .play-button');
                    return {
                        paused: vid.paused,
                        currentTime: vid.currentTime,
                        duration: vid.duration,
                        hasControls: vid.controls,
                        btnDisplay: btn ? btn.style.display : null
                    };
                })()""",
                "returnByValue": True
            })
            print("Inline result:", inline_state.get("result", {}).get("value"))
            
            # 2. Test Modal Expand
            print("--- Testing Modal Expand Button ---")
            await send("Runtime.evaluate", {"expression": "document.querySelector('.expand-modal-btn').click()"})
            await asyncio.sleep(2)
            
            modal_state = await send("Runtime.evaluate", {
                "expression": """(() => {
                    const modal = document.getElementById('video-review-modal');
                    const modalVid = document.getElementById('modal-video-element');
                    return {
                        modalActive: modal ? modal.classList.contains('active') : false,
                        modalVidPaused: modalVid ? modalVid.paused : null,
                        modalVidHasSrc: Boolean(modalVid && modalVid.src)
                    };
                })()""",
                "returnByValue": True
            })
            print("Modal result:", modal_state.get("result", {}).get("value"))

            # Capture screenshot of running video preview
            scr_res = await send("Page.captureScreenshot", {"format": "png"})
            import base64
            img_bytes = base64.b64decode(scr_res.get("data", ""))
            with open(r"C:\Users\vdvie\.gemini\antigravity-ide\brain\1b0221d5-22c1-41e9-89c1-c87b8ede21af\.tempmediaStorage\video_playing_verified.png", "wb") as f:
                f.write(img_bytes)
            print("Saved screenshot video_playing_verified.png")
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(check())
