/**
 * AUREUS V3.1: The Engine (offscreen.js)
 * 
 * This is the "Stable Tier" home for our WebSocket. 
 * Since this is a window-like environment, it won't be killed during 
 * long processing gaps.
 */

const BACKEND_WS = 'ws://127.0.0.1:8005/ws';
let socket = null;
let currentAudio = null;

function connect(urlToProcess) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ type: 'start', url: urlToProcess }));
        return;
    }

    console.log("AUREUS ENGINE: Connecting to Backend...");
    socket = new WebSocket(BACKEND_WS);

    socket.onopen = () => {
        console.log("AUREUS ENGINE: WebSocket Linked ✅");
        socket.send(JSON.stringify({ type: 'start', url: urlToProcess }));

        // Internal Keep-Alive to Backend
        socket.pingInterval = setInterval(() => {
            if (socket.readyState === WebSocket.OPEN) {
                socket.send(JSON.stringify({ type: 'ping' }));
            }
        }, 10000);
    };

    socket.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.type === 'pong') return;

        console.log("AUREUS ENGINE: Message Received", data);

        // Notify Background (which will relay to Content Scripts)
        chrome.runtime.sendMessage({
            target: 'background',
            type: 'AUREUS_UPDATE',
            data: data
        });

        if (data.type === 'result') {
            playAudio(data.audio_url);
        }
    };

    socket.onclose = () => {
        console.warn("AUREUS ENGINE: WebSocket Closed. Re-routing through Dispatcher...");
        if (socket.pingInterval) clearInterval(socket.pingInterval);
        socket = null;
    };
}

function playAudio(url) {
    if (currentAudio) {
        currentAudio.pause();
    }
    currentAudio = new Audio(url);
    currentAudio.play();
}

chrome.runtime.onMessage.addListener((message) => {
    if (message.target !== 'offscreen') return;

    if (message.type === 'START_INTERCEPT') {
        connect(message.url);
    }

    if (message.type === 'SYNC_AUDIO' && currentAudio) {
        const diff = Math.abs(currentAudio.currentTime - message.currentTime);
        if (diff > 0.4) {
            currentAudio.currentTime = message.currentTime;
        }
    }

    if (message.type === 'PAUSE_AUDIO' && currentAudio) {
        currentAudio.pause();
    }

    if (message.type === 'RESUME_AUDIO' && currentAudio) {
        currentAudio.play();
    }
});
