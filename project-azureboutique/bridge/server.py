import json
import time
import pathlib
import sys
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BRIDGE_DIR = pathlib.Path(__file__).parent
QUEUE = BRIDGE_DIR / "queue"
QUEUE.mkdir(exist_ok=True)
THEME_DIR = BRIDGE_DIR.parent / "theme"

# Path to shopify tools
TOOLS_DIR = BRIDGE_DIR.parent.parent / "tools" / "shopify-theme-cloner"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

class BridgeHandler(BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        if self.path == "/" or self.path == "/index.html":
            html_path = BRIDGE_DIR / "index.html"
            if html_path.exists():
                content = html_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(content)
                return

        elif self.path == "/preview" or self.path == "/preview.html":
            preview_path = BRIDGE_DIR / "preview.html"
            if preview_path.exists():
                content = preview_path.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(content)
                return

        elif self.path == "/api/queue" or self.path == "/api/tickets":
            tickets = []
            for f in sorted(QUEUE.glob("ticket_*.json")):
                try:
                    tickets.append(json.loads(f.read_text(encoding="utf-8")))
                except Exception:
                    pass
            content = json.dumps(tickets, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(content)
            return

        self.send_response(404)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        if self.path == "/ticket":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))
            
            n = len(list(QUEUE.glob("ticket_*.json"))) + 1
            ticket_id = f"ticket_{n:04d}"
            data["id"] = ticket_id
            if "status" not in data:
                data["status"] = "pending"
            if "created_at" not in data:
                data["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

            ticket_path = QUEUE / f"{ticket_id}.json"
            ticket_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            
            resp = json.dumps({"ok": True, "id": ticket_id, "ticket": data}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(resp)
            print(f"[+] Received Visual Inspector Ticket: {ticket_id} ({data.get('target', {}).get('source_file')})", flush=True)
            return

        elif self.path == "/api/sync-shopify":
            try:
                from core.store_client import ShopifyStoreClient
                client = ShopifyStoreClient()
                THEME_ID = "191338185071" # Target Rebuild Theme
                
                # Walk theme dir and upload files
                uploaded_count = 0
                for root, _, files in os.walk(THEME_DIR):
                    for f in files:
                        full_path = os.path.join(root, f)
                        rel_path = os.path.relpath(full_path, THEME_DIR).replace("\\", "/")
                        if rel_path.endswith((".liquid", ".json", ".css", ".js", ".html")):
                            with open(full_path, "r", encoding="utf-8", errors="ignore") as f_obj:
                                val = f_obj.read()
                            if client.upload_asset_to_theme(THEME_ID, rel_path, value=val):
                                uploaded_count += 1

                resp = json.dumps({
                    "ok": True,
                    "theme_id": THEME_ID,
                    "uploaded_count": uploaded_count,
                    "preview_url": f"https://{client.store}/?preview_theme_id={THEME_ID}",
                    "editor_url": f"https://admin.shopify.com/store/{client.store.split('.')[0]}/themes/{THEME_ID}/editor"
                }).encode("utf-8")
            except Exception as e:
                resp = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp)))
            self._send_cors_headers()
            self.end_headers()
            self.wfile.write(resp)
            return

        self.send_response(404)
        self._send_cors_headers()
        self.end_headers()

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    PORT = 4000
    ThreadingHTTPServer.allow_reuse_address = True
    server = ThreadingHTTPServer(("", PORT), BridgeHandler)
    print(f"[*] Design Bridge running at http://localhost:{PORT} and http://127.0.0.1:{PORT}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping Design Bridge.", flush=True)
