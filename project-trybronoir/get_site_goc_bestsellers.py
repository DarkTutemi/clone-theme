import urllib.request
from bs4 import BeautifulSoup
import sys

sys.stdout.reconfigure(encoding='utf-8')

url = 'https://trybronoir.com/?cid=dpfse29nm4u0lrd'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

soup = BeautifulSoup(html, 'html.parser')

# Find bestsellers section
bs = soup.find(id='bestsellers') or soup.find(id=lambda x: x and 'bestseller' in x)
if not bs:
    # search for section with Our Bestsellers
    for s in soup.find_all(['section', 'div']):
        if 'Our Bestsellers' in s.get_text():
            bs = s
            break

print("Found bestsellers section on site goc:", bs.name if bs else "None")

cards = []
if bs:
    # find all product links
    for a in bs.find_all('a'):
        href = a.get('href', '')
        if '/products/' in href:
            clean_href = href.split('?')[0]
            if clean_href not in [c['href'] for c in cards]:
                # find title
                card_container = a.find_parent(class_=lambda x: x and ('product' in x or 'card' in x or 'item' in x))
                title = card_container.find(['h2', 'h3', 'h4', 'span', 'p'], class_=lambda x: x and 'title' in x) if card_container else None
                title_txt = title.get_text(strip=True) if title else a.get_text(strip=True)
                cards.append({'title': title_txt, 'href': href, 'clean_href': clean_href})

print(f"\nTotal product cards in #bestsellers on site goc: {len(cards)}")
for i, c in enumerate(cards):
    print(f"{i+1}. Title: {c['title']} | Link: {c['href']}")
