/**
 * Arthur Voice System
 * Makes Arthur actually SPEAK his responses
 */

// Extend ArthurChat class to add voice
ArthurChat.prototype.playArthurVoice = async function(text) {
    try {
        const response = await fetch('/api/arthur/speak', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                session_id: this.sessionId
            })
        });
        
        const data = await response.json();
        
        if (data.audio_url) {
            // Create and play audio
            const audio = new Audio(data.audio_url);
            audio.play();
            
            // Add visual indicator that Arthur is speaking
            this.showSpeakingIndicator();
            
            audio.onended = () => {
                this.hideSpeakingIndicator();
            };
        }
        
    } catch (error) {
        console.error('Failed to play Arthur voice:', error);
    }
};

ArthurChat.prototype.showSpeakingIndicator = function() {
    const indicator = document.getElementById('arthur-speaking-indicator');
    if (!indicator) {
        const ind = document.createElement('div');
        ind.id = 'arthur-speaking-indicator';
        ind.className = 'speaking-indicator';
        ind.innerHTML = '🎙️ Arthur is speaking...';
        document.getElementById('arthur-chat-header').appendChild(ind);
    }
};

ArthurChat.prototype.hideSpeakingIndicator = function() {
    const indicator = document.getElementById('arthur-speaking-indicator');
    if (indicator) {
        indicator.remove();
    }
};

// Override sendMessage to add voice
const originalSendMessage = ArthurChat.prototype.sendMessage;
ArthurChat.prototype.sendMessage = async function(message) {
    // Call original
    await originalSendMessage.call(this, message);
    
    // After Arthur responds, play his voice
    // Get the last Arthur message
    const messages = document.querySelectorAll('.arthur-message');
    if (messages.length > 0) {
        const lastMessage = messages[messages.length - 1];
        const text = lastMessage.querySelector('.message-content p').textContent;
        
        // Play Arthur's voice
        this.playArthurVoice(text);
    }
};

// Auto-play introduction when chat opens
const originalStartSession = ArthurChat.prototype.startSession;
ArthurChat.prototype.startSession = async function() {
    await originalStartSession.call(this);
    
    // Wait for opening message to display, then speak it
    setTimeout(() => {
        const messages = document.querySelectorAll('.arthur-message');
        if (messages.length > 0) {
            const firstMessage = messages[0];
            const text = firstMessage.querySelector('.message-content p').textContent;
            this.playArthurVoice(text);
        }
    }, 500);
};
