# AI电商客服助手

基于多Agent协作的智能电商客服系统，使用Python + LangGraph + FastAPI + Streamlit构建。

## 项目简介

本项目实现了一个智能电商客服系统，采用多Agent协作架构，能够自动识别用户意图并路由到相应的专业Agent进行处理。系统支持流式响应，提供流畅的对话体验。

## 功能特性

- **多Agent协作架构**
  - 客服Agent：处理一般咨询和问题
  - 订单处理Agent：处理订单查询、物流跟踪、退换货等
  - 产品推荐Agent：根据用户需求推荐合适的产品

- **智能意图识别**
  - 自动识别用户查询类型
  - 智能路由到对应的专业Agent

- **流式响应**
  - 使用阿里百炼流式API
  - 实时输出，提升用户体验
  - 支持打字机效果

- **上下文管理**
  - 维护对话历史
  - 支持多轮对话

## 技术栈

- **后端框架**: FastAPI
- **前端框架**: Streamlit
- **Agent框架**: LangGraph
- **AI模型**: 阿里百炼 API (glm-5/qwen3.6-plus)
- **编程语言**: Python 3.12+

## 项目结构

```
E-commerce Customer/
├── src/
│   ├── agents/              # Agent模块
│   │   ├── base_agent.py           # 基础Agent类
│   │   ├── agent_coordinator.py    # Agent协调器
│   │   ├── langgraph_agent.py      # LangGraph工作流
│   │   ├── customer_service_agent.py      # 客服Agent
│   │   ├── order_processing_agent.py      # 订单处理Agent
│   │   └── product_recommendation_agent.py  # 产品推荐Agent
│   ├── backend/             # 后端服务
│   │   └── app.py           # FastAPI应用
│   ├── frontend/            # 前端界面
│   │   └── app.py           # Streamlit应用
│   ├── config/              # 配置文件
│   │   └── config.py        # 系统配置
│   └── utils/               # 工具模块
│       └── tools.py         # 工具函数
├── requirements.txt         # 依赖列表
├── start_backend.py         # 后端启动脚本
├── start_frontend.py        # 前端启动脚本
└── README.md               # 项目文档
```

## 安装部署

### 1. 克隆仓库

```bash
git clone https://github.com/iVVCC/ecommerce-assistant.git
cd ecommerce-assistant
```

### 2. 创建虚拟环境

```bash
python -m venv new_venv
```

### 3. 激活虚拟环境

**Windows:**
```bash
new_venv\Scripts\activate
```

**Linux/Mac:**
```bash
source new_venv/bin/activate
```

### 4. 安装依赖

```bash
pip install -r requirements.txt
```

### 5. 配置API密钥

编辑 `src/config/config.py` 文件，配置你的阿里百炼API密钥：

```python
class Config:
    OPENAI_API_KEY = 'your-api-key-here'  # 替换为你的API密钥
    MODEL_NAME = 'qwen3.6-plus'           # 模型名称
    # ...
```

## 启动服务

### 启动后端服务

```bash
python start_backend.py
```

后端服务将运行在: http://localhost:8000

### 启动前端服务

```bash
new_venv\Scripts\python.exe -m streamlit run src/frontend/app.py --server.port 8502
```

前端服务将运行在: http://localhost:8502

## 使用说明

1. 打开浏览器访问 http://localhost:8502
2. 在输入框中输入你的问题，例如：
   - "我的订单什么时候发货？"
   - "推荐一款适合我的产品"
   - "如何退换货？"
3. 系统会自动识别意图并给出相应的回答

## API接口

### 查询接口

**POST** `/api/query`

请求体：
```json
{
  "query": "我的订单什么时候发货？"
}
```

响应：流式文本输出

### 清除上下文

**POST** `/api/clear_context`

清除当前对话的上下文历史。

### 健康检查

**GET** `/health`

检查服务状态。

## Agent路由规则

系统根据关键词自动路由到对应的Agent：

| 关键词 | Agent类型 |
|--------|-----------|
| 订单、物流、发货、收货、退货、退款 | 订单处理Agent |
| 推荐、产品、商品、购买、选择 | 产品推荐Agent |
| 其他 | 客服Agent |

## 配置说明

### 模型配置

在 `src/config/config.py` 中可以修改：

- `MODEL_NAME`: 模型名称（如 qwen3.6-plus, glm-5等）
- `TEMPERATURE`: 温度参数（0-1之间，控制创造性）
- `MAX_TOKENS`: 最大生成token数
- `SYSTEM_PROMPTS`: 各Agent的系统提示词

## 开发计划

- [ ] 添加更多Agent类型
- [ ] 支持多语言
- [ ] 集成知识库
- [ ] 添加用户认证
- [ ] 支持语音输入输出

## 贡献指南

欢迎提交Issue和Pull Request！

## 许可证

MIT License

## 联系方式

如有问题，请通过GitHub Issue联系。

---

**项目地址**: https://github.com/iVVCC/ecommerce-assistant
