"""
MultiAgent-SalesArchitect Web 界面
基于 Streamlit 的单页应用，展示三 Agent 协作生成售前方案书。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from graph.workflow import run_workflow

# ---------- 页面配置 ----------
st.set_page_config(page_title="SalesArchitect", page_icon="🏗️", layout="wide")
st.title("🏗️ MultiAgent-SalesArchitect")
st.caption("输入客户需求，三 Agent 协作生成售前方案书")

# ---------- 输入区域 ----------
st.subheader("📝 客户需求描述")
raw_requirement = st.text_area(
    "请用一句话或一段话描述客户需求",
    value="我们是一家中小型电商公司，希望引入AI客服来降低人力成本并提升客户满意度。",
    height=100,
)

# ---------- 生成按钮 ----------
if st.button("🚀 开始生成方案书", type="primary"):
    if not raw_requirement.strip():
        st.warning("请输入客户需求。")
    else:
        # 步骤占位符
        step1_placeholder = st.empty()
        step2_placeholder = st.empty()
        step3_placeholder = st.empty()
        step4_placeholder = st.empty()

        try:
            # 运行工作流
            with st.spinner("正在分析需求..."):
                result = run_workflow(raw_requirement)

            # 逐步展示结果
            step1_placeholder.success("✅ 需求分析完成")
            with st.expander("📋 查看需求分析报告", expanded=False):
                st.markdown(result.get("analysis", "分析结果为空。"))

            step2_placeholder.success("✅ 技术方案生成完成")
            with st.expander("🏗️ 查看技术方案", expanded=False):
                st.markdown(result.get("proposal", "方案为空。"))

            step3_placeholder.success("✅ 技术评审完成")
            with st.expander("🔍 查看技术评审报告", expanded=False):
                st.markdown(result.get("review", "评审为空。"))

            step4_placeholder.success("✅ 最终方案书已生成")
            st.markdown("---")
            st.subheader("📄 最终售前方案书")
            st.markdown(result.get("final_doc", "方案书生成失败。"))

        except Exception as e:
            st.error(f"生成方案书时出错: {e}")

# ---------- 页脚 ----------
st.markdown("---")
st.caption("Powered by LangGraph + 通义千问 | MultiAgent-SalesArchitect")