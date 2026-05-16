"""
Agent 1：需求分析师 (Requirement Analyst)
接收用户一句话需求，输出结构化需求分析。
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

# ---------- System Prompt ----------
SYSTEM_PROMPT = """你是一名资深的售前需求分析师。你的任务是把客户模糊的一句话需求，转化为结构化的需求分析报告。

分析报告应包含以下六个维度（如果客户需求中未提及某项，请基于行业常识合理推断）：
1. 客户背景与行业
2. 核心痛点与业务目标
3. 关键功能需求（至少列出3项）
4. 技术约束与偏好（如部署方式、现有系统集成、性能要求）
5. 预算与时间范围（根据客户规模合理推断）
6. 潜在风险与注意事项

输出格式：用 Markdown 标题层级组织，语言专业简洁。"""

# ---------- 构建链 ----------
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}"),
])

llm = ChatOpenAI(
    model="qwen-turbo",
    openai_api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.7,
)

chain = prompt | llm | StrOutputParser()

# ---------- 调用函数 ----------
def analyze(requirement: str) -> str:
    """输入一句话需求，返回结构化需求分析报告。"""
    return chain.invoke({"input": requirement})


# ---------- 测试代码 ----------
if __name__ == "__main__":
    test_input = "我们是一家中小型电商公司，希望引入AI客服来降低人力成本并提升客户满意度。"
    print("📋 正在分析需求...\n")
    report = analyze(test_input)
    print(report)