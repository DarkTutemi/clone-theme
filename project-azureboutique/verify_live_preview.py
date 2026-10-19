import requests
from bs4 import BeautifulSoup

url = 'https://g1spma-ku.myshopify.com/?preview_theme_id=191338185071'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
r = requests.get(url, headers=headers, timeout=20)
print(f"Status: {r.status_code}")
print(f"Length: {len(r.text)}")

soup = BeautifulSoup(r.text, 'html.parser')
title = soup.find('title')
print(f"Page Title: {title.get_text() if title else 'No title'}")

# Check if password page or storefront
if 'password' in r.text.lower():
    print("Page contains 'password' - is store password protected?")

# Look for sections
sections = soup.find_all(lambda t: t.get('id', '').startswith('shopify-section-'))
print(f"Total sections: {len(sections)}")
for s in sections:
    print(f"  - {s.get('id')}")
