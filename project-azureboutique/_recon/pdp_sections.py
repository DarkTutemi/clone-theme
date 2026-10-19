from bs4 import BeautifulSoup
import re

path = r'C:\Users\vdvie\.gemini\antigravity-ide\brain\1b0221d5-22c1-41e9-89c1-c87b8ede21af\.system_generated\steps\519\content.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')
sections = soup.find_all(lambda tag: tag.get('id', '').startswith('shopify-section-'))
print(f"Total shopify sections on PDP: {len(sections)}")
for s in sections:
    s_id = s.get('id')
    print(f"  {s_id} (tag={s.name})")
