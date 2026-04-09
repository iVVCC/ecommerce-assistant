from src.agents.langgraph_agent import run_workflow

class AgentCoordinator:
    def __init__(self):
        self.context = []
        self.max_context_length = 10  # 最多保存10条消息
    
    def route_query(self, query):
        # 使用LangGraph工作流处理查询
        return run_workflow(query, self.context)
    
    def add_to_context(self, role, content):
        self.context.append({"role": role, "content": content})
        # 确保上下文长度不超过限制
        if len(self.context) > self.max_context_length:
            self.context = self.context[-self.max_context_length:]
    
    def clear_context(self):
        self.context = []
