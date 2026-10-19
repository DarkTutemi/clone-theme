#!/usr/bin/env python
"""
Visual Diff & DOM Inspector Suite for Shopify Clone Theme Verification
Automates headless browser capture, side-by-side visual comparison, and DOM style extraction.
"""
import os
import sys
import subprocess
import json
import argparse
from urllib.parse import urlparse
from bs4 import BeautifulSoup

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

def get_browser_path():
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    return "chrome"

def capture_screenshot(url: str, output_path: str, width: int = 1440, height: int = 900, wait_ms: int = 4000) -> bool:
    """Takes a screenshot of the given URL using headless Chrome."""
    browser = get_browser_path()
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    
    cmd = [
        browser,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        f"--virtual-time-budget={wait_ms}",
        f"--window-size={width},{height}",
        f"--screenshot={output_path}",
        url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return os.path.exists(output_path) and os.path.getsize(output_path) > 1000
    except Exception as e:
        print(f"[-] Capture failed: {e}", file=sys.stderr)
        return False

def dump_rendered_dom(url: str, wait_ms: int = 4000) -> str:
    """Dumps the full rendered DOM after JS execution."""
    browser = get_browser_path()
    cmd = [
        browser,
        "--headless=new",
        "--no-sandbox",
        "--disable-gpu",
        f"--virtual-time-budget={wait_ms}",
        "--dump-dom",
        url
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=35, encoding="utf-8", errors="replace")
        return res.stdout
    except Exception as e:
        print(f"[-] DOM dump failed: {e}", file=sys.stderr)
        return ""

def inspect_dom_element(url: str, selector: str) -> dict:
    """Finds an element in the rendered DOM and extracts tag, attributes, classes, inline styles, images, and text."""
    html = dump_rendered_dom(url)
    if not html:
        return {"error": "Could not fetch rendered DOM"}
    
    soup = BeautifulSoup(html, "html.parser")
    element = soup.select_one(selector)
    if not element:
        return {
            "found": False,
            "selector": selector,
            "message": f"Element matching selector '{selector}' was not found in rendered DOM."
        }
    
    # Extract images inside element
    images = []
    for img in element.find_all("img"):
        src = img.get("src") or img.get("data-src") or img.get("srcset")
        if src:
            images.append({
                "src": src,
                "alt": img.get("alt", ""),
                "class": img.get("class", [])
            })
            
    # Extract all child text snippets
    text_content = element.get_text(separator="\n", strip=True)
    
    return {
        "found": True,
        "selector": selector,
        "tag": element.name,
        "classes": element.get("class", []),
        "id": element.get("id", ""),
        "style": element.get("style", ""),
        "attributes": dict(element.attrs),
        "text_content": text_content[:500],
        "image_count": len(images),
        "images": images[:10],
        "outer_html": str(element)[:2000]
    }

def run_visual_verification(target_url: str, clone_url: str, output_dir: str) -> dict:
    """
    Captures side-by-side screenshots of target site vs clone site
    for Desktop (1440x900) and Mobile (375x812).
    """
    os.makedirs(output_dir, exist_ok=True)
    results = {
        "target_url": target_url,
        "clone_url": clone_url,
        "captures": {}
    }
    
    viewports = [
        ("desktop", 1440, 900),
        ("mobile", 375, 812),
        ("desktop_tall", 1440, 2500)
    ]
    
    for name, w, h in viewports:
        target_img = os.path.join(output_dir, f"target_{name}.png")
        clone_img = os.path.join(output_dir, f"clone_{name}.png")
        
        print(f"[*] Capturing {name} ({w}x{h})...")
        t_ok = capture_screenshot(target_url, target_img, width=w, height=h)
        c_ok = capture_screenshot(clone_url, clone_img, width=w, height=h)
        
        results["captures"][name] = {
            "target": target_img if t_ok else None,
            "clone": clone_img if c_ok else None,
            "target_size_bytes": os.path.getsize(target_img) if t_ok else 0,
            "clone_size_bytes": os.path.getsize(clone_img) if c_ok else 0
        }
        
    report_file = os.path.join(output_dir, "visual_verification_report.json")
    with open(report_file, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print(f"[+] Visual verification complete. Report: {report_file}")
    return results

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visual Diff & DOM Inspector")
    sub = parser.add_subparsers(dest="cmd", required=True)
    
    p_comp = sub.add_parser("compare", help="Compare target vs clone visuals")
    p_comp.add_argument("--target", required=True, help="Competitor target URL")
    p_comp.add_argument("--clone", required=True, help="Cloned store or preview URL")
    p_comp.add_argument("--out", default="./visual_diff", help="Output directory")
    
    p_dom = sub.add_parser("inspect", help="Inspect element in rendered DOM of target")
    p_dom.add_argument("--url", required=True, help="Page URL")
    p_dom.add_argument("--selector", required=True, help="CSS Selector")
    
    args = parser.parse_args()
    if args.cmd == "compare":
        run_visual_verification(args.target, args.clone, args.out)
    elif args.cmd == "inspect":
        res = inspect_dom_element(args.url, args.selector)
        print(json.dumps(res, indent=2, ensure_ascii=False))
