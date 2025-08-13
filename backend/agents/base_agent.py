from datetime import datetime
import logging
import os

class BaseAgent:
    """Base class for all AI agents"""
    
    def __init__(self, agent_id, capabilities):
        self.agent_id = agent_id
        self.capabilities = capabilities
        self.logger = logging.getLogger(agent_id)
        self.start_time = datetime.now()
        
    def log_error(self, message):
        """Standard error logging"""
        self.logger.error(f"[{self.agent_id}] {message}")
        
    def log_transaction(self, message, reference=None):
        """Audit trail for financial ops"""
        log_msg = f"[{self.agent_id}] {message}"
        if reference:
            log_msg += f" | Ref: {reference}"
        self.logger.info(log_msg)
        
    def _call_api(self, url, payload, method='POST'):
        """Generic API caller with retry logic"""
        # Implementation would use requests library
        pass
        
    def health_check(self):
        """Report agent status"""
        return {
            "agent_id": self.agent_id,
            "uptime": str(datetime.now() - self.start_time),
            "capabilities": self.capabilities,
            "status": "healthy"
        }
