from src.agents.customer_service_agent import CustomerServiceAgent
from src.agents.product_recommendation_agent import ProductRecommendationAgent
from src.agents.order_processing_agent import OrderProcessingAgent
import asyncio

# 初始化各个Agent（全局变量，确保在run_workflow中可以访问）
customer_service_agent = CustomerServiceAgent()
product_recommendation_agent = ProductRecommendationAgent()
order_processing_agent = OrderProcessingAgent()

# 执行工作流
def run_workflow(query, context=None):
    """简化的工作流处理函数，直接根据查询内容路由到对应Agent"""
    query_lower = query.lower()
    
    if any(keyword in query_lower for keyword in ['订单', '物流', '发货', '收货', '退货', '退款']):
        return order_processing_agent.process_order(query, context)
    elif any(keyword in query_lower for keyword in ['推荐', '产品', '商品', '购买', '选择']):
        return product_recommendation_agent.recommend_products(query, context)
    else:
        return customer_service_agent.handle_inquiry(query, context)

async def get_agent_stream(query, context=None):
    """流式工作流处理函数，返回异步生成器"""
    query_lower = query.lower()
    
    # 根据查询内容路由到对应Agent
    if any(keyword in query_lower for keyword in ['订单', '物流', '发货', '收货', '退货', '退款']):
        agent = order_processing_agent
        system_prompt = "你是一个订单处理专家，负责处理订单查询、修改和跟踪等问题。"
    elif any(keyword in query_lower for keyword in ['推荐', '产品', '商品', '购买', '选择']):
        agent = product_recommendation_agent
        system_prompt = "你是一个产品推荐专家，根据用户的需求和偏好推荐合适的产品。"
    else:
        agent = customer_service_agent
        system_prompt = "你是一个专业的电商客服代表，善于理解用户需求并提供友好、专业的服务。"
    
    # 使用流式API获取响应
    from src.agents.base_agent import BaseAgent
    
    # 构建消息
    messages = [
        {"role": "system", "content": system_prompt}
    ]
    
    if context:
        messages.extend(context)
    
    messages.append({"role": "user", "content": query})
    
    # 调用流式API
    from src.config.config import Config
    import requests
    import json
    
    BAILIAN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
    API_KEY = Config.OPENAI_API_KEY
    
    data = {
        "model": Config.MODEL_NAME,
        "messages": messages,
        "temperature": Config.TEMPERATURE,
        "max_tokens": Config.MAX_TOKENS,
        "stream": True
    }
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    # 在异步环境中执行同步请求
    loop = asyncio.get_event_loop()
    
    def make_streaming_request():
        response = requests.post(
            BAILIAN_API_URL,
            headers=headers,
            data=json.dumps(data),
            stream=True,
            timeout=60
        )
        response.raise_for_status()
        return response
    
    # 执行请求
    response = await loop.run_in_executor(None, make_streaming_request)
    
    # 处理流式响应
    for line in response.iter_lines():
        if line:
            line_text = line.decode('utf-8')
            
            if line_text.startswith('data: '):
                json_str = line_text[6:]
                
                if json_str == '[DONE]':
                    break
                
                try:
                    chunk_data = json.loads(json_str)
                    
                    if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                        delta = chunk_data['choices'][0].get('delta', {})
                        content = delta.get('content', '')
                        
                        if content:
                            yield content
                            # 添加小延迟使输出更平滑
                            await asyncio.sleep(0.01)
                            
                except json.JSONDecodeError:
                    continue
