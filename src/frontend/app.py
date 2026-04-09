import streamlit as st
import requests
import time

# 设置页面配置
st.set_page_config(
    page_title="AI电商客服系统",
    page_icon="🛍️",
    layout="wide"
)

# 后端API地址
API_URL = "http://localhost:8000"

# 初始化会话状态
if "messages" not in st.session_state:
    st.session_state.messages = []

# 页面标题
st.title("AI电商客服系统")
st.subheader("多Agent协作智能客服")

# 聊天窗口
st.markdown("---")
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入
if prompt := st.chat_input("请输入您的问题..."):
    # 添加用户消息到会话状态
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # 显示用户消息
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 显示思考动画
    with st.chat_message("assistant"):
        # 显示简单的思考提示
        st.markdown("思考中...")
        
        # 发送请求到后端API（流式）
        try:
            # 不设置超时时间
            response = requests.post(
                f"{API_URL}/api/query",
                json={"query": prompt},
                stream=True
            )
            response.raise_for_status()
            
            # 清空思考提示，准备显示响应
            st.empty()
            
            # 流式接收响应
            assistant_response = ""
            response_placeholder = st.empty()
            
            # 更自然的流式输出
            for chunk in response.iter_content(chunk_size=1024, decode_unicode=True):
                if chunk:
                    assistant_response += chunk
                    # 实时更新显示
                    response_placeholder.markdown(assistant_response)
                    # 稍微延迟，使输出更自然
                    time.sleep(0.01)
            
            # 添加助手消息到会话状态
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
        except requests.Timeout:
            # 清空思考提示
            st.empty()
            
            error_message = "抱歉，系统响应超时，请稍后再试。"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.markdown(error_message)
        except Exception as e:
            # 清空思考提示
            st.empty()
            
            error_message = f"抱歉，系统暂时无法处理您的请求：{str(e)}"
            st.session_state.messages.append({"role": "assistant", "content": error_message})
            st.markdown(error_message)

# 侧边栏
with st.sidebar:
    st.title("功能操作")
    
    # 清空对话历史
    if st.button("清空对话历史"):
        st.session_state.messages = []
        # 调用API清空上下文
        try:
            requests.post(f"{API_URL}/api/clear_context")
        except:
            pass
        st.rerun()
    
    # 系统信息
    st.markdown("---")
    st.subheader("系统信息")
    st.write("基于多Agent协作的智能客服系统")
    st.write("支持客服咨询、产品推荐、订单处理")
