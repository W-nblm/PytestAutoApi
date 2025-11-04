import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.title("🚀 执行测试用例")

if st.button("运行所有测试用例"):
    with st.spinner("正在执行测试，请稍候..."):
        res = requests.post(f"{API_BASE}/run/execute")
    if res.status_code == 200:
        st.success("✅ 测试执行完成")
        report = res.json()
        st.json(report)
    else:
        st.error(f"执行失败: {res.text}")
