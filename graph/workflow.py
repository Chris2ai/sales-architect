"""
LangGraph 工作流：需求分析师 → 方案架构师 → 技术评审员 → 方案书整合
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from typing import TypedDict
from langgraph.graph import StateGraph, END

from agents.analyst import analyze
from agents.architect import design
from agents.reviewer import review

# ---------- 1. 定义 State（工作流中流转的数据） ----------
class WorkflowState(TypedDict):
    raw_requirement: str     # 用户输入的原始需求
    analysis: str            # 需求分析师输出
    proposal: str            # 方案架构师输出
    review: str              # 技术评审员输出
    final_doc: str           # 最终整合的方案书
    review_passed: bool      # 新增：评审是否通过
    iteration: int           # 新增：当前迭代次数

# ---------- 2. 定义三个 Node（每个节点调用一个 Agent） ----------
def node_analyst(state: WorkflowState) -> WorkflowState:
    """节点1：需求分析"""
    print("📋 [1/3] 需求分析师正在分析...")
    analysis_result = analyze(state["raw_requirement"])
    return {"analysis": analysis_result}

def node_architect(state: WorkflowState) -> WorkflowState:
    """节点2：方案设计（含迭代）"""
    iteration = state.get("iteration", 1) + 1
    if iteration > 1:
        print(f"🏗️ [2/3] 方案架构师正在根据评审意见修改方案...（第 {iteration} 轮）")
        # 将评审意见附在需求分析后面，供架构师参考
        input_with_feedback = f"{state['analysis']}\n\n【上一轮评审意见】\n{state['review']}"
        proposal_result = design(input_with_feedback)
    else:
        print("🏗️ [2/3] 方案架构师正在设计方案...")
        proposal_result = design(state["analysis"])

    return {"proposal": proposal_result, "iteration": iteration}

def node_reviewer(state: WorkflowState) -> WorkflowState:
    """节点3：技术评审（含通过/不通过判断）"""
    iteration = state.get("iteration", 1)
    print(f"🔍 [3/3] 技术评审员正在评审方案...（第 {iteration} 轮）")
    review_result = review(state["proposal"])

    # 简单判断是否通过：如果评审结论中包含“不通过”且不含“通过”则未通过
    passed = "不通过" not in review_result or "通过" in review_result.replace("不通过", "")

    return {
        "review": review_result,
        "review_passed": passed,
    }

def should_continue(state: WorkflowState) -> str:
    """条件判断：评审是否通过？是否达到最大迭代次数？"""
    MAX_ITERATIONS = 3

    if state.get("review_passed", False):
        print("✅ 评审通过！进入方案书整合。")
        return "finalize"

    if state.get("iteration", 1) >= MAX_ITERATIONS:
        print(f"⚠️ 已达最大迭代次数（{MAX_ITERATIONS}），强制进入整合。")
        return "finalize"

    print(f"🔄 评审未通过，返回方案架构师修改（第 {state.get('iteration', 1) + 1} 轮）...")
    return "architect"

def node_finalize(state: WorkflowState) -> WorkflowState:
    """节点4：整合最终方案书（专业化模板）"""
    print("📄 正在整合方案书...")
    final = f"""---
title: "售前方案书"
author: "MultiAgent-SalesArchitect"
date: "{__import__('datetime').datetime.now().strftime('%Y-%m-%d')}"
---

# 🏗️ 售前方案书

> **项目名称**：{state.get('raw_requirement', '未提供')[:80]}  
> **生成时间**：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}  
> **生成方式**：三 Agent 协作（需求分析 → 方案设计 → 技术评审）

---

## 📑 目录
1. [需求分析](#一需求分析)
2. [技术方案](#二技术方案)
3. [技术评审](#三技术评审)

---

## 一、需求分析
{state["analysis"]}

---

## 二、技术方案
{state["proposal"]}

---

## 三、技术评审
{state["review"]}

---

> 本方案书由 AI 多智能体协作自动生成，仅供参考。实际部署前需结合客户具体场景进行人工复核与调整。
"""
    return {"final_doc": final}

# ---------- 3. 构建 Graph ----------
graph = StateGraph(WorkflowState)

# 添加节点
graph.add_node("analyst", node_analyst)
graph.add_node("architect", node_architect)
graph.add_node("reviewer", node_reviewer)
graph.add_node("finalize", node_finalize)

# 添加边
graph.set_entry_point("analyst")
graph.add_edge("analyst", "architect")
graph.add_edge("architect", "reviewer")

# 条件边：评审后决定是修改还是结束
graph.add_conditional_edges(
    "reviewer",
    should_continue,
    {
        "architect": "architect",   # 不通过 → 返回修改
        "finalize": "finalize",     # 通过 → 整合输出
    }
)

graph.add_edge("finalize", END)

# 编译
# app = graph.compile() 注释掉改为手动控制流程

# ---------- 4. 调用函数 ----------
def run_workflow(raw_requirement: str, status_callback=None):
    """
    运行完整工作流。
    status_callback: 可选的回调函数，接收 (step_name, message) 两个参数
    """
    def log(step: str, msg: str):
        print(msg)
        if status_callback:
            status_callback(step, msg)

    # 构建初始状态（用 dict 确保可变，避免 TypedDict 限制）
    state = dict(
        raw_requirement=raw_requirement,
        analysis="",
        proposal="",
        review="",
        final_doc="",
        review_passed=False,
        iteration=0,
    )

    # 第一步：需求分析
    log("analyst", "📋 需求分析师正在分析...")
    state.update(node_analyst(state))

    # 第二步：第一次方案设计
    log("architect", "🏗️ 方案架构师正在设计方案...")
    state.update(node_architect(state))

    # 循环评审与修改
    max_iterations = 3
    while True:
        state.update(node_reviewer(state))
        log("reviewer", f"🔍 评审完成（第 {state.get('iteration', 1)} 轮）")

        decision = should_continue(state)
        if decision == "finalize":
            log("finalize", "✅ 评审通过，正在整合方案书...")
            break
        elif state.get("iteration", 1) >= max_iterations:
            log("finalize", f"⚠️ 已达最大迭代次数（{max_iterations}），强制整合方案书...")
            break
        else:
            log("architect", f"🔄 评审未通过，方案架构师正在修改（第 {state.get('iteration', 1) + 1} 轮）...")
            state.update(node_architect(state))

    # 最终整合
    state.update(node_finalize(state))
    log("done", "📄 方案书生成完毕！")

    return state


# ---------- 5. 测试 ----------
if __name__ == "__main__":
    test_requirement = "我们是一家中小型电商公司，希望引入AI客服来降低人力成本并提升客户满意度。"
    print("🚀 开始运行多Agent协作工作流...\n")
    result = run_workflow(test_requirement)
    
    print("\n" + "="*60)
    print("✅ 最终方案书")
    print("="*60)
    print(result["final_doc"])