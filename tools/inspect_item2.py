import urllib.request
from bs4 import BeautifulSoup

url = "https://trybronoir.com/"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
html = urllib.request.urlopen(req).read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

selector = "product-list#block-template--27860728578148__custom_featured_collections_aNYzTQ-collection_RQjykN product-item:nth-of-type(2)"
item2 = soup.select_one(selector)
if not item2:
    print("Trying fallback selector...")
    items = soup.select("product-item")
    if len(items) > 1:
        item2 = items[1]

if item2:
    print("TAG:", item2.name, "ATTRS:", item2.attrs)
    print("=== HTML ===")
    print(item2.prettify())
else:
    print("Item 2 not found!")
