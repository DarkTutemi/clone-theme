controller_js = """
<!-- Arctic 2.0 Swatch & Gallery Interactive Controller -->
<script id="arctic-pdp-controller">
(function() {
  function initArcticPDP() {
    const thumbs = Array.from(document.querySelectorAll('.product__thumbnail-item'));
    const swatches = Array.from(document.querySelectorAll('.variant-swatch'));
    const colorValSpan = document.querySelector('.product-form__option-value');
    const stickyColorSelect = document.querySelector('.product-sticky-form select[name="option1"]');

    if (!thumbs.length || !swatches.length) {
      setTimeout(initArcticPDP, 150);
      return;
    }

    function cleanName(url) {
      if (!url) return '';
      return url.split('?')[0].split('/').pop().replace(/_\\d+x/g, '').split('.')[0];
    }

    // 1. Swatch Click Handler
    swatches.forEach(sw => {
      sw.style.cursor = 'pointer';
      sw.addEventListener('click', function(e) {
        // Mark active swatch
        swatches.forEach(s => {
          s.classList.remove('is-active');
          const l = s.querySelector('.variant-swatch__item');
          if (l) {
            l.style.boxShadow = 'none';
            l.style.borderColor = 'rgba(0,0,0,0.12)';
          }
        });
        sw.classList.add('is-active');
        const activeLabel = sw.querySelector('.variant-swatch__item');
        if (activeLabel) {
          activeLabel.style.boxShadow = '0 0 0 2px #08435e';
          activeLabel.style.borderColor = '#08435e';
        }
        const inp = sw.querySelector('input');
        if (inp) inp.checked = true;

        const colorName = (inp ? inp.value : sw.innerText).trim();
        if (colorValSpan) colorValSpan.innerText = colorName;
        if (stickyColorSelect) stickyColorSelect.value = colorName;

        // Find matching thumbnail and click it to trigger native Flickity carousel navigation
        const sImg = sw.querySelector('img');
        if (sImg) {
          const sBase = cleanName(sImg.src);
          const targetThumb = thumbs.find(t => {
            const tImg = t.querySelector('img');
            return tImg && cleanName(tImg.src) === sBase;
          });
          if (targetThumb) {
            targetThumb.click();
          }
        }
      });
    });

    // 2. Thumbnail Click Handler (Sync matching swatch)
    thumbs.forEach(t => {
      t.addEventListener('click', function() {
        const tImg = t.querySelector('img');
        if (!tImg) return;
        const tBase = cleanName(tImg.src);
        const matchingSwatch = swatches.find(sw => {
          const sImg = sw.querySelector('img');
          return sImg && cleanName(sImg.src) === tBase;
        });
        if (matchingSwatch && !matchingSwatch.classList.contains('is-active')) {
          swatches.forEach(s => {
            s.classList.remove('is-active');
            const l = s.querySelector('.variant-swatch__item');
            if (l) {
              l.style.boxShadow = 'none';
              l.style.borderColor = 'rgba(0,0,0,0.12)';
            }
          });
          matchingSwatch.classList.add('is-active');
          const activeLabel = matchingSwatch.querySelector('.variant-swatch__item');
          if (activeLabel) {
            activeLabel.style.boxShadow = '0 0 0 2px #08435e';
            activeLabel.style.borderColor = '#08435e';
          }
          const inp = matchingSwatch.querySelector('input');
          if (inp) inp.checked = true;
          const colorName = (inp ? inp.value : matchingSwatch.innerText).trim();
          if (colorValSpan) colorValSpan.innerText = colorName;
          if (stickyColorSelect) stickyColorSelect.value = colorName;
        }
      });
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initArcticPDP);
  } else {
    setTimeout(initArcticPDP, 100);
  }
})();
</script>
"""

with open('f:/clone-theme/project-trybronoir/bridge/product_arctic.html', 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Remove any old controller if present
if 'id="arctic-pdp-controller"' in content:
    import re
    content = re.sub(r'<!-- Arctic 2\.0 Swatch.*?<\/script>', '', content, flags=re.DOTALL)

# Inject before </body>
insert_pos = content.rfind('</body>')
if insert_pos != -1:
    content = content[:insert_pos] + controller_js + '\n' + content[insert_pos:]
    with open('f:/clone-theme/project-trybronoir/bridge/product_arctic.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Injected arctic-pdp-controller into product_arctic.html")
else:
    print("Could not find </body>")
