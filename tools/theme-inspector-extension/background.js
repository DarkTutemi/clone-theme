// Theme Inspector Extension — Background Service Worker
// Solves Mixed Content blocking: enables HTTPS pages to send tickets to http://localhost:4000 without browser security restrictions.

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'sendTicket') {
    const bridgeUrl = 'http://localhost:4000/ticket';

    fetch(bridgeUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(request.data)
    })
      .then(async (res) => {
        if (!res.ok) {
          throw new Error(`HTTP ${res.status}: ${res.statusText}`);
        }
        return res.json();
      })
      .then((data) => {
        console.log('[Background] Ticket sent successfully:', data);
        sendResponse({ ok: true, data: data });
      })
      .catch((err) => {
        console.warn('[Background] Failed to send ticket to bridge:', err);
        sendResponse({ ok: false, error: err.message });
      });

    return true; // Keep message channel open for asynchronous response
  }
});
