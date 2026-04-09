from src.agents.base_agent import BaseAgent

class OrderProcessingAgent(BaseAgent):
    def __init__(self):
        super().__init__('order_processing')
    
    def process_order(self, order_query, context=None):
        return self.generate_response(order_query, context)
