// Theme Inspector Content Script — Design Bridge
(function () {
  'use strict';

  if (window.__SHOPIFY_THEME_INSPECTOR_LOADED__) return;
  window.__SHOPIFY_THEME_INSPECTOR_LOADED__ = true;

  let isInspectMode = false;
  let hoveredElement = null;
  let selectedElement = null;
  let bridgeServerUrl = 'http://localhost:4000';

  // Create UI overlay container
  const overlayContainer = document.createElement('div');
  overlayContainer.id = 'theme-inspector-root';
  overlayContainer.innerHTML = `
    <div id="ti-highlight-box" class="ti-hidden">
      <div id="ti-highlight-badge"></div>
    </div>
    <div id="ti-modal" class="ti-hidden">
      <div class="ti-modal-header">
        <div class="ti-modal-title">
          <span class="ti-indicator"></span>
          <span>Theme Inspector — AI Bridge</span>
        </div>
        <button id="ti-modal-close" title="Đóng (Esc)">✕</button>
      </div>
      <div class="ti-modal-body">
        <div class="ti-meta-grid">
          <div class="ti-meta-item">
            <span class="ti-meta-label">File nguồn (Liquid):</span>
            <span id="ti-meta-file" class="ti-meta-val ti-highlight-green">Đang phát hiện...</span>
          </div>
          <div class="ti-meta-item">
            <span class="ti-meta-label">DOM Selector:</span>
            <span id="ti-meta-selector" class="ti-meta-val">div > p</span>
          </div>
          <div class="ti-meta-item ti-col-span-2">
            <span class="ti-meta-label">Nội dung text hiện tại:</span>
            <div id="ti-meta-text" class="ti-text-preview">...</div>
          </div>
        </div>

        <div class="ti-input-group">
          <label for="ti-user-prompt">Yêu cầu chỉnh sửa của ông chủ:</label>
          <textarea id="ti-user-prompt" placeholder="Ví dụ: Đổi màu chữ thành trắng, nền xanh lục #44624a, bo tròn góc 8px và tăng kích thước chữ lên 18px..."></textarea>
        </div>

        <div id="ti-status-msg" class="ti-status-msg ti-hidden"></div>

        <div class="ti-modal-actions">
          <button id="ti-btn-send" class="ti-btn ti-btn-primary">
            <span>🚀 Gửi cho AI Agent</span>
          </button>
          <button id="ti-btn-copy" class="ti-btn ti-btn-secondary">
            <span>📋 Copy Prompt</span>
          </button>
          <button id="ti-btn-cancel" class="ti-btn ti-btn-ghost">Hủy</button>
        </div>
      </div>
    </div>

    <!-- Floating Toggle Button on Page -->
    <div id="ti-floating-trigger" title="Bật/Tắt chế độ chỉ định phần tử (Alt + I)">
      <span class="ti-trigger-icon">🎯</span>
      <span class="ti-trigger-text">Inspect DOM</span>
    </div>
  `;
  document.documentElement.appendChild(overlayContainer);

  const highlightBox = document.getElementById('ti-highlight-box');
  const highlightBadge = document.getElementById('ti-highlight-badge');
  const modal = document.getElementById('ti-modal');
  const modalClose = document.getElementById('ti-modal-close');
  const modalCancel = document.getElementById('ti-btn-cancel');
  const btnSend = document.getElementById('ti-btn-send');
  const btnCopy = document.getElementById('ti-btn-copy');
  const metaFile = document.getElementById('ti-meta-file');
  const metaSelector = document.getElementById('ti-meta-selector');
  const metaText = document.getElementById('ti-meta-text');
  const userPromptInput = document.getElementById('ti-user-prompt');
  const statusMsg = document.getElementById('ti-status-msg');
  const floatingTrigger = document.getElementById('ti-floating-trigger');

  // Toggle Inspect Mode
  function setInspectMode(active) {
    isInspectMode = active;
    if (isInspectMode) {
      document.body.classList.add('ti-inspect-active');
      floatingTrigger.classList.add('ti-active');
      floatingTrigger.querySelector('.ti-trigger-text').textContent = 'Đang Inspect (Alt+I)';
      showStatusNotice('🎯 Chế độ Inspect đã BẬT. Di chuột và click vào phần tử muốn sửa!');
    } else {
      document.body.classList.remove('ti-inspect-active');
      floatingTrigger.classList.remove('ti-active');
      floatingTrigger.querySelector('.ti-trigger-text').textContent = 'Inspect DOM';
      hideHighlight();
    }
  }

  function toggleInspectMode() {
    setInspectMode(!isInspectMode);
  }

  floatingTrigger.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleInspectMode();
  });

  // Hotkey Alt + I to toggle
  window.addEventListener('keydown', (e) => {
    if (e.altKey && (e.key === 'i' || e.key === 'I')) {
      e.preventDefault();
      toggleInspectMode();
    }
    if (e.key === 'Escape' && isInspectMode) {
      if (!modal.classList.contains('ti-hidden')) {
        closeModal();
      } else {
        setInspectMode(false);
      }
    }
  });

  // Compute CSS Selector
  function getCssSelector(el) {
    if (!el || el.nodeType !== Node.ELEMENT_NODE) return '';
    if (el.id) return '#' + CSS.escape(el.id);

    let path = [];
    while (el && el.nodeType === Node.ELEMENT_NODE) {
      let selector = el.nodeName.toLowerCase();
      if (el.id) {
        selector += '#' + CSS.escape(el.id);
        path.unshift(selector);
        break;
      } else {
        let sibling = el;
        let nth = 1;
        while ((sibling = sibling.previousElementSibling)) {
          if (sibling.nodeName.toLowerCase() === selector) nth++;
        }
        if (nth > 1) selector += `:nth-of-type(${nth})`;
      }
      path.unshift(selector);
      el = el.parentElement;
      if (path.length >= 4) break; // keep selector concise
    }
    return path.join(' > ');
  }

  // Detect Traceable Liquid Section / Snippet
  function detectSourceFile(el) {
    let current = el;
    while (current && current !== document.documentElement) {
      if (current.dataset && current.dataset.src) {
        return current.dataset.src;
      }
      if (current.dataset && current.dataset.sectionId) {
        return `sections/${current.dataset.sectionId}.liquid`;
      }
      if (current.id && current.id.startsWith('shopify-section-')) {
        const secName = current.id.replace('shopify-section-', '');
        return `sections/${secName}.liquid`;
      }
      // Check class hints
      if (current.className && typeof current.className === 'string') {
        if (current.className.includes('hero-banner') || current.className.includes('banner')) return 'sections/hero-banner.liquid';
        if (current.className.includes('header') || current.className.includes('navbar')) return 'sections/header.liquid';
        if (current.className.includes('footer')) return 'sections/footer.liquid';
        if (current.className.includes('product-card') || current.className.includes('card-product')) return 'snippets/product-card.liquid';
        if (current.className.includes('featured-collection') || current.className.includes('collection-grid')) return 'sections/featured-collection.liquid';
        if (current.className.includes('rich-text')) return 'sections/rich-text.liquid';
      }
      current = current.parentElement;
    }
    return 'assets/base.css / main-page.liquid';
  }

  // Highlight Position Update
  function updateHighlight(el) {
    if (!el || el === overlayContainer || overlayContainer.contains(el)) {
      hideHighlight();
      return;
    }
    const rect = el.getBoundingClientRect();
    highlightBox.style.top = `${rect.top + window.scrollY}px`;
    highlightBox.style.left = `${rect.left + window.scrollX}px`;
    highlightBox.style.width = `${rect.width}px`;
    highlightBox.style.height = `${rect.height}px`;

    const tag = el.tagName.toLowerCase();
    const cls = el.className && typeof el.className === 'string' ? '.' + el.className.trim().split(/\s+/).slice(0, 2).join('.') : '';
    const src = detectSourceFile(el);
    highlightBadge.textContent = `<${tag}${cls}> ⟶ [${src}]`;
    highlightBox.classList.remove('ti-hidden');
  }

  function hideHighlight() {
    highlightBox.classList.add('ti-hidden');
  }

  // Mousemove for Inspect Mode
  document.addEventListener(
    'mousemove',
    (e) => {
      if (!isInspectMode || !modal.classList.contains('ti-hidden')) return;
      const target = e.target;
      if (target === overlayContainer || overlayContainer.contains(target)) return;
      hoveredElement = target;
      updateHighlight(target);
    },
    true
  );

  // Click on Element to Inspect
  document.addEventListener(
    'click',
    (e) => {
      if (!isInspectMode) return;
      const target = e.target;
      if (target === overlayContainer || overlayContainer.contains(target)) return;

      e.preventDefault();
      e.stopPropagation();

      selectedElement = target;
      openModal(target);
    },
    true
  );

  function openModal(el) {
    const selector = getCssSelector(el);
    const sourceFile = detectSourceFile(el);
    const textSnippet = (el.innerText || el.textContent || '').trim().slice(0, 150) || '(Phần tử không chứa text trực tiếp)';

    metaSelector.textContent = selector;
    metaFile.textContent = sourceFile;
    metaText.textContent = textSnippet;
    userPromptInput.value = '';
    statusMsg.classList.add('ti-hidden');

    // Position modal near element if possible, or center
    const rect = el.getBoundingClientRect();
    let top = rect.bottom + window.scrollY + 10;
    let left = Math.max(20, Math.min(window.innerWidth - 480, rect.left + window.scrollX));

    if (rect.bottom + 380 > window.innerHeight) {
      top = Math.max(20, rect.top + window.scrollY - 360);
    }

    modal.style.top = `${top}px`;
    modal.style.left = `${left}px`;
    modal.classList.remove('ti-hidden');
    userPromptInput.focus();
  }

  function closeModal() {
    modal.classList.add('ti-hidden');
    selectedElement = null;
    hideHighlight();
  }

  modalClose.addEventListener('click', closeModal);
  modalCancel.addEventListener('click', closeModal);

  // Extract Element Context Data
  function getElementContext(el, prompt) {
    const computed = window.getComputedStyle(el);
    return {
      prompt: prompt,
      page_url: window.location.href,
      target: {
        tag: el.tagName.toLowerCase(),
        classes: el.className || '',
        id: el.id || '',
        selector: getCssSelector(el),
        source_file: detectSourceFile(el),
        text_content: (el.innerText || el.textContent || '').trim().slice(0, 300),
        html_snippet: el.outerHTML ? el.outerHTML.slice(0, 400) : ''
      },
      styles: {
        color: computed.color,
        backgroundColor: computed.backgroundColor,
        fontSize: computed.fontSize,
        fontWeight: computed.fontWeight,
        padding: computed.padding,
        margin: computed.margin,
        display: computed.display
      },
      timestamp: new Date().toISOString()
    };
  }

  // Format prompt for clipboard
  function generateFormattedPrompt(context) {
    return `[N] Sửa phần tử giao diện theo yêu cầu của ông chủ:
**File mục tiêu:** \`${context.target.source_file}\`
**Selector:** \`${context.target.selector}\`
**Thẻ HTML:** \`<${context.target.tag}>\`
**Nội dung hiện tại:** "${context.target.text_content}"

**Yêu cầu chỉnh sửa:**
${context.prompt}

**Thông tin Style hiện tại:**
- Font size: ${context.styles.fontSize} | Color: ${context.styles.color}
- Background: ${context.styles.backgroundColor} | Padding: ${context.styles.padding}
- URL trang: ${context.page_url}`;
  }

  // Send Ticket to Agent via Background Service Worker or Localhost Bridge
  btnSend.addEventListener('click', async () => {
    const prompt = userPromptInput.value.trim();
    if (!prompt) {
      showStatus('Vui lòng nhập yêu cầu chỉnh sửa của ông chủ!', 'error');
      return;
    }
    if (!selectedElement) return;

    const ticketData = getElementContext(selectedElement, prompt);
    showStatus('⏳ Đang gửi yêu cầu tới AI Agent...', 'info');

    // Method 1: Try via extension background worker (avoids Mixed Content on HTTPS Shopify pages)
    if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.sendMessage) {
      chrome.runtime.sendMessage({ action: 'sendTicket', data: ticketData }, async (response) => {
        if (chrome.runtime.lastError || !response || !response.ok) {
          // Fallback to direct fetch
          sendViaDirectFetch(ticketData);
        } else {
          showStatus(`✅ Đã gửi ticket #${response.data.id} tới AI Agent thành công! Agent đang xử lý...`, 'success');
          setTimeout(() => {
            closeModal();
            setInspectMode(false);
          }, 1800);
        }
      });
      return;
    }

    // Method 2: Direct fetch fallback (for localhost)
    sendViaDirectFetch(ticketData);
  });

  async function sendViaDirectFetch(ticketData) {
    try {
      const response = await fetch(`${bridgeServerUrl}/ticket`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(ticketData)
      });

      if (!response.ok) throw new Error(`HTTP error ${response.status}`);
      const res = await response.json();

      showStatus(`✅ Đã gửi ticket #${res.id} tới AI Agent thành công! Agent đang xử lý...`, 'success');
      setTimeout(() => {
        closeModal();
        setInspectMode(false);
      }, 1800);
    } catch (err) {
      console.warn('Bridge server error:', err);
      // Fallback: Copy to clipboard if server offline
      const promptText = generateFormattedPrompt(ticketData);
      navigator.clipboard.writeText(promptText);
      showStatus('⚠️ Bridge server chưa kết nối, nhưng đã tự động COPY PROMPT vào clipboard cho ông chủ!', 'warning');
    }
  }

  // Copy Prompt directly to Clipboard
  btnCopy.addEventListener('click', () => {
    const prompt = userPromptInput.value.trim();
    if (!selectedElement) return;
    const ticketData = getElementContext(selectedElement, prompt || '(Chưa nhập chi tiết, sửa theo selector)');
    const promptText = generateFormattedPrompt(ticketData);

    navigator.clipboard.writeText(promptText).then(() => {
      showStatus('📋 Đã copy prompt đầy đủ context vào Clipboard! Ông chủ chỉ cần dán (Ctrl+V) vào chat với Antigravity.', 'success');
      setTimeout(() => {
        closeModal();
      }, 1600);
    });
  });

  function showStatus(msg, type) {
    statusMsg.textContent = msg;
    statusMsg.className = `ti-status-msg ti-${type}`;
    statusMsg.classList.remove('ti-hidden');
  }

  function showStatusNotice(msg) {
    const notice = document.createElement('div');
    notice.className = 'ti-toast-notice';
    notice.textContent = msg;
    document.body.appendChild(notice);
    setTimeout(() => {
      notice.style.opacity = '0';
      notice.style.transform = 'translateY(-10px)';
      setTimeout(() => notice.remove(), 400);
    }, 2500);
  }

  // Listen to messages from extension popup
  if (typeof chrome !== 'undefined' && chrome.runtime && chrome.runtime.onMessage) {
    chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
      if (request.action === 'toggleInspect') {
        toggleInspectMode();
        sendResponse({ active: isInspectMode });
      } else if (request.action === 'getInspectState') {
        sendResponse({ active: isInspectMode });
      }
    });
  }

  console.log('🚀 Theme Inspector Extension loaded. Press Alt+I or click the 🎯 button at bottom-right to inspect.');
})();
