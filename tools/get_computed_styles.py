import asyncio, json, subprocess, time, urllib.request
import websockets

async def get_styles():
    cmd = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        "--headless=new",
        "--remote-debugging-port=9234",
        "--no-first-run",
        "--no-default-browser-check",
        "https://trybronoir.com/"
    ]
    proc = subprocess.Popen(cmd)
    time.sleep(3)
    try:
        tabs = json.loads(urllib.request.urlopen("http://localhost:9234/json").read())
        target_ws = [t["webSocketDebuggerUrl"] for t in tabs if t.get("type") == "page"][0]
        async with websockets.connect(target_ws) as ws:
            async def send(method, params=None):
                msg_id = int(time.time() * 1000) % 1000000
                await ws.send(json.dumps({"id": msg_id, "method": method, "params": params or {}}))
                while True:
                    res = json.loads(await ws.recv())
                    if res.get("id") == msg_id:
                        return res.get("result", {})

            await send("Page.enable")
            await send("Runtime.enable")
            await asyncio.sleep(3)

            res = await send("Runtime.evaluate", {
                "expression": """(() => {
                    const item = document.querySelectorAll('product-item')[1];
                    if (!item) return 'Item not found';
                    const cs = window.getComputedStyle(item);
                    const title = item.querySelector('.product-item-meta__title');
                    const titleCs = title ? window.getComputedStyle(title) : null;
                    const price = item.querySelector('.price');
                    const priceCs = price ? window.getComputedStyle(price) : null;
                    const swatches = item.querySelector('.color-swatch-list');
                    const swatchesCs = swatches ? window.getComputedStyle(swatches) : null;
                    const dot = item.querySelector('.color-swatch__item');
                    const dotCs = dot ? window.getComputedStyle(dot) : null;
                    
                    return {
                        item: {
                            background: cs.backgroundColor,
                            padding: cs.padding,
                            borderRadius: cs.borderRadius,
                            boxShadow: cs.boxShadow,
                            border: cs.border
                        },
                        title: titleCs ? {
                            fontSize: titleCs.fontSize,
                            fontWeight: titleCs.fontWeight,
                            color: titleCs.color,
                            textAlign: titleCs.textAlign
                        } : null,
                        price: priceCs ? {
                            fontSize: priceCs.fontSize,
                            fontWeight: priceCs.fontWeight,
                            color: priceCs.color
                        } : null,
                        swatches: swatchesCs ? {
                            justifyContent: swatchesCs.justifyContent,
                            gap: swatchesCs.gap
                        } : null,
                        dot: dotCs ? {
                            width: dotCs.width,
                            height: dotCs.height,
                            borderRadius: dotCs.borderRadius,
                            boxShadow: dotCs.boxShadow
                        } : null
                    };
                })()""",
                "returnByValue": True
            })
            print("Computed Styles from trybronoir:", json.dumps(res.get("result", {}).get("value"), indent=2))
    finally:
        proc.terminate()

if __name__ == "__main__":
    asyncio.run(get_styles())
