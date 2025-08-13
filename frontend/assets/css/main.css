// Initialize AI Chat
const chatToggle = document.getElementById('chatToggle');
const aiChat = document.getElementById('aiChat');
const chatForm = document.getElementById('chatForm');
const chatMessages = document.getElementById('chatMessages');

chatToggle.addEventListener('click', () => {
  aiChat.classList.toggle('active');
});

chatForm.addEventListener('submit', (e) => {
  e.preventDefault();
  const input = chatForm.querySelector('input');
  const message = input.value.trim();
  
  if (message) {
    addMessage('user', message);
    input.value = '';
    
    // Simulate AI response
    setTimeout(() => {
      addMessage('ai', "I'm Robyn, your AI assistant. How can I help you today?");
    }, 1000);
  }
});

function addMessage(sender, text) {
  const messageDiv = document.createElement('div');
  messageDiv.classList.add('message', sender);
  messageDiv.innerHTML = `<p>${text}</p>`;
  chatMessages.appendChild(messageDiv);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Load AI Agents
const agentGrid = document.getElementById('agentGrid');
const agents = [
  {
    name: "Content Creator",
    description: "Generates HD marketing content",
    icon: "content"
  },
  {
    name: "Social Media Manager",
    description: "Automates posting across platforms",
    icon: "social"
  },
  {
    name: "Customer Support",
    description: "24/7 automated customer service",
    icon: "support"
  }
];

function loadAgents() {
  agentGrid.innerHTML = agents.map(agent => `
    <div class="agent-card">
      <div class="agent-icon">
        <img src="./assets/img/${agent.icon}.webp" alt="${agent.name}">
      </div>
      <h3>${agent.name}</h3>
      <p>${agent.description}</p>
      <button class="btn btn-primary">Deploy</button>
    </div>
  `).join('');
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  loadAgents();
  
  // Initialize model-viewer
  const modelViewer = document.querySelector('model-viewer');
  if (modelViewer) {
    modelViewer.addEventListener('load', () => {
      console.log('3D model loaded successfully');
    });
  }
});
