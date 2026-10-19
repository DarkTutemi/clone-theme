import requests
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

url = "https://g1spma-ku.myshopify.com/?preview_theme_id=191340118383"
r = requests.get(url, timeout=15)
print(f"HTTP Status: {r.status_code}")
html = r.text
print(f"HTML Content Length: {len(html)} bytes")

sections = set(re.findall(r'data-src="([^"]+)"', html))
print(f"\n[+] Sections detected in live preview ({len(sections)}):")
for s in sorted(sections):
    print(f"  - {s}")

imgs = re.findall(r'<img[^>]+src="([^"]+)"', html)
print(f"\n[+] Rendered images in live preview ({len(imgs)}):")
for img in imgs[:8]:
    print(f"  * {img}")

if "BUY 1, GET 2 FREE!" in html:
    print("\n[+] Verification PASSED: Urgency ticker and Bronoir headline rendered properly!")
