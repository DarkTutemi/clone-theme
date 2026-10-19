import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://trybronoir.com/products/bronoir%E2%84%A2-arctic-2-0-winter-barefoot-shoes-1-1-free?cid=dpfse29nm4u0lrdcj46rhbe6'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

for el in soup.find_all(['h1', 'h2', 'h3', 'h4', 'p', 'div', 'section']):
    txt = el.get_text(strip=True)
    if 'Built for' in txt and len(txt) < 100:
        print("MATCH:", el.name, el.get('class'), txt)
        p = el
        while p and p.name != '[document]':
            if p.get('class') and 'shopify-section' in p.get('class'):
                print("  PARENT SECTION:", p.get('id'), p.get('class'))
                break
            p = p.parent
