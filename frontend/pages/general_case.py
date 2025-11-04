import streamlit as st
import requests
import yaml

API_BASE = "http://127.0.0.1:8000"

st.title("🧠 AI 生成测试用例")

if st.button("生成测试用例"):
    with st.spinner("正在调用 AI 生成测试用例..."):
        res = requests.post(f"{API_BASE}/case/generate")
    if res.status_code == 200:
        path = res.json().get("data").get("generated_case_file")
        st.success(f"✅ 用例生成完成：\n{path}")

    else:
        st.error(f"生成失败: {res.text}")
