import json
from bs4 import BeautifulSoup

# 1. Check preview.html for all cards in #bestsellers
with open('f:/clone-theme/project-trybronoir/bridge/preview.html', 'r', encoding='utf-8', errors='ignore') as f:
    soup = BeautifulSoup(f.read(), 'html.parser')

bs_section = soup.find(id='bestsellers')
cards = []
if bs_section:
    for link in bs_section.find_all('a'):
        href = link.get('href', '')
        if '/products/' in href:
            title_el = link.find(class_='product-card__title') or link.find(['h2', 'h3', 'h4'])
            title = title_el.get_text(strip=True) if title_el else link.get_text(strip=True)
            if href not in [c['href'] for c in cards]:
                cards.append({'title': title, 'href': href})

print(f"Total product cards in #bestsellers: {len(cards)}")
for i, c in enumerate(cards):
    print(f"{i+1}. {c['title']} -> {c['href']}")

# 2. Check catalog
with open('f:/clone-theme/project-trybronoir/bridge/bestsellers_catalog.json', 'r', encoding='utf-8') as f:
    catalog = json.load(f)

print(f"\nTotal products in bestsellers_catalog.json: {len(catalog)}")
for i, p in enumerate(catalog):
    print(f"{i+1}. {p.get('title')} -> handle: {p.get('handle')}")
