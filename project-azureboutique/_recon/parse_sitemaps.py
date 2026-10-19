import urllib.request
import xml.etree.ElementTree as ET
import json
import os

sub_sitemaps = [
    'https://www.azureboutique.co/sitemap_products_1.xml?from=9217655832885&to=10388246069557',
    'https://www.azureboutique.co/sitemap_pages_1.xml?from=131153953077&to=163612950837',
    'https://www.azureboutique.co/sitemap_collections_1.xml?from=486235078965&to=636925247797',
    'https://www.azureboutique.co/sitemap_blogs_1.xml'
]

result = {
    'home': ['https://www.azureboutique.co/'],
    'collections': [],
    'products': [],
    'pages': [],
    'blogs': [],
    'other': []
}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

for url in sub_sitemaps:
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read()
            root = ET.fromstring(xml_data)
            for elem in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                loc = elem.text.strip()
                if '/products/' in loc:
                    result['products'].append(loc)
                elif '/collections/' in loc:
                    result['collections'].append(loc)
                elif '/pages/' in loc:
                    result['pages'].append(loc)
                elif '/blogs/' in loc:
                    result['blogs'].append(loc)
                else:
                    result['other'].append(loc)
    except Exception as e:
        print(f'Error fetching {url}: {e}')

p_count = len(result['products'])
c_count = len(result['collections'])
pg_count = len(result['pages'])
b_count = len(result['blogs'])
print(f'Done! Found: {p_count} products, {c_count} collections, {pg_count} pages, {b_count} blogs')

output_path = r'f:\clone-theme\project-azureboutique\_recon\sitemap-categorized.json'
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=2, ensure_ascii=False)
