console.log("AUREUS X1 V3: Premium Glassmorphism UI Active");

let widget = null;
let statusText = null;
let steps = [];

function createV3Widget() {
    const video = document.querySelector('video');
    if (!video || document.getElementById('aureus-v3-root')) return;

    const container = video.parentElement;
    if (!container) return;

    widget = document.createElement('div');
    widget.id = 'aureus-v3-root';
    widget.className = 'aureus-floating-bar';
    
    widget.innerHTML = `
        <div class="aureus-title">AUREUS X1 PRO</div>
        <div id="aureus-status">Ready to Intercept</div>
        <div class="aureus-stepper">
            <span class="aureus-step" title="Ripping Audio">🎙️</span>
            <span class="aureus-step" title="Transcribing">🧠</span>
            <span class="aureus-step" title="Translating">🌎</span>
            <span class="aureus-step" title="Dubbing">🗣️</span>
        </div>
        <button id="aureus-action-btn" class="aureus-btn-v3">INTERCEPT</button>
    `;

    container.appendChild(widget);
    statusText = widget.querySelector('#aureus-status');
    steps = widget.querySelectorAll('.aureus-step');

    widget.querySelector('#aureus-action-btn').onclick = (e) => {
        const btn = e.target;
        btn.disabled = true;
        btn.innerText = "INITIALIZING...";
        
        // Pause original video
        video.pause();

        chrome.runtime.sendMessage({ 
            type: 'START_INTERCEPT', 
            url: window.location.href 
        });
    };
}

function updateSteps(message) {
    if (!statusText) return;
    statusText.innerText = message;
    
    steps.forEach(s => s.classList.remove('active'));

    // Improved mapping for V3 Statuses
    if (message.toLowerCase().includes("intercepting") || message.toLowerCase().includes("audio")) steps[0].classList.add('active');
    if (message.toLowerCase().includes("transcribing") || message.toLowerCase().includes("whisper")) steps[1].classList.add('active');
    if (message.toLowerCase().includes("translating") || message.toLowerCase().includes("gemini")) steps[2].classList.add('active');
    if (message.toLowerCase().includes("synthesizing") || message.toLowerCase().includes("dub")) steps[3].classList.add('active');
}

chrome.runtime.onMessage.addListener((message) => {
    if (message.type === 'AUREUS_UPDATE') {
        const data = message.data;
        if (data.type === 'status') {
            updateSteps(data.message);
        } else if (data.type === 'result') {
            statusText.innerText = "✨ DUB ACTIVE";
            statusText.style.color = "#00ff88";
            
            const btn = widget.querySelector('#aureus-action-btn');
            btn.innerText = "ACTIVE";
            btn.style.background = "rgba(0, 255, 136, 0.2)";
            btn.style.border = "1px solid #00ff88";

            const video = document.querySelector('video');
            video.volume = 0.15; // Duck original
            video.play();
            
            // Sync time loop
            setInterval(() => {
                if (!video.paused) {
                    chrome.runtime.sendMessage({ type: 'SYNC_AUDIO', currentTime: video.currentTime }).catch(() => {});
                }
            }, 500);
        }
    }
});

// AUREUS V3: Keep Service Worker Alive during heavy processing
setInterval(() => {
    chrome.runtime.sendMessage({ type: 'KEEP_ALIVE' }).catch(() => {});
}, 10000);

const observer = new MutationObserver(() => createV3Widget());
observer.observe(document.body, { childList: true, subtree: true });
createV3Widget();
