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
        "--remote-debugging-port=9233",
        "--no-first-run",
        "--no-default-browser-check",
        "--window-size=1440,900",
        "http://localhost:4000/preview#claim"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(3)
    try:
        tabs = json.loads(urllib.request.urlopen("http://localhost:9233/json").read())
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
            await asyncio.sleep(2)

            # Scroll to bestsellers
            await send("Runtime.evaluate", {"expression": "document.getElementById('bestsellers')?.scrollIntoView()"})
            await asyncio.sleep(1)

            # Check initial state of card 1
            init_state = await send("Runtime.evaluate", {
                "expression": """(() => {
                    const card = document.querySelector('.product-item-card');
                    const img = card.querySelector('.primary-img');
                    const dots = card.querySelectorAll('.swatch-dot');
                    return {
                        initialImg: img.src,
                        dotsCount: dots.length,
                        firstDotActive: dots[0].classList.contains('is-active')
                    };
                })()""",
                "returnByValue": True
            })
            print("Initial Card 1 State:", init_state.get("result", {}).get("value"))

            # Click 2nd swatch (White)
            print("Clicking 2nd swatch (White)...")
            await send("Runtime.evaluate", {"expression": "document.querySelectorAll('.product-item-card .swatch-dot')[1].click()"})
            await asyncio.sleep(1)

            after_white = await send("Runtime.evaluate", {
                "expression": """(() => {
                    const card = document.querySelector('.product-item-card');
                    const img = card.querySelector('.primary-img');
                    const dots = card.querySelectorAll('.swatch-dot');
                    return {
                        currentImg: img.src,
                        dot0Active: dots[0].classList.contains('is-active'),
                        dot1Active: dots[1].classList.contains('is-active')
                    };
                })()""",
                "returnByValue": True
            })
            print("After White Click:", after_white.get("result", {}).get("value"))

            # Click 3rd swatch (Pink)
            print("Clicking 3rd swatch (Pink)...")
            await send("Runtime.evaluate", {"expression": "document.querySelectorAll('.product-item-card .swatch-dot')[2].click()"})
            await asyncio.sleep(1)

            after_pink = await send("Runtime.evaluate", {
                "expression": """(() => {
                    const card = document.querySelector('.product-item-card');
                    const img = card.querySelector('.primary-img');
                    const dots = card.querySelectorAll('.swatch-dot');
                    return {
                        currentImg: img.src,
                        dot2Active: dots[2].classList.contains('is-active')
                    };
                })()""",
                "returnByValue": True
            })
            print("After Pink Click:", after_pink.get("result", {}).get("value"))

            # Test Card 2 (CosyCloud Boot) swatch click
            print("Clicking Card 2 second swatch (Midnight Black)...")
            await send("Runtime.evaluate", {
                "expression": """(() => {
                    const cards = document.querySelectorAll('.product-item-card');
                    if (cards[1]) {
                        const dots = cards[1].querySelectorAll('.swatch-dot');
                        if (dots[1]) dots[1].click();
                    }
                })()"""
            })
            await asyncio.sleep(1)

            card2_state = await send("Runtime.evaluate", {
                "expression": """(() => {
                    const cards = document.querySelectorAll('.product-item-card');
                    const img = cards[1].querySelector('.primary-img');
                    const dots = cards[1].querySelectorAll('.swatch-dot');
                    return {
                        card2Img: img.src,
                        card2Dot1Active: dots[1].classList.contains('is-active')
                    };
                })()""",
                "returnByValue": True
            })
            print("Card 2 State after click:", card2_state.get("result", {}).get("value"))

            # Capture screenshot of bestsellers
            scr_res = await send("Page.captureScreenshot", {"format": "png"})
            import base64
            img_bytes = base64.b64decode(scr_res.get("data", ""))
            with open(r"C:\Users\vdvie\.gemini\antigravity-ide\brain\1b0221d5-22c1-41e9-89c1-c87b8ede21af\.tempmediaStorage\swatches_switched_verified.png", "wb") as f:
                f.write(img_bytes)
            print("Saved screenshot swatches_switched_verified.png")
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(check())
