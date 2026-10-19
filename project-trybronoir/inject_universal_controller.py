import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

BRONOIR_DIR = "f:/clone-theme/project-trybronoir"

universal_js = """
<!-- Universal PDP Swatch & Gallery Interactive Controller -->
<script id="universal-pdp-controller">
(function() {
  function initPDP() {
    const thumbs = Array.from(document.querySelectorAll('.product__thumbnail-item'));
    const swatches = Array.from(document.querySelectorAll('.variant-swatch, .popup-swatch'));
    const colorValSpan = document.querySelector('.product-form__option-value, [id*="-value"]');
    const stickyColorSelect = document.querySelector('.product-sticky-form select[name="option1"]');

    if (!thumbs.length) {
      setTimeout(initPDP, 150);
      return;
    }

    function cleanName(url) {
      if (!url) return '';
      return url.split('?')[0].split('/').pop().replace(/_\\d+x/g, '').split('.')[0];
    }

    // 1. Swatch Click Handler
    if (swatches.length) {
      swatches.forEach((sw, sIdx) => {
        sw.style.cursor = 'pointer';
        sw.addEventListener('click', function(e) {
          // Highlight active swatch
          swatches.forEach(s => {
            s.classList.remove('is-active', 'active');
            const l = s.querySelector('.variant-swatch__item') || s;
            l.style.boxShadow = 'none';
            l.style.borderColor = 'rgba(0,0,0,0.12)';
          });
          sw.classList.add('is-active', 'active');
          const activeLabel = sw.querySelector('.variant-swatch__item') || sw;
          activeLabel.style.boxShadow = '0 0 0 2px #08435e';
          activeLabel.style.borderColor = '#08435e';

          const inp = sw.querySelector('input');
          if (inp) inp.checked = true;

          const colorName = (inp ? inp.value : (sw.getAttribute('data-item') || sw.innerText)).trim();
          if (colorValSpan) colorValSpan.innerText = colorName;
          if (stickyColorSelect) stickyColorSelect.value = colorName;

          // Find target thumbnail by matching base filename
          const sImg = sw.querySelector('img');
          let targetThumb = null;
          if (sImg) {
            const sBase = cleanName(sImg.src);
            targetThumb = thumbs.find(t => {
              const tImg = t.querySelector('img');
              return tImg && cleanName(tImg.src) === sBase;
            });
          }
          // Fallback to index if available
          if (!targetThumb && thumbs[sIdx]) {
            targetThumb = thumbs[sIdx];
          }
          if (targetThumb) {
            targetThumb.click();
          }
        });
      });
    }

    // 2. Thumbnail Click Handler (Highlight active thumbnail & sync swatch)
    thumbs.forEach((t, tIdx) => {
      t.addEventListener('click', function() {
        thumbs.forEach(th => {
          th.classList.remove('is-nav-selected');
          th.removeAttribute('aria-current');
          th.style.outline = 'none';
        });
        t.classList.add('is-nav-selected');
        t.setAttribute('aria-current', 'true');
        t.style.outline = '2px solid #44c2fd';
        t.style.outlineOffset = '2px';
        t.style.borderRadius = '6px';

        const tImg = t.querySelector('img');
        if (!tImg || !swatches.length) return;
        const tBase = cleanName(tImg.src);
        const matchingSwatch = swatches.find(sw => {
          const sImg = sw.querySelector('img');
          return sImg && cleanName(sImg.src) === tBase;
        });
        if (matchingSwatch && !matchingSwatch.classList.contains('is-active')) {
          swatches.forEach(s => {
            s.classList.remove('is-active', 'active');
            const l = s.querySelector('.variant-swatch__item') || s;
            l.style.boxShadow = 'none';
            l.style.borderColor = 'rgba(0,0,0,0.12)';
          });
          matchingSwatch.classList.add('is-active', 'active');
          const activeLabel = matchingSwatch.querySelector('.variant-swatch__item') || matchingSwatch;
          activeLabel.style.boxShadow = '0 0 0 2px #08435e';
          activeLabel.style.borderColor = '#08435e';

          const inp = matchingSwatch.querySelector('input');
          if (inp) inp.checked = true;
          const colorName = (inp ? inp.value : (matchingSwatch.getAttribute('data-item') || matchingSwatch.innerText)).trim();
          if (colorValSpan) colorValSpan.innerText = colorName;
          if (stickyColorSelect) stickyColorSelect.value = colorName;
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPDP);
  } else {
    setTimeout(initPDP, 100);
  }
})();
</script>
"""

target_files = [
    "bridge/product.html",
    "bridge/product_cosycloud.html",
    "bridge/product_arctic.html",
    "bridge/product_toasty.html",
    "bridge/product_trail_masters.html"
]

for tf in target_files:
    full_path = os.path.join(BRONOIR_DIR, tf)
    if not os.path.exists(full_path):
        continue
    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
        c = f.read()

    # Remove any existing controllers
    c = re.sub(r'<!-- Universal PDP Swatch.*?<\/script>', '', c, flags=re.DOTALL)
    c = re.sub(r'<script id="universal-pdp-controller">.*?<\/script>', '', c, flags=re.DOTALL)
    c = re.sub(r'<script id="pdp-interactive-controller">.*?<\/script>', '', c, flags=re.DOTALL)
    c = re.sub(r'<!-- Arctic 2\.0 Swatch.*?<\/script>', '', c, flags=re.DOTALL)

    insert_pos = c.rfind("</body>")
    if insert_pos != -1:
        c = c[:insert_pos] + universal_js + "\n" + c[insert_pos:]
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"✅ Injected updated universal-pdp-controller into {tf}")
    else:
        print(f"❌ No </body> in {tf}")
