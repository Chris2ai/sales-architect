"""
MultiAgent-SalesArchitect Web 界面（实时状态流版）
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import streamlit as st
from graph.workflow import run_workflow

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

# ---------- 初始化会话状态 ----------
if "status_messages" not in st.session_state:
    st.session_state.status_messages = []
if "final_result" not in st.session_state:
    st.session_state.final_result = None

# ---------- 生成按钮 ----------
if st.button("🚀 开始生成方案书", type="primary"):
    if not raw_requirement.strip():
        st.warning("请输入客户需求。")
    else:
        # 重置状态
        st.session_state.status_messages = []
        st.session_state.final_result = None

        # 状态容器
        status_container = st.status("准备生成...", expanded=True)

        def status_callback(step: str, msg: str):
            """工作流回调：将状态消息存入会话状态"""
            icon_map = {
                "analyst": "📋",
                "architect": "🏗️",
                "reviewer": "🔍",
                "finalize": "📄",
                "done": "✅",
            }
            icon = icon_map.get(step, "⏳")
            st.session_state.status_messages.append(f"{icon} {msg}")

        # 运行工作流（阻塞，但回调会实时更新状态）
        result = run_workflow(raw_requirement, status_callback=status_callback)

        # 更新状态容器
        with status_container:
            for msg in st.session_state.status_messages:
                st.write(msg)
            status_container.update(label="方案书生成完毕！", state="complete")

        # 保存结果
        st.session_state.final_result = result

# ---------- 展示最终结果 ----------
if st.session_state.final_result:
    st.markdown("---")
    st.subheader("📄 最终售前方案书")
    st.markdown(st.session_state.final_result.get("final_doc", "方案书生成失败。"))

    # 折叠查看中间结果
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.expander("📋 需求分析报告"):
            st.markdown(st.session_state.final_result.get("analysis", ""))
    with col2:
        with st.expander("🏗️ 技术方案"):
            st.markdown(st.session_state.final_result.get("proposal", ""))
    with col3:
        with st.expander("🔍 技术评审报告"):
            st.markdown(st.session_state.final_result.get("review", ""))

st.markdown("---")
st.caption("Powered by LangGraph + 通义千问 | MultiAgent-SalesArchitect")