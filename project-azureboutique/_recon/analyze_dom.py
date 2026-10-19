import re
import json

path = r'C:\Users\vdvie\.gemini\antigravity-ide\brain\1b0221d5-22c1-41e9-89c1-c87b8ede21af\.system_generated\steps\481\content.md'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Find all section divs
sections = re.findall(r'<div id="(shopify-section-[^"]+)" class="([^"]+)"', text)
results = []
for s_id, s_cls in sections:
    results.append({'id': s_id, 'class': s_cls})
    print(f"Section: {s_id} | Class: {s_cls}")

# Also find comments like <!-- BEGIN sections: ... -->
comments = re.findall(r'<!-- (BEGIN|END) (?:sections|section):? ([^>]+) -->', text)
for c in comments:
    print(f"Comment: {c}")

with open(r'f:\clone-theme\project-azureboutique\_recon\sections-extracted.json', 'w', encoding='utf-8') as out:
    json.dump({'sections': results, 'comments': comments}, out, indent=2)
