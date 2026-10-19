import urllib.request
from bs4 import BeautifulSoup
import re

url = "https://trybronoir.com/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

# Look for bestsellers or product cards
cards = soup.select(".product-card, .card, [class*='product-item'], [class*='card--product']")
print(f"Cards found: {len(cards)}")

# Search for swatch markup
for card in cards[:3]:
    swatch_wrap = card.select("[class*='swatch'], [class*='color'], [class*='variant']")
    print("Card swatch count:", len(swatch_wrap))
    for sw in swatch_wrap:
        print("TAG:", sw.name, "CLASS:", sw.get("class"))
        print(sw.prettify()[:400])

# Also search full HTML for any swatch image change scripts or attributes
print("\n--- Searching for swatch data in HTML ---")
for m in re.finditer(r'(swatch|variant-image|data-image|data-media)', html, re.I):
    start = max(0, m.start() - 100)
    end = min(len(html), m.end() + 200)
    print("Match:", html[start:end])
    break
