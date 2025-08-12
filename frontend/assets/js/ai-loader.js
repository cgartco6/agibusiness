/**
 * NexusAGI Core Loader
 * Manages all frontend AI interactions and dynamic content
 */
class AILoader {
    constructor() {
        this.aiEndpoints = {
            content: '/api/ai/content',
            chat: '/api/ai/chat',
            commerce: '/api/ai/commerce'
        };
        this.sessionToken = this.getSessionToken();
        this.initEventListeners();
        this.checkAuthStatus();
    }

    // Initialize all event listeners
    initEventListeners() {
        // Dynamic service loader
        document.querySelectorAll('[data-ai-service]').forEach(el => {
            el.addEventListener('click', () => this.loadService(el.dataset.aiService));
        });

        // AI chat trigger
        const chatTrigger = document.getElementById('ai-chat-trigger');
        if (chatTrigger) {
            chatTrigger.addEventListener('click', () => this.toggleChat());
        }

        // Content refresh handler
        window.addEventListener('ai-content-update', () => this.refreshDynamicContent());
    }

    // Get or create session token
    getSessionToken() {
        let token = localStorage.getItem('nexus_ai_token');
        if (!token) {
            token = crypto.randomUUID();
            localStorage.setItem('nexus_ai_token', token);
        }
        return token;
    }

    // Check authentication status with backend
    async checkAuthStatus() {
        try {
            const response = await fetch('/api/auth/status', {
                headers: {
                    'X-AI-Token': this.sessionToken
                }
            });
            
            const data = await response.json();
            
            if (data.authenticated) {
                document.body.classList.add('ai-authenticated');
                this.loadUserPreferences();
            } else {
                document.body.classList.add('ai-guest');
            }
        } catch (error) {
            console.error('AI Auth Check Failed:', error);
            this.showErrorToast('Connection issue detected. Working in offline mode.');
        }
    }

    // Load AI service dynamically
    async loadService(serviceId) {
        const serviceContainer = document.getElementById('ai-service-container');
        
        // Show loading state
        serviceContainer.innerHTML = `
            <div class="ai-loading">
                <div class="ai-spinner"></div>
                <p>Initializing ${serviceId} agent...</p>
            </div>
        `;
        
        try {
            const response = await fetch(`${this.aiEndpoints.content}/service/${serviceId}`, {
                headers: {
                    'X-AI-Token': this.sessionToken,
                    'Content-Type': 'application/json'
                }
            });
            
            const serviceHTML = await response.text();
            serviceContainer.innerHTML = serviceHTML;
            
            // Dispatch custom event for service-specific JS
            document.dispatchEvent(new CustomEvent('ai-service-loaded', {
                detail: { serviceId }
            }));
            
        } catch (error) {
            console.error(`Failed to load ${serviceId}:`, error);
            serviceContainer.innerHTML = `
                <div class="ai-error">
                    <h3>Service Temporarily Unavailable</h3>
                    <p>Our AI team has been notified. Please try again later.</p>
                    <button onclick="window.location.reload()">Retry</button>
                </div>
            `;
        }
    }

    // Toggle AI chat interface
    toggleChat() {
        const chatContainer = document.getElementById('ai-chat-container');
        chatContainer.classList.toggle('active');
        
        if (chatContainer.classList.contains('active')) {
            this.initChatSession();
        }
    }

    // Initialize chat session with Robyn AI
    async initChatSession() {
        const chatWindow = document.getElementById('ai-chat-messages');
        chatWindow.innerHTML = '<div class="ai-message"><p>Robyn: Hello! How can I assist you today?</p></div>';
        
        // Load chat history if available
        const chatHistory = localStorage.getItem('ai_chat_history');
        if (chatHistory) {
            chatWindow.innerHTML += JSON.parse(chatHistory);
        }
        
        // Set up message listener
        const chatForm = document.getElementById('ai-chat-form');
        chatForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const input = chatForm.querySelector('input');
            const message = input.value.trim();
            
            if (message) {
                this.addChatMessage('user', message);
                input.value = '';
                
                // Get AI response
                const response = await this.getAIResponse(message);
                this.addChatMessage('ai', response);
                
                // Save to history
                this.saveChatHistory();
            }
        });
    }

    // Add message to chat UI
    addChatMessage(sender, content) {
        const chatWindow = document.getElementById('ai-chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `ai-message ${sender}`;
        messageDiv.innerHTML = `<p>${sender === 'user' ? 'You' : 'Robyn'}: ${content}</p>`;
        chatWindow.appendChild(messageDiv);
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }

    // Get response from AI backend
    async getAIResponse(message) {
        try {
            const response = await fetch(`${this.aiEndpoints.chat}/respond`, {
                method: 'POST',
                headers: {
                    'X-AI-Token': this.sessionToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message })
            });
            
            const data = await response.json();
            return data.response || "I'm having trouble connecting to my neural network. Please try again later.";
        } catch (error) {
            console.error('Chat Error:', error);
            return "Apologies, I'm experiencing technical difficulties. My human overlords have been alerted.";
        }
    }

    // Save chat history
    saveChatHistory() {
        const chatWindow = document.getElementById('ai-chat-messages');
        const messages = Array.from(chatWindow.querySelectorAll('.ai-message'))
            .map(el => el.outerHTML);
        localStorage.setItem('ai_chat_history', JSON.stringify(messages.join('')));
    }

    // Refresh dynamic content
    async refreshDynamicContent() {
        const dynamicElements = document.querySelectorAll('[data-ai-content]');
        
        await Promise.all(Array.from(dynamicElements).map(async el => {
            const contentKey = el.dataset.aiContent;
            try {
                const response = await fetch(`${this.aiEndpoints.content}/dynamic/${contentKey}`);
                const content = await response.text();
                el.innerHTML = content;
            } catch (error) {
                console.error(`Failed to refresh ${contentKey}:`, error);
                el.innerHTML = '<span class="ai-error">Content update failed</span>';
            }
        }));
    }

    // Show error notification
    showErrorToast(message) {
        const toast = document.createElement('div');
        toast.className = 'ai-toast error';
        toast.innerHTML = `
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="8" x2="12" y2="12"></line>
                <line x1="12" y1="16" x2="12.01" y2="16"></line>
            </svg>
            <span>${message}</span>
        `;
        
        document.body.appendChild(toast);
        setTimeout(() => toast.remove(), 5000);
    }
}

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    const aiLoader = new AILoader();
    
    // Make available globally for debugging
    window.NexusAI = aiLoader;
});
