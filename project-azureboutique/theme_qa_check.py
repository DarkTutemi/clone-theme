import os
import json
import re

theme_dir = r'f:\clone-theme\project-azureboutique\theme'

errors = []
warnings = []

# 1. Validate all JSON files
json_files = []
for root, dirs, files in os.walk(theme_dir):
    for f in files:
        if f.endswith('.json'):
            json_files.append(os.path.join(root, f))

for jf in json_files:
    rel = os.path.relpath(jf, theme_dir)
    try:
        with open(jf, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Check section references in templates and groups
        if 'sections' in data:
            for s_key, s_val in data['sections'].items():
                s_type = s_val.get('type')
                if s_type:
                    sec_file = os.path.join(theme_dir, 'sections', f"{s_type}.liquid")
                    if not os.path.exists(sec_file):
                        errors.append(f"Missing section file: {sec_file} referenced in {rel} (section: {s_key})")
    except Exception as e:
        errors.append(f"Invalid JSON in {rel}: {e}")

# 2. Check Liquid files for balanced tags and schema validity
liquid_files = []
for root, dirs, files in os.walk(theme_dir):
    for f in files:
        if f.endswith('.liquid'):
            liquid_files.append(os.path.join(root, f))

for lf in liquid_files:
    rel = os.path.relpath(lf, theme_dir)
    with open(lf, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    # Check schema tag
    if '{% schema %}' in content:
        schema_match = re.search(r'\{%\s*schema\s*%\}(.*?)\{%\s*endschema\s*%\}', content, re.DOTALL)
        if schema_match:
            raw_schema = schema_match.group(1).strip()
            try:
                json.loads(raw_schema)
            except Exception as e:
                errors.append(f"Invalid schema JSON in {rel}: {e}")
        else:
            errors.append(f"Unclosed schema tag in {rel}")

    # Check for basic unbalanced liquid tags
    for tag in ['if', 'for', 'form', 'paginate']:
        open_count = len(re.findall(rf'\{{%\s*{tag}\b', content))
        close_count = len(re.findall(rf'\{{%\s*end{tag}\b', content))
        if open_count != close_count:
            errors.append(f"Unbalanced '{tag}' tag in {rel}: {open_count} open vs {close_count} close")

print(f"QA Results: {len(liquid_files)} Liquid files, {len(json_files)} JSON files checked.")
if errors:
    print(f"FAILED with {len(errors)} errors:")
    for err in errors:
        print(f"  [ERROR] {err}")
else:
    print("SUCCESS: All Liquid and JSON files passed validation with 0 errors!")

if warnings:
    for w in warnings:
        print(f"  [WARN] {w}")
