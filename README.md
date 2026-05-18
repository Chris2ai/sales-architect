# 🏗️ MultiAgent-SalesArchitect

基于 LangGraph 的三智能体协作售前方案生成系统。输入一句话客户需求，三个 Agent（需求分析师 → 方案架构师 → 技术评审员）自动协作，输出完整的售前方案书。

## ✨ 功能特点

- 🤖 **多 Agent 协作**：需求分析师、方案架构师、技术评审员三个角色自动分工
- 🔄 **循环评审**：评审不通过时，架构师自动修改方案，迭代直到通过或达到最大轮次
- 📄 **专业方案书**：自动生成含封面、目录、需求分析、技术方案、技术评审的完整方案书
- 💬 **多行业适配**：已验证电商、金融等多个行业的需求分析场景
- 🖥️ **Web 界面**：Streamlit 构建的简洁交互界面，开箱即用

## 🛠️ 技术栈

| 组件 | 技术 | 说明 |
|------|------|------|
| 编排框架 | LangGraph | 多 Agent 状态管理与条件分支 |
| Agent 框架 | LangChain | LCEL 链式调用 |
| 大模型 | 通义千问 (qwen-turbo) | 三个 Agent 共用 |
| 前端 | Streamlit | Web 交互界面 |

## 🚀 快速开始

### 环境要求
- Python 3.10+
- Windows / macOS / Linux

### 安装与运行

```bash
# 1. 克隆项目
git clone https://github.com/Chris2ai/sales-architect.git
cd sales-architect

# 2. 创建虚拟环境
python -m venv venv

# 3. 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 安装依赖
pip install -r requirements.txt

# 5. 配置 API Key
# 将 .env.example 复制为 .env，填入你的通义千问 API Key
# 获取地址: https://bailian.console.aliyun.com/

# 6. 运行应用
streamlit run app.py