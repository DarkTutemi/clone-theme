import urllib.request, re

html = urllib.request.urlopen("https://trybronoir.com/").read().decode("utf-8")
css_urls = re.findall(r'href=[\'"]([^\'"]+\.css[^\'"]*)[\'"]', html)
print("CSS URLs:", len(css_urls))
for u in css_urls:
    if u.startswith("//"): u = "https:" + u
    elif u.startswith("/"): u = "https://trybronoir.com" + u
    try:
        req = urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"})
        css = urllib.request.urlopen(req).read().decode("utf-8", errors="ignore")
        matches = list(re.finditer(r"secondary-image", css))
        if matches:
            print("Found in:", u, "count:", len(matches))
            for m in matches[:3]:
                print("--- CSS MATCH ---")
                print(css[max(0, m.start()-100):min(len(css), m.end()+200)])
    except Exception as e:
        pass
