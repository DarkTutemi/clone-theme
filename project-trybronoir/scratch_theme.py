import urllib.request
import re

content = urllib.request.urlopen('https://trybronoir.com/cdn/shop/t/20/assets/theme.js?v=42546318628993233181791218588').read().decode('utf-8', errors='ignore')

matches = [m.start() for m in re.finditer(r'aria-controls', content)]
print('Matches for aria-controls:', len(matches))
for pos in matches:
    print('--- MATCH ---')
    print(content[max(0, pos-100):min(len(content), pos+200)])
