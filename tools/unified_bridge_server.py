import json
import time
import pathlib
import sys
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

BASE_DIR = pathlib.Path(__file__).parent.parent
BRONOIR_DIR = BASE_DIR / "project-trybronoir"
AZURE_DIR = BASE_DIR / "project-azureboutique"

QUEUE_DIR = BRONOIR_DIR / "bridge" / "queue"
QUEUE_DIR.mkdir(parents=True, exist_ok=True)

TOOLS_DIR = BASE_DIR / "tools" / "shopify-theme-cloner"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

THEME_BRONOIR_ID = "191340118383"
THEME_AZURE_ID = "191338185071"

class UnifiedBridgeHandler(BaseHTTPRequestHandler):
    def _send_cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, PUT, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, X-Requested-With")

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors()
        self.end_headers()

    def do_GET(self):
        print(f"[DEBUG GET] path={self.path}", flush=True)
        if self.path in ["/", "/index.html"]:
            html = self._get_dashboard_html()
            content = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self._send_cors()
            self.end_headers()
            self.wfile.write(content)
            return

        elif self.path in ["/preview", "/preview/bronoir"]:
            p = BRONOIR_DIR / "bridge" / "preview.html"
            if p.exists():
                content = p.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self._send_cors()
                self.end_headers()
                self.wfile.write(content)
                return

        elif self.path.startswith("/products") or self.path in ["/product", "/preview/product"]:
            clean_path = self.path.split("?")[0].rstrip("/")
            if clean_path.endswith(".js"):
                p_handle = clean_path.split("/")[-1][:-3]
                try:
                    auth_path = BRONOIR_DIR / "bridge" / "authentic_live_products.json"
                    if auth_path.exists():
                        with open(auth_path, "r", encoding="utf-8") as f:
                            all_prod = json.load(f)
                        match_prod = None
                        for k, v in all_prod.items():
                            if k in p_handle or p_handle in k:
                                match_prod = v
                                break
                        if match_prod:
                            content = json.dumps(match_prod).encode("utf-8")
                            self.send_response(200)
                            self.send_header("Content-Type", "application/json; charset=utf-8")
                            self.send_header("Content-Length", str(len(content)))
                            self._send_cors()
                            self.end_headers()
                            self.wfile.write(content)
                            return
                except Exception as e:
                    print(f"[!] Error serving product json: {e}", flush=True)

            handle = clean_path.split("/")[-1] if "/" in clean_path and clean_path != "/products" else "bronoir-skin-pro-with-copper-grounding-allround-barefoot-shoes"
            try:
                import sys, importlib
                bridge_dir = str(BRONOIR_DIR / "bridge")
                if bridge_dir not in sys.path:
                    sys.path.append(bridge_dir)
                import pdp_renderer
                importlib.reload(pdp_renderer)
                content = pdp_renderer.render_pdp(handle).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self._send_cors()
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                print(f"[!] Error rendering PDP {handle}: {e}", flush=True)
                p = BRONOIR_DIR / "bridge" / "product.html"
                if p.exists():
                    content = p.read_bytes()
                    self.send_response(200)
                    self.send_header("Content-Type", "text/html; charset=utf-8")
                    self.send_header("Content-Length", str(len(content)))
                    self._send_cors()
                    self.end_headers()
                    self.wfile.write(content)
                    return

        elif self.path.startswith("/collections"):
            clean_path = self.path.split("?")[0].rstrip("/")
            handle = clean_path.split("/")[-1] if "/" in clean_path else "barefoot-shoes-bogo-volume"
            try:
                import sys, importlib
                bridge_dir = str(BRONOIR_DIR / "bridge")
                if bridge_dir not in sys.path:
                    sys.path.append(bridge_dir)
                import collection_renderer
                importlib.reload(collection_renderer)
                content = collection_renderer.render_collection_page(handle).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self._send_cors()
                self.end_headers()
                self.wfile.write(content)
                return
            except Exception as e:
                print(f"[!] Error rendering collection {handle}: {e}", flush=True)


        elif self.path == "/preview/azure":
            p = AZURE_DIR / "bridge" / "preview.html"
            if p.exists():
                content = p.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(content)))
                self._send_cors()
                self.end_headers()
                self.wfile.write(content)
                return

        elif self.path in ["/api/queue", "/api/tickets"]:
            tickets = []
            for f in sorted(QUEUE_DIR.glob("ticket_*.json")):
                try:
                    tickets.append(json.loads(f.read_text(encoding="utf-8")))
                except Exception:
                    pass
            content = json.dumps(tickets, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self._send_cors()
            self.end_headers()
            self.wfile.write(content)
            return

        self.send_response(404)
        self._send_cors()
        self.end_headers()

    def do_POST(self):
        if self.path == "/ticket":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            data = json.loads(body.decode("utf-8"))
            
            n = len(list(QUEUE_DIR.glob("ticket_*.json"))) + 1
            ticket_id = f"ticket_{n:04d}"
            data["id"] = ticket_id
            data["status"] = "pending"
            if "created_at" not in data:
                data["created_at"] = time.strftime("%Y-%m-%dT%H:%M:%SZ")

            ticket_path = QUEUE_DIR / f"{ticket_id}.json"
            ticket_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            
            resp = json.dumps({"ok": True, "id": ticket_id, "ticket": data}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp)))
            self._send_cors()
            self.end_headers()
            self.wfile.write(resp)
            print(f"[+] Design Bridge Received Ticket: {ticket_id} ({data.get('target', {}).get('source_file')})", flush=True)
            return

        elif self.path == "/api/sync-shopify":
            try:
                from core.store_client import ShopifyStoreClient
                client = ShopifyStoreClient()
                theme_dir = BRONOIR_DIR / "theme"
                uploaded = 0
                for root, _, files in os.walk(theme_dir):
                    for f in files:
                        fp = pathlib.Path(root) / f
                        rel = fp.relative_to(theme_dir).as_posix()
                        if rel.endswith((".liquid", ".json", ".css", ".js", ".html")):
                            content = fp.read_text(encoding="utf-8", errors="ignore")
                            if client.upload_asset_to_theme(THEME_BRONOIR_ID, rel, value=content):
                                uploaded += 1
                resp = json.dumps({
                    "ok": True,
                    "theme_id": THEME_BRONOIR_ID,
                    "uploaded_count": uploaded,
                    "preview_url": f"https://{client.store}/?preview_theme_id={THEME_BRONOIR_ID}",
                    "editor_url": f"https://admin.shopify.com/store/{client.store.split('.')[0]}/themes/{THEME_BRONOIR_ID}/editor"
                }).encode("utf-8")
            except Exception as e:
                resp = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")

            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(resp)))
            self._send_cors()
            self.end_headers()
            self.wfile.write(resp)
            return

        self.send_response(404)
        self._send_cors()
        self.end_headers()

    def log_message(self, format, *args):
        pass

    def _get_dashboard_html(self):
        return """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <title>Design Bridge — Unified Control Center</title>
  <style>
    :root {
      --bg: #090d16; --card: #111827; --card-sub: #162032; --border: #1f2937;
      --primary: #44c2fd; --ocean: #08435e; --success: #10b981; --sale: #e11d48;
      --text: #f8fafc; --muted: #94a3b8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: var(--bg); color: var(--text); padding-bottom: 60px; }
    header { background: var(--card); border-bottom: 1px solid var(--border); padding: 1.25rem 2rem; display: flex; justify-content: space-between; align-items: center; }
    .badge { padding: 4px 8px; border-radius: 4px; font-size: 11px; font-weight: 700; text-transform: uppercase; }
    .badge-cyan { background: var(--primary); color: #000; }
    .badge-green { background: #059669; color: #fff; }
    .container { max-width: 1180px; margin: 2rem auto; padding: 0 1.5rem; display: flex; flex-direction: column; gap: 2rem; }
    .project-banner { background: linear-gradient(135deg, #08435e 0%, #031e2b 100%); border: 1px solid rgba(68,194,253,0.3); border-radius: 14px; padding: 2rem; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .actions-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.25rem; margin-top: 1.5rem; }
    .action-card { background: var(--card-sub); border: 1px solid var(--border); border-radius: 10px; padding: 1.5rem; display: flex; flex-direction: column; gap: 0.75rem; transition: transform 0.2s, border-color 0.2s; }
    .action-card:hover { transform: translateY(-2px); border-color: var(--primary); }
    .btn { display: inline-flex; align-items: center; justify-content: center; gap: 8px; padding: 12px 20px; font-size: 14px; font-weight: 700; border-radius: 6px; text-decoration: none; border: none; cursor: pointer; transition: all 0.2s; }
    .btn-cyan { background: var(--primary); color: #000; }
    .btn-cyan:hover { background: #fff; }
    .btn-green { background: var(--success); color: #fff; }
    .btn-green:hover { background: #059669; }
    .btn-secondary { background: #374151; color: #fff; }
    .btn-secondary:hover { background: #4b5563; }
    .queue-card { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 1.75rem; }
  </style>
</head>
<body>
  <header>
    <div style="display: flex; align-items: center; gap: 10px;">
      <span class="badge badge-cyan">DESIGN BRIDGE</span>
      <strong>Shopify 1:1 Rebuild &amp; Live Inspector</strong>
    </div>
    <div style="font-size: 13px; color: var(--muted);">
      Store: <code style="color: var(--primary);">g1spma-ku.myshopify.com</code>
    </div>
  </header>

  <div class="container">
    <!-- Active Project: Bronoir Canada -->
    <div class="project-banner">
      <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 12px;">
        <div>
          <span class="badge badge-green">DỰ ÁN MỚI NHẤT — ĐÃ DEPLOY 1:1</span>
          <h1 style="font-size: 2rem; margin: 8px 0; color: #fff;">Bronoir Canada — Grounding Barefoot Shoes</h1>
          <p style="color: #94a3b8; font-size: 14px; max-width: 650px;">
            Nhân bản 1:1 giao diện, danh mục 1,010 sản phẩm, ảnh thật độ phân giải cao, bảng so sánh và cơ chế BOGO Prime Deal.
          </p>
        </div>
        <button id="btn-sync-bronoir" class="btn btn-green">
          ⚡ Đồng Bộ Theme Lên Shopify (ID: 191340118383)
        </button>
      </div>

      <div id="sync-notice" style="display:none; padding:10px 14px; border-radius:6px; margin-top:14px; font-size:13px;"></div>

      <div class="actions-grid">
        <div class="action-card">
          <h3 style="color:#fff;">🖥️ Offline Preview (Localhost)</h3>
          <p style="color:var(--muted); font-size:13px; flex-grow:1;">
            Xem trang web cục bộ với tốc độ tức thì, không cần mật khẩu. Dùng Chrome Extension (Alt+I) để chỉ định phần tử muốn sửa.
          </p>
          <a href="/preview" target="_blank" class="btn btn-cyan">Mở Preview Local (:4000/preview) ➔</a>
        </div>

        <div class="action-card">
          <h3 style="color:#fff;">👁️ Shopify Live Preview</h3>
          <p style="color:var(--muted); font-size:13px; flex-grow:1;">
            Xem trước theme chính thức trên store Shopify g1spma-ku (Theme ID: 191340118383).
          </p>
          <a href="https://g1spma-ku.myshopify.com/?preview_theme_id=191340118383" target="_blank" class="btn btn-secondary">Mở Shopify Preview ↗</a>
        </div>

        <div class="action-card">
          <h3 style="color:#fff;">🎨 Shopify Theme Editor</h3>
          <p style="color:var(--muted); font-size:13px; flex-grow:1;">
            Trình tùy biến kéo - thả trong Admin Shopify để chỉnh sửa nội dung, banner, bảng giá.
          </p>
          <a href="https://admin.shopify.com/store/g1spma-ku/themes/191340118383/editor" target="_blank" class="btn btn-secondary">Mở Theme Editor ↗</a>
        </div>
      </div>
    </div>

    <!-- Ticket Queue -->
    <div class="queue-card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem; border-bottom: 1px solid var(--border); padding-bottom: 0.75rem;">
        <h3 style="color: #fff; display: flex; align-items: center; gap: 8px;">
          <span>📋 Hàng Đợi Chỉnh Sửa Từ Chrome Extension (Alt + I)</span>
          <span id="queue-count" class="badge badge-cyan">0</span>
        </h3>
        <button id="btn-refresh" class="btn btn-secondary" style="padding: 6px 12px; font-size: 12px;">🔄 Làm mới</button>
      </div>

      <div id="tickets-container" style="display: flex; flex-direction: column; gap: 10px;">
        <div style="color: var(--muted); text-align: center; padding: 20px;">Đang tải ticket...</div>
      </div>
    </div>
  </div>

  <script>
    async function loadTickets() {
      try {
        const res = await fetch('/api/queue');
        const tickets = await res.json();
        const container = document.getElementById('tickets-container');
        document.getElementById('queue-count').textContent = tickets.length;
        if (tickets.length === 0) {
          container.innerHTML = '<div style="color: var(--muted); text-align: center; padding: 20px;">Chưa có yêu cầu nào. Mở trang web và nhấn Alt + I để bắt đầu chỉ định phần tử cho Agent!</div>';
          return;
        }
        container.innerHTML = tickets.reverse().map(t => `
          <div style="background:#0f172a; border:1px solid var(--border); border-radius:8px; padding:12px 16px; display:flex; justify-content:space-between; align-items:center;">
            <div>
              <div style="font-weight:700; color:#fff; font-size:14px;">${t.prompt || '(Không có mô tả)'}</div>
              <div style="font-size:12px; color:var(--muted); font-family:monospace; margin-top:3px;">
                ${t.target?.source_file ? '📄 ' + t.target.source_file : ''} • Selector: <code>${t.target?.selector || ''}</code>
              </div>
            </div>
            <span class="badge ${t.status === 'applied' ? 'badge-green' : 'badge-cyan'}">${t.status === 'applied' ? 'ĐÃ SỬA' : 'CHỜ AGENT'}</span>
          </div>
        `).join('');
      } catch (e) {}
    }

    const btnSync = document.getElementById('btn-sync-bronoir');
    const notice = document.getElementById('sync-notice');
    btnSync.addEventListener('click', async () => {
      btnSync.disabled = true;
      btnSync.textContent = '⏳ Đang đồng bộ...';
      notice.style.display = 'block';
      notice.style.background = 'rgba(68,194,253,0.15)';
      notice.style.color = '#7dd3fc';
      notice.textContent = 'Đang đẩy toàn bộ file Liquid và CSS lên Theme ID: 191340118383...';
      try {
        const res = await fetch('/api/sync-shopify', { method: 'POST' });
        const data = await res.json();
        if (data.ok) {
          notice.style.background = 'rgba(16,185,129,0.15)';
          notice.style.color = '#6ee7b7';
          notice.innerHTML = `✅ Đã đồng bộ thành công <strong>${data.uploaded_count}</strong> files lên Shopify! <a href="${data.preview_url}" target="_blank" style="color:#38bdf8; text-decoration:underline; margin-left:8px;">Xem kết quả ngay ↗</a>`;
        }
      } catch (e) {
        notice.textContent = 'Lỗi kết nối đồng bộ.';
      } finally {
        btnSync.disabled = false;
        btnSync.textContent = '⚡ Đồng Bộ Theme Lên Shopify (ID: 191340118383)';
      }
    });

    document.getElementById('btn-refresh').addEventListener('click', loadTickets);
    loadTickets();
    setInterval(loadTickets, 5000);
  </script>
</body>
</html>"""

if __name__ == "__main__":
    PORT = 4000
    ThreadingHTTPServer.allow_reuse_address = True
    server = ThreadingHTTPServer(("", PORT), UnifiedBridgeHandler)
    print(f"[*] Unified Design Bridge running at http://localhost:{PORT} and http://127.0.0.1:{PORT}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] Stopping Unified Design Bridge.", flush=True)
