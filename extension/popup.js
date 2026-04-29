fetch('http://127.0.0.1:8005/audio/')
  .then(() => {
    const statusText = document.getElementById('status-text');
    if (statusText) {
      statusText.innerText = 'Online ✅';
      statusText.className = 'status-online';
    }
  })
  .catch(() => {
    const statusText = document.getElementById('status-text');
    if (statusText) {
      statusText.innerText = 'Offline ❌ (Start server.py)';
      statusText.className = 'status-offline';
    }
  });
