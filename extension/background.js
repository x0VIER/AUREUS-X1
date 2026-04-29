/**
 * AUREUS V3.1: The Dispatcher (background.js)
 * 
 * In this bulletproof architecture, the Service Worker is just a router.
 * It manages the Offscreen Document, which holds the actual WebSocket connection.
 */

async function setupOffscreen() {
    // Check if offscreen already exists
    const existingContexts = await chrome.runtime.getContexts({
        contextTypes: ['OFFSCREEN_DOCUMENT']
    });

    if (existingContexts.length > 0) return;

    await chrome.offscreen.createDocument({
        url: 'offscreen.html',
        reasons: ['AUDIO_PLAYBACK', 'WEB_RTC'], // Using WEB_RTC as a proxy reason for persistent connection
        justification: 'AUREUS X1 requires a persistent WebSocket for long-duration audio processing.'
    });
}

// Relays messages from Offscreen -> Content Scripts (Broadcast)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.target === 'background') {
        if (message.type === 'AUREUS_UPDATE') {
            chrome.tabs.query({}, (tabs) => {
                tabs.forEach(tab => {
                    chrome.tabs.sendMessage(tab.id, message).catch(() => {});
                });
            });
        }
        return;
    }

    if (message.type === 'START_INTERCEPT') {
        setupOffscreen().then(() => {
            // Forward the command to the offscreen engine
            chrome.runtime.sendMessage({ ...message, target: 'offscreen' });
        });
        return true;
    }

    // Pass-through for sync/pause/resume commands to offscreen
    if (['SYNC_AUDIO', 'PAUSE_AUDIO', 'RESUME_AUDIO'].includes(message.type)) {
        chrome.runtime.sendMessage({ ...message, target: 'offscreen' }).catch(() => {});
    }
});

// Alarm to occasionally wake service worker if needed, though offscreen handles the heavy lifting
chrome.alarms.create('AUREUS_HEARTBEAT', { periodInMinutes: 1 });
chrome.alarms.onAlarm.addListener(() => {
    console.log("AUREUS: Dispatcher Heartbeat");
});
