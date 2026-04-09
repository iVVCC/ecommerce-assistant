from src.agents.base_agent import BaseAgent

class CustomerServiceAgent(BaseAgent):
    def __init__(self):
        super().__init__('customer_service')
    
    def handle_inquiry(self, inquiry, context=None):
        return self.generate_response(inquiry, context)
