import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = 'sk-bc70e645c106423a8b181eeec4e7e0c0'
    MODEL_NAME = 'qwen3.6-plus'
    TEMPERATURE = 0.7
    MAX_TOKENS = 1000
    
    # 系统提示
    SYSTEM_PROMPTS = {
        'customer_service': "你是一个专业的电商客服代表，善于理解用户需求并提供友好、专业的服务。",
        'product_recommendation': "你是一个产品推荐专家，根据用户的需求和偏好推荐合适的产品。",
        'order_processing': "你是一个订单处理专家，负责处理订单查询、修改和跟踪等问题。"
    }
