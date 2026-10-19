import re
from bs4 import BeautifulSoup

path = r'C:\Users\vdvie\.gemini\antigravity-ide\brain\1b0221d5-22c1-41e9-89c1-c87b8ede21af\.system_generated\steps\481\content.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

soup = BeautifulSoup(text, 'html.parser')

main = soup.find('main', id='MainContent')
if main:
    print("Found <main id='MainContent'>")
    # list top-level children of main
    children = [c for c in main.children if getattr(c, 'name', None)]
    for idx, c in enumerate(children):
        print(f"Child {idx}: tag={c.name}, id={c.get('id', '')}, class={c.get('class', [])}")
        # if section or div with section in class
        sub_sections = c.find_all('section')
        if sub_sections:
            for s in sub_sections:
                print(f"  -> sub <section>: id={s.get('id', '')}, class={s.get('class', [])}")
else:
    print("No <main id='MainContent'> found! Searching for main tags...")
    m = soup.find_all('main')
    print(f"Total <main> tags: {len(m)}")
    for item in m:
        print(item.get('id'), item.get('class'))
