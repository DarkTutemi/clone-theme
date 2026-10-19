"""
Single Section HTML-to-Liquid Converter
Transforms raw HTML snippets or competitor sections into modular Shopify Liquid sections with editable schema.
"""
import re
import json
from bs4 import BeautifulSoup

def convert_html_to_liquid_section(html: str, section_name: str, section_title: str = None) -> str:
    soup = BeautifulSoup(html, "html.parser")
    if not section_title:
        section_title = section_name.replace("-", " ").replace("_", " ").title()

    # Detect editable texts (headings, buttons, paragraphs)
    schema_settings = []
    
    # Check main heading
    h_tag = soup.find(["h1", "h2", "h3"])
    if h_tag and h_tag.string:
        default_heading = h_tag.string.strip()
        schema_settings.append({
            "type": "text",
            "id": "heading",
            "label": "Heading Text",
            "default": default_heading
        })
        h_tag.string = "{{ section.settings.heading }}"

    # Check button
    btn_tag = soup.find(["a", "button"], class_=re.compile(r"btn|button", re.I))
    if btn_tag and btn_tag.string:
        default_btn = btn_tag.string.strip()
        schema_settings.append({
            "type": "text",
            "id": "button_label",
            "label": "Button Label",
            "default": default_btn
        })
        schema_settings.append({
            "type": "url",
            "id": "button_link",
            "label": "Button Link"
        })
        btn_tag.string = "{{ section.settings.button_label }}"
        if btn_tag.name == "a":
            btn_tag["href"] = "{{ section.settings.button_link }}"

    schema = {
        "name": section_title,
        "tag": "section",
        "class": f"section-{section_name}",
        "settings": schema_settings,
        "presets": [
            {
                "name": section_title
            }
        ]
    }

    liquid_output = f"""{{% comment %}}
  Section: {section_title}
  Converted by Antigravity Shopify Engine
{{% endcomment %}}

<div id="{section_name}-section" class="shopify-section-wrapper">
{soup.prettify()}
</div>

{{% schema %}}
{json.dumps(schema, indent=2)}
{{% endschema %}}
"""
    return liquid_output
