// Popup JS
document.addEventListener('DOMContentLoaded', async () => {
  const btnToggle = document.getElementById('btn-toggle-inspect');
  const bridgeStatus = document.getElementById('bridge-status');

  // Check localhost:4000
  try {
    const res = await fetch('http://localhost:4000/api/queue', { method: 'GET', cache: 'no-store' });
    if (res.ok) {
      bridgeStatus.textContent = '🟢 Online (:4000)';
      bridgeStatus.style.color = '#10b981';
    } else {
      bridgeStatus.textContent = '🟡 Warning';
      bridgeStatus.style.color = '#f59e0b';
    }
  } catch (e) {
    bridgeStatus.textContent = '🔴 Offline';
    bridgeStatus.style.color = '#ef4444';
  }

  // Check active tab state
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  if (tab && tab.id) {
    try {
      chrome.tabs.sendMessage(tab.id, { action: 'getInspectState' }, (response) => {
        if (chrome.runtime.lastError) return;
        if (response && response.active) {
          btnToggle.classList.add('active');
          btnToggle.innerHTML = '<span>🛑 Tắt Inspect DOM</span>';
        }
      });
    } catch (e) {}
  }

  // Toggle button click
  btnToggle.addEventListener('click', async () => {
    const [activeTab] = await chrome.tabs.query({ active: true, currentWindow: true });
    if (!activeTab || !activeTab.id) return;

    chrome.tabs.sendMessage(activeTab.id, { action: 'toggleInspect' }, (response) => {
      if (chrome.runtime.lastError) {
        alert('Vui lòng tải lại (F5) trang web trước khi bật Inspect!');
        return;
      }
      if (response && response.active) {
        btnToggle.classList.add('active');
        btnToggle.innerHTML = '<span>🛑 Tắt Inspect DOM</span>';
      } else {
        btnToggle.classList.remove('active');
        btnToggle.innerHTML = '<span>🎯 Bật / Tắt Inspect DOM</span>';
      }
      window.close();
    });
  });
});
