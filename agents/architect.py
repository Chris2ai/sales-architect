"""
Agent 2：方案架构师 (Solution Architect)
接收需求分析报告，输出技术方案建议。
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
SYSTEM_PROMPT = """你是一名经验丰富的售前方案架构师。你将收到一份需求分析报告，请你基于此设计一套完整的技术方案。

方案应包含以下部分（使用 Markdown 格式，专业清晰）：
1. **方案总体架构**（文字描述或简单的分层架构）
2. **核心功能模块**（至少3个，每个模块说明其作用与关键技术）
3. **推荐技术栈**（如语言模型选型、中间件、数据库等，注意结合客户已有环境）
4. **部署与扩展建议**（私有化部署、云部署、混合方案）
5. **实施路径**（分阶段建议，如第一阶段、第二阶段）
6. **成本估算**（基于客户规模给出大致人力与资源投入）

请根据需求分析报告的内容，输出具体、可落地的方案，避免空泛的套话。"""

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
def design(analysis_report: str) -> str:
    """输入需求分析报告，返回技术方案。"""
    return chain.invoke({"input": analysis_report})


# ---------- 测试代码 ----------
if __name__ == "__main__":
    # 模拟一份需求分析报告
    sample_analysis = """## 需求分析报告
- **客户背景**：中小型电商公司
- **核心痛点**：人力成本高，客户咨询响应慢
- **关键功能需求**：智能问答、情绪识别与转人工、多轮对话、数据分析看板
- **技术约束**：倾向于云部署，需与现有ERP系统集成
- **预算范围**：中等"""
    print("🏗️ 正在生成技术方案...\n")
    proposal = design(sample_analysis)
    print(proposal)