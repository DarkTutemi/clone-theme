import subprocess, time, json, urllib.request, base64, socket, os, shutil
from urllib.parse import urlparse
import sys

sys.stdout.reconfigure(encoding='utf-8')

chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
port = 9697
art_dir = r'C:\Users\vdvie\.gemini\antigravity-ide\brain\1b0221d5-22c1-41e9-89c1-c87b8ede21af\.tempmediaStorage'
os.makedirs(art_dir, exist_ok=True)

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

    def snap(url, fname, click_swatch_idx=None):
        send_cdp('Page.navigate', {'url': url}, 1)
        recv_cdp()
        time.sleep(3)
        if click_swatch_idx is not None:
            js = f"const sw = document.querySelectorAll('.variant-swatch, .popup-swatch')[{click_swatch_idx}]; if (sw) sw.click();"
            send_cdp('Runtime.evaluate', {'expression': js}, 2)
            recv_cdp()
            time.sleep(1)
        send_cdp('Page.captureScreenshot', {'format': 'png'}, 3)
        resp = recv_cdp()
        while 'result' not in resp or 'data' not in resp['result']: resp = recv_cdp()
        img = base64.b64decode(resp['result']['data'])
        out_path = os.path.join(art_dir, fname)
        with open(out_path, 'wb') as f: f.write(img)
        print(f"✅ Saved screenshot: {fname}")

    snap("http://localhost:4000/products/bronoir-cosycloud-boot-warm-comfy-winter-barefoot-boot", "verified_cosycloud_pdp.png", click_swatch_idx=1)
    snap("http://localhost:4000/products/bronoir-toasty-cozy-winter-barefoot-shoes-with-thermal-lining", "verified_toasty_pdp.png", click_swatch_idx=1)
    snap("http://localhost:4000/products/bronoir-trail-masters-all-terrain-grip-barefoot-boots", "verified_trail_masters_pdp.png", click_swatch_idx=1)

finally:
    proc.terminate()
