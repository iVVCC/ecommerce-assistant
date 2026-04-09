from src.agents.base_agent import BaseAgent

class ProductRecommendationAgent(BaseAgent):
    def __init__(self):
        super().__init__('product_recommendation')
    
    def recommend_products(self, user_preferences, context=None):
        return self.generate_response(f"用户偏好：{user_preferences}", context)
