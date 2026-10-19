#!/usr/bin/env python
"""
Bridge Ticket Processor & Shopify Auto-Sync Tool
Usage:
  python process_bridge_tickets.py --list
  python process_bridge_tickets.py --show <ticket_id>
  python process_bridge_tickets.py --sync-shopify
  python process_bridge_tickets.py --mark-applied <ticket_id>
"""

import os
import sys
import json
import argparse
import pathlib

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = pathlib.Path(__file__).parent.parent
QUEUES = [
    BASE_DIR / "project-trybronoir" / "bridge" / "queue",
    BASE_DIR / "project-azureboutique" / "bridge" / "queue"
]
THEME_DIR = BASE_DIR / "project-trybronoir" / "theme"

TOOLS_DIR = BASE_DIR / "tools" / "shopify-theme-cloner"
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))

THEME_ID = "191338185071" # Target Rebuild Theme on g1spma-ku.myshopify.com

def list_tickets():
    tickets = []
    for q in QUEUES:
        if q.exists():
            for f in sorted(q.glob("ticket_*.json")):
                try:
                    tickets.append(json.loads(f.read_text(encoding="utf-8")))
                except Exception:
                    pass

    print(f"\n=== DANH SÁCH TICKET CHỈ ĐỊNH TỪ CHROME EXTENSION ({len(tickets)}) ===")
    if not tickets:
        print("  (Chưa có ticket nào trong hàng đợi. Hãy mở website và dùng extension Alt+I để tạo ticket!)")
        return

    for t in tickets:
        status_icon = "⏳" if t.get("status") == "pending" else "✅"
        print(f"[{status_icon} {t.get('status', 'unknown').upper()}] {t.get('id')} — {t.get('created_at')}")
        target = t.get("target", {})
        print(f"    File nguồn: {target.get('source_file')}")
        print(f"    Selector  : {target.get('selector')}")
        print(f"    Nội dung  : \"{target.get('text_content', '')[:60]}\"")
        print(f"    Yêu cầu   : {t.get('prompt')}")
        print("-" * 60)

def show_ticket(ticket_id):
    ticket_file = QUEUE_DIR / f"{ticket_id}.json"
    if not ticket_file.exists():
        print(f"[-] Không tìm thấy ticket: {ticket_id}")
        return
    data = json.loads(ticket_file.read_text(encoding="utf-8"))
    print(json.dumps(data, indent=2, ensure_ascii=False))

def mark_applied(ticket_id):
    ticket_file = QUEUE_DIR / f"{ticket_id}.json"
    if not ticket_file.exists():
        print(f"[-] Không tìm thấy ticket: {ticket_id}")
        return
    data = json.loads(ticket_file.read_text(encoding="utf-8"))
    data["status"] = "applied"
    data["applied_at"] = time_now()
    ticket_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"[+] Đã cập nhật ticket {ticket_id} thành 'applied' thành công!")

def sync_to_shopify(target_asset=None):
    from core.store_client import ShopifyStoreClient
    client = ShopifyStoreClient()
    print(f"[*] Đang đồng bộ giao diện lên Shopify store: {client.store} (Theme ID: {THEME_ID})...")

    if target_asset:
        full_path = THEME_DIR / target_asset
        if not full_path.exists():
            print(f"[-] File không tồn tại: {full_path}")
            return
        content = full_path.read_text(encoding="utf-8", errors="ignore")
        ok = client.upload_asset_to_theme(THEME_ID, target_asset.replace("\\", "/"), value=content)
        if ok:
            print(f"[+] Đã upload thành công asset: {target_asset}")
        else:
            print(f"[-] Upload thất bại: {target_asset}")
    else:
        # Sync entire theme
        uploaded = 0
        for root, _, files in os.walk(THEME_DIR):
            for f in files:
                fp = pathlib.Path(root) / f
                rel = fp.relative_to(THEME_DIR).as_posix()
                if rel.endswith((".liquid", ".json", ".css", ".js", ".html")):
                    content = fp.read_text(encoding="utf-8", errors="ignore")
                    if client.upload_asset_to_theme(THEME_ID, rel, value=content):
                        uploaded += 1
                        print(f"  + Uploaded: {rel}")
        print(f"[+] Đồng bộ hoàn tất! Tổng cộng {uploaded} files đã cập nhật.")
        print(f"    Preview URL : https://{client.store}/?preview_theme_id={THEME_ID}")
        print(f"    Theme Editor: https://admin.shopify.com/store/{client.store.split('.')[0]}/themes/{THEME_ID}/editor")

def time_now():
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%SZ")

def main():
    parser = argparse.ArgumentParser(description="Bridge Ticket Processor & Shopify Auto-Sync")
    parser.add_argument("--list", action="store_true", help="Liệt kê danh sách ticket")
    parser.add_argument("--show", help="Hiển thị chi tiết ticket theo ID (ví dụ: ticket_0001)")
    parser.add_argument("--mark-applied", help="Đánh dấu ticket đã hoàn thành")
    parser.add_argument("--sync-shopify", action="store_true", help="Đồng bộ theme cục bộ lên Shopify")
    parser.add_argument("--sync-file", help="Đồng bộ 1 file cụ thể lên Shopify (ví dụ: sections/hero-banner.liquid)")

    args = parser.parse_args()

    if args.list:
        list_tickets()
    elif args.show:
        show_ticket(args.show)
    elif args.mark_applied:
        mark_applied(args.mark_applied)
    elif args.sync_shopify:
        sync_to_shopify()
    elif args.sync_file:
        sync_to_shopify(args.sync_file)
    else:
        list_tickets()

if __name__ == "__main__":
    main()
