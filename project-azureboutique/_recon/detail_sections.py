from bs4 import BeautifulSoup

path = r'C:\Users\vdvie\.gemini\antigravity-ide\brain\1b0221d5-22c1-41e9-89c1-c87b8ede21af\.system_generated\steps\481\content.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')
main = soup.find('main', id='MainContent')
sections = [c for c in main.children if getattr(c, 'name', None) == 'section']

for idx, s in enumerate(sections):
    print(f"\n================ SECTION {idx} ================")
    print(f"ID: {s.get('id')}")
    print(f"Class: {s.get('class')}")
    # Headings
    headings = [h.get_text(strip=True) for h in s.find_all(['h1', 'h2', 'h3', 'h4'])]
    print(f"Headings: {headings}")
    # Links
    links = [(a.get_text(strip=True), a.get('href')) for a in s.find_all('a') if a.get_text(strip=True)]
    print(f"Links ({len(links)}): {links[:5]}")
    # Images
    imgs = [img.get('src') or img.get('data-src') for img in s.find_all('img')]
    print(f"Images count: {len(imgs)}, sample: {imgs[:3]}")
    # Text snippet
    print(f"Text sample: {s.get_text(separator=' ', strip=True)[:300]}")
