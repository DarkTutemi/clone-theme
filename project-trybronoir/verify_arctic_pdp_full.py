import subprocess, time, json, urllib.request, base64, socket
from urllib.parse import urlparse

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9695
proc = subprocess.Popen([
    chrome_path, f'--remote-debugging-port={port}', '--headless=new', '--disable-gpu', '--no-sandbox',
    '--window-size=1400,1200',
    'http://localhost:4000/products/bronoir-arctic-2-0-winter-barefoot-shoes-1-1-free'
])

try:
    time.sleep(3)
    tabs = json.loads(urllib.request.urlopen(f'http://127.0.0.1:{port}/json').read().decode('utf-8'))
    page_tabs = [t for t in tabs if t.get('type') == 'page']
    target_tab = page_tabs[0] if page_tabs else tabs[0]
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

    js_eval = '''
    (async function() {
        const swatches = Array.from(document.querySelectorAll('.variant-swatch'));
        const thumbs = Array.from(document.querySelectorAll('.product__thumbnail-item'));
        const swatchResults = [];
        
        for (let i = 0; i < swatches.length; i++) {
            const sw = swatches[i];
            const inp = sw.querySelector('input');
            const colorName = inp ? inp.value : sw.innerText.trim();
            
            // Click swatch
            sw.click();
            await new Promise(r => setTimeout(r, 450));
            
            const selectedMedia = document.querySelector('.product__media-item.is-selected');
            const selectedImg = selectedMedia ? selectedMedia.querySelector('img').src : null;
            const sliderTransform = document.querySelector('.flickity-slider') ? document.querySelector('.flickity-slider').style.transform : null;
            const activeThumb = document.querySelector('.product__thumbnail-item[aria-current="true"]');
            
            swatchResults.push({
                color: colorName,
                imgFilename: selectedImg ? selectedImg.split('/').pop().split('?')[0] : null,
                sliderTransform,
                activeThumbIndex: thumbs.indexOf(activeThumb)
            });
        }

        // Test thumbnail clicks directly
        const thumbResults = [];
        const testIndices = [0, 4, 8, 12, 15];
        for (let idx of testIndices) {
            if (thumbs[idx]) {
                thumbs[idx].click();
                await new Promise(r => setTimeout(r, 450));
                const selectedMedia = document.querySelector('.product__media-item.is-selected');
                const selectedImg = selectedMedia ? selectedMedia.querySelector('img').src : null;
                thumbResults.push({
                    clickedThumb: idx,
                    imgFilename: selectedImg ? selectedImg.split('/').pop().split('?')[0] : null
                });
            }
        }

        // Description sections
        const descHeadings = Array.from(document.querySelectorAll('.custom-info-blocks h2, .custom-info-blocks h3')).map(h => h.innerText.trim());

        return {
            swatchResults,
            thumbResults,
            descHeadings
        };
    })()
    '''
    send_cdp('Runtime.evaluate', {'expression': js_eval, 'returnByValue': True, 'awaitPromise': True}, 2)
    resp = recv_cdp()
    while 'result' not in resp or 'result' not in resp['result']: resp = recv_cdp()
    print('VERIFICATION RESULTS:\n', json.dumps(resp['result']['result']['value'], indent=2))

    # Take screenshot of the top fold with Black selected
    send_cdp('Page.captureScreenshot', {'format': 'png'}, 3)
    resp_snap = recv_cdp()
    while 'result' not in resp_snap or 'data' not in resp_snap['result']: resp_snap = recv_cdp()
    img_data = base64.b64decode(resp_snap['result']['data'])
    with open('f:/clone-theme/project-trybronoir/verified_arctic_top.png', 'wb') as f:
        f.write(img_data)
    print("Saved verified_arctic_top.png")

    # Scroll down to custom-info-blocks and screenshot
    send_cdp('Runtime.evaluate', {'expression': 'window.scrollTo(0, 1200)'}, 4)
    recv_cdp()
    time.sleep(1)
    send_cdp('Page.captureScreenshot', {'format': 'png'}, 5)
    resp_snap2 = recv_cdp()
    while 'result' not in resp_snap2 or 'data' not in resp_snap2['result']: resp_snap2 = recv_cdp()
    img_data2 = base64.b64decode(resp_snap2['result']['data'])
    with open('f:/clone-theme/project-trybronoir/verified_arctic_description.png', 'wb') as f:
        f.write(img_data2)
    print("Saved verified_arctic_description.png")

finally:
    proc.terminate()
