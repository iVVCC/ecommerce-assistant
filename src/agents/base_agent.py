from src.config.config import Config
import requests
import json
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 阿里百炼API配置 - 使用正确的兼容模式URL
BAILIAN_API_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
API_KEY = Config.OPENAI_API_KEY

class BaseAgent:
    def __init__(self, agent_type):
        self.agent_type = agent_type
        self.system_prompt = Config.SYSTEM_PROMPTS.get(agent_type, "你是一个助手")
    
    def generate_response(self, prompt, context=None):
        """非流式响应，用于兼容旧代码"""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            if context:
                messages.extend(context)
            
            messages.append({"role": "user", "content": prompt})
            
            # 构建请求数据
            data = {
                "model": Config.MODEL_NAME,
                "messages": messages,
                "temperature": Config.TEMPERATURE,
                "max_tokens": Config.MAX_TOKENS
            }
            
            # 设置请求头
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }
            
            logger.info(f"Sending request to 阿里百炼 with model: {Config.MODEL_NAME}")
            logger.info(f"API URL: {BAILIAN_API_URL}")
            # 发送请求，增加超时时间
            response = requests.post(
                BAILIAN_API_URL,
                headers=headers,
                data=json.dumps(data),
                timeout=30
            )
            
            # 检查响应状态
            response.raise_for_status()
            
            # 解析响应
            response_data = response.json()
            logger.info("Received response from 阿里百炼")
            logger.info(f"Response status code: {response.status_code}")
            logger.info(f"Response content: {json.dumps(response_data, ensure_ascii=False)}")
            
            if 'choices' in response_data and len(response_data['choices']) > 0:
                return response_data['choices'][0]['message']['content']
            else:
                return "抱歉，系统暂时无法处理您的请求：响应格式错误"
        except requests.exceptions.RequestException as e:
            logger.error(f"API request error: {str(e)}")
            return f"抱歉，系统暂时无法处理您的请求：{str(e)}"
        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}")
            return f"抱歉，系统暂时无法处理您的请求：{str(e)}"
    
    def generate_response_stream(self, prompt, context=None):
        """流式响应生成器，使用阿里百炼流式API"""
        try:
            messages = [
                {"role": "system", "content": self.system_prompt}
            ]
            
            if context:
                messages.extend(context)
            
            messages.append({"role": "user", "content": prompt})
            
            # 构建请求数据，启用流式输出
            data = {
                "model": Config.MODEL_NAME,
                "messages": messages,
                "temperature": Config.TEMPERATURE,
                "max_tokens": Config.MAX_TOKENS,
                "stream": True  # 启用流式输出
            }
            
            # 设置请求头
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }
            
            logger.info(f"Sending streaming request to 阿里百炼 with model: {Config.MODEL_NAME}")
            
            # 发送流式请求
            response = requests.post(
                BAILIAN_API_URL,
                headers=headers,
                data=json.dumps(data),
                stream=True,  # 启用流式传输
                timeout=60
            )
            
            # 检查响应状态
            response.raise_for_status()
            
            # 处理流式响应
            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')
                    
                    # 跳过空行和data: [DONE]
                    if line_text.startswith('data: '):
                        json_str = line_text[6:]  # 去掉 "data: " 前缀
                        
                        if json_str == '[DONE]':
                            break
                        
                        try:
                            chunk_data = json.loads(json_str)
                            
                            # 提取内容
                            if 'choices' in chunk_data and len(chunk_data['choices']) > 0:
                                delta = chunk_data['choices'][0].get('delta', {})
                                content = delta.get('content', '')
                                
                                if content:
                                    yield content
                                    
                        except json.JSONDecodeError:
                            logger.warning(f"Failed to parse JSON: {json_str}")
                            continue
                            
        except requests.exceptions.RequestException as e:
            logger.error(f"API streaming request error: {str(e)}")
            yield f"抱歉，系统暂时无法处理您的请求：{str(e)}"
        except Exception as e:
            logger.error(f"Error in generate_response_stream: {str(e)}")
            yield f"抱歉，系统暂时无法处理您的请求：{str(e)}"
