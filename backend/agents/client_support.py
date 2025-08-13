from openai import OpenAI
from .base_agent import BaseAgent
from app.models import SupportTicket
import re

class ClientSupportAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            agent_id="support_specialist_v4",
            capabilities=["ticketing", "live_chat", "knowledge_base"]
        )
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.model = "gpt-4-1106-preview"
    
    def handle_ticket(self, ticket_id):
        """Process support ticket with AI"""
        ticket = SupportTicket.query.get(ticket_id)
        if not ticket:
            raise ValueError("Ticket not found")
        
        # Generate response
        prompt = self._build_prompt(ticket)
        response = self._generate_response(prompt)
        
        # Store response
        ticket.response = self._clean_response(response)
        ticket.status = "responded"
        db.session.commit()
        
        return ticket
    
    def _build_prompt(self, ticket):
        """Construct LLM prompt from ticket"""
        return f"""
        You are Robyn, an AI support agent for an AGI business platform.
        Client: {ticket.client.name}
        Priority: {ticket.priority}
        Issue: {ticket.description}
        
        Guidelines:
        - Respond in friendly but professional tone
        - Use South African English phrasing
        - Suggest at least one solution
        - Keep under 200 words
        """
    
    def _generate_response(self, prompt):
        """Call OpenAI API"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content
    
    def _clean_response(self, text):
        """Remove unwanted artifacts from AI response"""
        return re.sub(r'\[.*?\]', '', text)  # Remove citation markers
