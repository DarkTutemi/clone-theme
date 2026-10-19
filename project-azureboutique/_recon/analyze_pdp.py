from bs4 import BeautifulSoup

path = r'C:\Users\vdvie\.gemini\antigravity-ide\brain\1b0221d5-22c1-41e9-89c1-c87b8ede21af\.system_generated\steps\519\content.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')
main = soup.find('main', id='MainContent')
if main:
    sections = [c for c in main.children if getattr(c, 'name', None) == 'section' or (getattr(c, 'name', None) == 'div' and 'shopify-section' in c.get('class', []))]
    print(f"Total sections in PDP main: {len(sections)}")
    for idx, s in enumerate(sections):
        s_id = s.get('id')
        headings = [h.get_text(strip=True) for h in s.find_all(['h1', 'h2', 'h3'])]
        print(f"Section {idx}: ID={s_id} | Headings={headings}")
else:
    print("No main tag found")
