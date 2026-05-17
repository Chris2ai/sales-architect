"""
LangGraph 入门示例：一个简单的三步计算流程
演示 State、Node、Edge 的基本用法
"""
from typing import TypedDict
from langgraph.graph import StateGraph, END

# 1. 定义 State（在整个流程中传递的数据结构）
class CalculatorState(TypedDict):
    number: int          # 当前数值
    history: list[str]   # 操作历史记录

# 2. 定义三个 Node（处理节点）
def add_two(state: CalculatorState) -> CalculatorState:
    """第一步：加 2"""
    number = state["number"] + 2
    history = state["history"] + [f"加2 → {number}"]
    print(f"🔵 加2 节点：{state['number']} + 2 = {number}")
    return {"number": number, "history": history}

def multiply_three(state: CalculatorState) -> CalculatorState:
    """第二步：乘 3"""
    number = state["number"] * 3
    history = state["history"] + [f"乘3 → {number}"]
    print(f"🟢 乘3 节点：{state['number']} * 3 = {number}")
    return {"number": number, "history": history}

def subtract_five(state: CalculatorState) -> CalculatorState:
    """第三步：减 5"""
    number = state["number"] - 5
    history = state["history"] + [f"减5 → {number}"]
    print(f"🟡 减5 节点：{state['number']} - 5 = {number}")
    return {"number": number, "history": history}

# 3. 构建 Graph
graph = StateGraph(CalculatorState)

# 添加节点
graph.add_node("add_two", add_two)
graph.add_node("multiply_three", multiply_three)
graph.add_node("subtract_five", subtract_five)

# 添加边（定义执行顺序）
graph.set_entry_point("add_two")          # 从 add_two 开始
graph.add_edge("add_two", "multiply_three")   # add_two 执行后去 multiply_three
graph.add_edge("multiply_three", "subtract_five")  # 然后去 subtract_five
graph.add_edge("subtract_five", END)           # 最后结束

# 4. 编译为可执行对象
app = graph.compile()

# 5. 测试运行
if __name__ == "__main__":
    print("🚀 运行 LangGraph 示例：")
    print("初始值: 10\n")
    
    result = app.invoke({"number": 10, "history": []})
    
    print(f"\n✅ 最终结果: {result['number']}")
    print(f"📜 操作历史: {result['history']}")