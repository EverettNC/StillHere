/**
 * Arthur Intelligent Chat System
 * Real-time personality detection + adaptive responses
 * Carbon + Silicon closed loop
 */

class ArthurChat {
    constructor() {
        this.sessionId = null;
        this.messageStartTime = null;
        this.conversationHistory = [];
        this.isTyping = false;
    }

    async startSession() {
        try {
            const response = await fetch('/api/arthur/start', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });
            
            const data = await response.json();
            this.sessionId = data.session_id;
            
            // Display Arthur's opening message
            this.displayArthurMessage(data.arthur_response);
            
        } catch (error) {
            console.error('Failed to start Arthur session:', error);
        }
    }

    async sendMessage(message) {
        if (!message.trim() || this.isTyping) return;
        
        // Calculate response time
        const responseTime = this.messageStartTime 
            ? (Date.now() - this.messageStartTime) / 1000 
            : null;
        
        // Display user message
        this.displayUserMessage(message);
        
        // Show Arthur typing
        this.showTypingIndicator();
        this.isTyping = true;
        
        try {
            const response = await fetch('/api/arthur/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    session_id: this.sessionId,
                    message: message,
                    response_time: responseTime
                })
            });
            
            const data = await response.json();
            
            // Hide typing indicator
            this.hideTypingIndicator();
            this.isTyping = false;
            
            // Display Arthur's intelligent response
            this.displayArthurMessage(data.arthur_response);
            
            // Update personality indicator
            if (data.personality_detected) {
                this.updatePersonalityIndicator(
                    data.personality_detected, 
                    data.confidence
                );
            }
            
            // Track predictions
            if (data.predictions && data.predictions.length > 0) {
                console.log('Arthur predictions:', data.predictions);
            }
            
            // Reset message timer for next response
            this.messageStartTime = Date.now();
            
        } catch (error) {
            console.error('Chat error:', error);
            this.hideTypingIndicator();
            this.isTyping = false;
        }
    }

    displayUserMessage(message) {
        const chatContainer = document.getElementById('arthur-chat-messages');
        const messageEl = document.createElement('div');
        messageEl.className = 'chat-message user-message';
        messageEl.innerHTML = `
            <div class="message-content">
                <p>${this.escapeHtml(message)}</p>
            </div>
        `;
        chatContainer.appendChild(messageEl);
        this.scrollToBottom();
    }

    displayArthurMessage(message) {
        const chatContainer = document.getElementById('arthur-chat-messages');
        const messageEl = document.createElement('div');
        messageEl.className = 'chat-message arthur-message';
        messageEl.innerHTML = `
            <div class="arthur-avatar">A</div>
            <div class="message-content">
                <p>${this.formatMessage(message)}</p>
            </div>
        `;
        chatContainer.appendChild(messageEl);
        this.scrollToBottom();
    }

    showTypingIndicator() {
        const chatContainer = document.getElementById('arthur-chat-messages');
        const typingEl = document.createElement('div');
        typingEl.id = 'typing-indicator';
        typingEl.className = 'chat-message arthur-message typing';
        typingEl.innerHTML = `
            <div class="arthur-avatar">A</div>
            <div class="message-content">
                <div class="typing-dots">
                    <span></span><span></span><span></span>
                </div>
            </div>
        `;
        chatContainer.appendChild(typingEl);
        this.scrollToBottom();
    }

    hideTypingIndicator() {
        const typingEl = document.getElementById('typing-indicator');
        if (typingEl) {
            typingEl.remove();
        }
    }

    updatePersonalityIndicator(type, confidence) {
        const indicator = document.getElementById('personality-indicator');
        if (!indicator) return;
        
        const typeLabel = {
            'suggestible': '💜 Emotional Journey',
            'solid': '🎯 Factual Exploration',
            'neutral': '⚖️ Balanced Approach'
        }[type] || 'Detecting...';
        
        indicator.innerHTML = `
            <div class="personality-badge">
                ${typeLabel}
                <span class="confidence">${Math.round(confidence * 100)}%</span>
            </div>
        `;
        indicator.style.display = 'block';
    }

    formatMessage(message) {
        // Preserve line breaks
        return message.replace(/\n/g, '<br>');
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    scrollToBottom() {
        const chatContainer = document.getElementById('arthur-chat-messages');
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
}

// Initialize Arthur chat when page loads
let arthurChat;

document.addEventListener('DOMContentLoaded', () => {
    arthurChat = new ArthurChat();
    
    // Start session button
    const startBtn = document.getElementById('start-arthur-chat');
    if (startBtn) {
        startBtn.addEventListener('click', () => {
            document.getElementById('arthur-chat-container').style.display = 'flex';
            arthurChat.startSession();
            startBtn.style.display = 'none';
        });
    }
    
    // Send message
    const sendBtn = document.getElementById('send-arthur-message');
    const inputEl = document.getElementById('arthur-chat-input');
    
    if (sendBtn && inputEl) {
        sendBtn.addEventListener('click', () => {
            const message = inputEl.value;
            if (message.trim()) {
                arthurChat.sendMessage(message);
                inputEl.value = '';
            }
        });
        
        inputEl.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const message = inputEl.value;
                if (message.trim()) {
                    arthurChat.sendMessage(message);
                    inputEl.value = '';
                }
            }
        });
        
        // Start response timer
        inputEl.addEventListener('focus', () => {
            if (!arthurChat.messageStartTime) {
                arthurChat.messageStartTime = Date.now();
            }
        });
    }
});
