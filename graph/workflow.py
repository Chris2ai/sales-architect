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

# ---------- 2. 定义三个 Node（每个节点调用一个 Agent） ----------
def node_analyst(state: WorkflowState) -> WorkflowState:
    """节点1：需求分析"""
    print("📋 [1/3] 需求分析师正在分析...")
    analysis_result = analyze(state["raw_requirement"])
    return {"analysis": analysis_result}

def node_architect(state: WorkflowState) -> WorkflowState:
    """节点2：方案设计"""
    print("🏗️ [2/3] 方案架构师正在设计方案...")
    proposal_result = design(state["analysis"])
    return {"proposal": proposal_result}

def node_reviewer(state: WorkflowState) -> WorkflowState:
    """节点3：技术评审"""
    print("🔍 [3/3] 技术评审员正在评审方案...")
    review_result = review(state["proposal"])
    return {"review": review_result}

def node_finalize(state: WorkflowState) -> WorkflowState:
    """节点4：整合最终方案书"""
    print("📄 正在整合方案书...")
    final = f"""# 售前方案书

## 一、需求分析
{state["analysis"]}

## 二、技术方案
{state["proposal"]}

## 三、技术评审
{state["review"]}
"""
    return {"final_doc": final}

# ---------- 3. 构建 Graph ----------
graph = StateGraph(WorkflowState)

# 添加节点
graph.add_node("analyst", node_analyst)
graph.add_node("architect", node_architect)
graph.add_node("reviewer", node_reviewer)
graph.add_node("finalize", node_finalize)

# 添加边（线性流程）
graph.set_entry_point("analyst")
graph.add_edge("analyst", "architect")
graph.add_edge("architect", "reviewer")
graph.add_edge("reviewer", "finalize")
graph.add_edge("finalize", END)

# 编译
app = graph.compile()

# ---------- 4. 调用函数 ----------
def run_workflow(raw_requirement: str) -> WorkflowState:
    """输入原始需求，运行完整工作流，返回包含所有阶段的 State"""
    initial_state = WorkflowState(
        raw_requirement=raw_requirement,
        analysis="",
        proposal="",
        review="",
        final_doc="",
    )
    return app.invoke(initial_state)


# ---------- 5. 测试 ----------
if __name__ == "__main__":
    test_requirement = "我们是一家中小型电商公司，希望引入AI客服来降低人力成本并提升客户满意度。"
    print("🚀 开始运行多Agent协作工作流...\n")
    result = run_workflow(test_requirement)
    
    print("\n" + "="*60)
    print("✅ 最终方案书")
    print("="*60)
    print(result["final_doc"])