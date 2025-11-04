import streamlit as st

st.set_page_config(
    page_title="AI 测试平台",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 AI 自动化测试平台")
st.markdown(
    """
    ### 欢迎使用 AI Test Platform  
    本平台支持以下功能：
    - 📤 上传接口文档（OpenAPI / Swagger）
    - 🧠 使用 AI 自动生成接口测试用例
    - 🚀 一键执行测试
    - 📊 可视化测试报告与智能分析
    """
)

st.info("请从左侧导航栏选择一个模块开始操作 👈")
