from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import asyncio
from src.agents.agent_coordinator import AgentCoordinator
from src.utils.tools import handle_error

app = FastAPI(
    title="AI电商客服系统",
    description="基于多Agent协作的智能客服系统",
    version="1.0.0"
)

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str

# 全局Agent协作者实例
coordinator = AgentCoordinator()

async def stream_response(query):
    """使用阿里百炼流式API的响应生成器"""
    try:
        # 添加到上下文
        coordinator.add_to_context("user", query)
        
        # 使用流式API获取响应
        from src.agents.langgraph_agent import get_agent_stream
        
        full_response = []
        async for chunk in get_agent_stream(query, coordinator.context):
            yield chunk
            full_response.append(chunk)
        
        # 保存完整响应到上下文
        complete_response = ''.join(full_response)
        coordinator.add_to_context("assistant", complete_response)
        
    except Exception as e:
        # 更友好的错误信息
        error_msg = str(e)
        if "timeout" in error_msg.lower():
            yield "抱歉，系统响应超时，请稍后再试。"
        elif "unauthorized" in error_msg.lower():
            yield "抱歉，系统认证失败，请检查API配置。"
        else:
            yield f"抱歉，系统暂时无法处理您的请求：{error_msg[:100]}..."

@app.post("/api/query")
async def process_query(request: QueryRequest):
    return StreamingResponse(
        stream_response(request.query),
        media_type="text/plain"
    )

@app.post("/api/clear_context")
async def clear_context():
    coordinator.clear_context()
    return {"message": "Context cleared"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
