"""
Agent 3：技术评审员 (Tech Reviewer)
接收方案架构师的输出，进行技术评审并提供改进建议。
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
SYSTEM_PROMPT = """你是一名严谨的技术评审专家，负责对售前技术方案进行评审。

评审报告请包含以下内容（Markdown格式）：
1. **总体评价**（一句话总结方案的优缺点）
2. **可行性评估**（技术选型是否合理，架构是否可落地）
3. **风险点识别**（列出至少2个潜在风险，并说明理由）
4. **改进建议**（对方案提出具体、可操作的优化建议）
5. **是否通过**（给出“通过”、“有条件通过”或“不通过”的结论，并解释原因）

请基于提供的技术方案内容进行评审，语言专业、客观。"""

# ---------- 构建链 ----------
prompt = ChatPromptTemplate.from_messages([
    ("system", SYSTEM_PROMPT),
    ("human", "{input}"),
])

llm = ChatOpenAI(
    model="qwen-turbo",
    openai_api_key=os.getenv("DASHSCOPE_API_KEY"),
    openai_api_base="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=0.3,  # 评审需要更严谨
)

chain = prompt | llm | StrOutputParser()

# ---------- 调用函数 ----------
def review(proposal: str) -> str:
    """输入技术方案，返回评审报告。"""
    return chain.invoke({"input": proposal})


# ---------- 测试代码 ----------
if __name__ == "__main__":
    # 模拟一份技术方案
    sample_proposal = """## 技术方案
- **总体架构**：基于微服务架构，前端使用React，后端使用Spring Cloud
- **核心模块**：智能问答引擎、情绪分析服务、数据分析平台
- **推荐技术栈**：通义千问API、Redis、MySQL
- **部署方式**：阿里云ECS，Docker容器化
- **实施计划**：第一阶段上线FAQ问答，第二阶段接入情绪识别"""
    print("🔍 正在评审方案...\n")
    report = review(sample_proposal)
    print(report)