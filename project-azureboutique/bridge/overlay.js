(() => {
  let picking = false, hovered = null;
  const box = document.createElement('div');
  box.style.cssText = 'position:fixed;outline:2px solid #ef4444;background:rgba(239,68,68,0.1);pointer-events:none;z-index:99999;transition:all .05s ease;border-radius:4px;';
  
  const panel = document.createElement('div');
  panel.style.cssText = 'position:fixed;right:20px;bottom:20px;z-index:100000;background:#0f172a;color:#f8fafc;padding:16px;border-radius:12px;width:340px;box-shadow:0 10px 25px -5px rgba(0,0,0,0.5);font:14px system-ui;display:none;border:1px solid #334155;';
  panel.innerHTML = `
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;">
      <span style="font-weight:700;color:#38bdf8;font-size:13px;letter-spacing:0.05em;text-transform:uppercase;">Design Bridge</span>
      <span style="font-size:11px;color:#94a3b8;">Alt+I to toggle</span>
    </div>
    <div id="bg-tgt" style="color:#94a3b8;margin-bottom:10px;font-size:12px;word-break:break-all;background:#1e293b;padding:6px 8px;border-radius:6px;"></div>
    <textarea id="bg-intent" rows="3" style="width:100%;box-sizing:border-box;background:#1e293b;border:1px solid #475569;color:#fff;padding:8px;border-radius:6px;outline:none;font-family:inherit;font-size:13px;" placeholder="Yêu cầu sửa (vd: Đổi font sang Playfair, nút màu xanh, thêm bóng...)..."></textarea>
    <div style="display:flex;gap:8px;margin-top:10px;">
      <button id="bg-send" style="flex-grow:1;background:#38bdf8;color:#0f172a;font-weight:700;padding:8px;border-radius:6px;cursor:pointer;border:none;">Gửi cho Agent</button>
      <button id="bg-cancel" style="background:transparent;color:#cbd5e1;padding:8px;border-radius:6px;cursor:pointer;border:1px solid #475569;">Huỷ</button>
    </div>`;
  document.body.append(box, panel);

  function srcOf(el){
    const n = el.closest('[data-src]');
    return {
      source_file: n?.dataset.src || 'UNKNOWN',
      block_id: n?.dataset.block || null
    };
  }

  function sel(el){
    if (el.id) return '#' + el.id;
    const c = [...el.classList].slice(0, 2).join('.');
    return el.tagName.toLowerCase() + (c ? '.' + c : '');
  }

  window.addEventListener('keydown', e => {
    if (e.key === 'i' && e.altKey) {
      picking = !picking;
      document.body.style.cursor = picking ? 'crosshair' : '';
      if (!picking) box.style.width = '0px';
    }
  });

  window.addEventListener('mousemove', e => {
    if (!picking || panel.contains(e.target)) return;
    hovered = e.target;
    const r = hovered.getBoundingClientRect();
    Object.assign(box.style, {
      left: r.left + 'px',
      top: r.top + 'px',
      width: r.width + 'px',
      height: r.height + 'px'
    });
  });

  window.addEventListener('click', e => {
    if (!picking || panel.contains(e.target)) return;
    e.preventDefault();
    e.stopPropagation();
    picking = false;
    document.body.style.cursor = '';
    
    const el = hovered;
    const cs = getComputedStyle(el);
    const s = srcOf(el);
    
    panel.dataset.ticket = JSON.stringify({
      target: {
        ...s,
        selector: sel(el),
        computed_styles: {
          'font-family': cs.fontFamily,
          'color': cs.color,
          'font-size': cs.fontSize,
          'background-color': cs.backgroundColor,
          'padding': cs.padding
        }
      }
    });

    document.getElementById('bg-tgt').textContent = s.source_file + ' → ' + sel(el);
    panel.style.display = 'block';
    document.getElementById('bg-intent').focus();
  }, true);

  document.getElementById('bg-cancel').onclick = () => {
    panel.style.display = 'none';
  };

  document.getElementById('bg-send').onclick = async () => {
    const raw = panel.dataset.ticket;
    if (!raw) return;
    const t = JSON.parse(raw);
    t.intent = document.getElementById('bg-intent').value;
    t.scope = 'this-element';
    t.status = 'pending';
    t.created_at = new Date().toISOString();

    try {
      await fetch('/ticket', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(t)
      });
      panel.style.display = 'none';
      document.getElementById('bg-intent').value = '';
      alert('Đã gửi ticket thành công! Hãy báo agent "xử lý bridge queue".');
    } catch(err) {
      alert('Lỗi gửi ticket: ' + err);
    }
  };
})();
