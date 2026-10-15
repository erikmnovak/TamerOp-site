(() => {
  'use strict';
  const selector = '.prepared-example iframe';

  window.addEventListener('message', event => {
    const message = event.data;
    if (event.origin !== 'null' || !message ||
        message.type !== 'tamerop:prepared-viewer-height' ||
        typeof message.height !== 'number' || !Number.isFinite(message.height) ||
        message.height < 100 || message.height > 20000) return;
    const frame = Array.from(document.querySelectorAll(selector)).find(
      candidate => candidate.contentWindow === event.source);
    if (!frame) return;
    const style = getComputedStyle(frame);
    const borders = style.boxSizing === 'border-box'
      ? parseFloat(style.borderTopWidth) + parseFloat(style.borderBottomWidth) : 0;
    const height = Math.ceil(message.height + borders) + 'px';
    if (frame.style.height !== height) frame.style.height = height;
  });

  function requestHeight(frame) {
    if (!frame.matches || !frame.matches(selector) || !frame.contentWindow) return;
    // A sandbox without allow-same-origin has an opaque origin. The request
    // carries no data; the reply is accepted only from this exact frame.
    frame.contentWindow.postMessage({type: 'tamerop:prepared-viewer-measure'}, '*');
  }
  document.addEventListener('load', event => requestHeight(event.target), true);
  const measureExisting = () => document.querySelectorAll(selector).forEach(requestHeight);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', measureExisting);
  else measureExisting();
})();
