import subprocess, time, json, urllib.request, base64, socket
from urllib.parse import urlparse
import sys

sys.stdout.reconfigure(encoding='utf-8')

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9696

handles = [
    "bronoir-skin-pro-with-copper-grounding-allround-barefoot-shoes",
    "bronoir-cosycloud-boot-warm-comfy-winter-barefoot-boot",
    "bronoir-hikers-orthopedic-outdoor-barefoot-shoes-bogo",
    "bronoir-trail-masters-all-terrain-grip-barefoot-boots",
    "bronoir-arctic-2-0-winter-barefoot-shoes-1-1-free",
    "bronoir-toasty-cozy-winter-barefoot-shoes-with-thermal-lining",
    "bronoir-summit-winter-warm-insulated-barefoot-shoes",
    "bronoir-cloudwalk-ultra-light-breathable-barefoot-sneakers"
]

proc = subprocess.Popen([
    chrome_path, f'--remote-debugging-port={port}', '--headless=new', '--disable-gpu', '--no-sandbox',
    '--window-size=1400,1200'
])

try:
    time.sleep(3)
    tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json').read().decode('utf-8'))
    target_tab = [t for t in tabs if t.get('type') == 'page'][0]
    ws_url = target_tab['webSocketDebuggerUrl']
    parsed = urlparse(ws_url)
    sock = socket.create_connection((parsed.hostname, parsed.port))

    key = base64.b64encode(b'test123456789012').decode('utf-8')
    req = f'GET {parsed.path} HTTP/1.1\r\nHost: {parsed.hostname}:{parsed.port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n'
    sock.sendall(req.encode('utf-8'))
    sock.recv(4096)

    def send_cdp(method, params=None, msg_id=1):
        msg = json.dumps({'id': msg_id, 'method': method, 'params': params or {}})
        payload = msg.encode('utf-8')
        length = len(payload)
        frame = bytearray([0x81])
        if length <= 125: frame.append(0x80 | length)
        elif length <= 65535: frame.append(0x80 | 126); frame.extend(length.to_bytes(2, 'big'))
        else: frame.append(0x80 | 127); frame.extend(length.to_bytes(8, 'big'))
        mask = b'\x12\x34\x56\x78'
        frame.extend(mask)
        masked = bytearray(b ^ mask[i % 4] for i, b in enumerate(payload))
        frame.extend(masked)
        sock.sendall(frame)

    def recv_cdp():
        b1, b2 = sock.recv(2)
        length = b2 & 0x7f
        if length == 126: length = int.from_bytes(sock.recv(2), 'big')
        elif length == 127: length = int.from_bytes(sock.recv(8), 'big')
        data = bytearray()
        while len(data) < length: data.extend(sock.recv(length - len(data)))
        return json.loads(data.decode('utf-8', errors='ignore'))

    for idx, handle in enumerate(handles):
        url = f"http://localhost:4000/products/{handle}"
        send_cdp('Page.navigate', {'url': url}, 100 + idx*10)
        recv_cdp()
        time.sleep(2.5)

        js_eval = '''
        (async function() {
            const title = document.title;
            const h1 = document.querySelector('h1') ? document.querySelector('h1').innerText.trim() : null;
            const thumbs = Array.from(document.querySelectorAll('.product__thumbnail-item'));
            const swatches = Array.from(document.querySelectorAll('.variant-swatch, .popup-swatch'));
            const items = Array.from(document.querySelectorAll('.product__media-item'));
            const selItem = document.querySelector('.product__media-item.is-selected');
            const initImg = selItem ? (selItem.querySelector('img') ? selItem.querySelector('img').src : null) : null;
            
            // Test clicking thumbnail 1 (second thumb) if available
            let thumbClickSuccess = false;
            let thumbImgAfter = null;
            if (thumbs.length > 1) {
                thumbs[1].click();
                await new Promise(r => setTimeout(r, 400));
                const selItemAfter = document.querySelector('.product__media-item.is-selected');
                thumbImgAfter = selItemAfter ? (selItemAfter.querySelector('img') ? selItemAfter.querySelector('img').src : null) : null;
                thumbClickSuccess = (thumbImgAfter !== initImg);
            }

            // Test clicking swatch 1 (second swatch) if available
            let swatchClickSuccess = false;
            let swatchImgAfter = null;
            if (swatches.length > 1) {
                swatches[1].click();
                await new Promise(r => setTimeout(r, 400));
                const selItemAfter = document.querySelector('.product__media-item.is-selected');
                swatchImgAfter = selItemAfter ? (selItemAfter.querySelector('img') ? selItemAfter.querySelector('img').src : null) : null;
                swatchClickSuccess = (swatchImgAfter !== null);
            }

            // Headings in custom info blocks or image with text
            const infoH2 = Array.from(document.querySelectorAll('.custom-info-blocks h2, .custom-info-blocks h3, .image-with-text h3')).map(h => h.innerText.trim());

            return {
                title,
                h1,
                thumbsCount: thumbs.length,
                swatchesCount: swatches.length,
                itemsCount: items.length,
                initImg: initImg ? initImg.split('/').pop().split('?')[0] : null,
                thumbClickSuccess,
                thumbImgAfter: thumbImgAfter ? thumbImgAfter.split('/').pop().split('?')[0] : null,
                swatchClickSuccess,
                swatchImgAfter: swatchImgAfter ? swatchImgAfter.split('/').pop().split('?')[0] : null,
                infoH2: infoH2.slice(0, 4)
            };
        })()
        '''
        send_cdp('Runtime.evaluate', {'expression': js_eval, 'returnByValue': True, 'awaitPromise': True}, 200 + idx*10)
        resp = recv_cdp()
        while 'result' not in resp or 'result' not in resp['result']: resp = recv_cdp()
        val = resp['result']['result']['value']
        print(f"\n================ [{idx+1}/8] {handle} ================")
        print(json.dumps(val, indent=2, ensure_ascii=False))

finally:
    proc.terminate()
