import streamlit as st
import requests

API_BASE = "http://127.0.0.1:8000"

st.title("📤 上传接口文档")
uploaded_file = st.file_uploader(
    "选择 OpenAPI 文件 (YAML/JSON)", type=["yaml", "yml", "json"]
)

if uploaded_file:
    files = {"file": uploaded_file}
    with st.spinner("正在上传并解析接口文档..."):
        res = requests.post(f"{API_BASE}/spec/upload", files=files)
    if res.status_code == 200:
        st.success("✅ 上传成功！接口文档解析如下：")
        st.json(res.json())
    else:
        st.error(f"上传失败: {res.text}")
