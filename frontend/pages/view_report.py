import streamlit as st
import json
from pathlib import Path

st.title("📊 查看测试报告")

report_dir = Path("reports")
if not report_dir.exists():
    st.warning("暂无报告，请先执行测试。")
else:
    reports = sorted(report_dir.glob("*.json"), reverse=True)
    if reports:
        selected = st.selectbox("选择测试报告：", reports)
        with open(selected, "r", encoding="utf-8") as f:
            data = json.load(f)
            st.json(data)
    else:
        st.info("没有可用的测试报告。")
