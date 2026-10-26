
"""
P03：AI Agent 核心模块
负责创建 Agent，并提供统一的问答入口。
"""

### 0、导入依赖
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from rag.tools import search_company_policies   #封装成工具的检索函数


### 1、 加载项目根目录下的环境变量
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

api_key = os.getenv("dashscope_api_key")

if not api_key:
    raise ValueError(
        "没有读取到 dashscope_api_key，请检查项目根目录下的 .env 文件"
    )


### 2、 创建 Qwen 模型对象
llm = ChatOpenAI(
    model="qwen-plus",
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


### 3、 创建 Agent
agent = create_agent(
    model=llm,
    tools=[search_company_policies],
    system_prompt=(
        "你是一个严谨的企业规章制度知识库助手。"
        "当用户询问考勤、请假、费用报销、出差、办公设备或信息安全制度时，"
        "必须调用 search_company_policies 工具查询知识库。"

        "回答必须以工具返回的制度资料为依据。"
        "只能将资料中明确记载的内容表述为公司制度规定。"
        "不得编造制度条款、审批要求、材料清单、金额上限或处罚标准。"
        "不得将相关制度中提到的事项，直接推断为用户所问事项的强制要求。"
        "例如，出差制度要求提交出差总结，不代表报销时必须提交出差总结。"

        "如果资料没有明确回答用户的问题，"
        "必须明确说明现有知识库无法确认，"
        "并区分资料中已经明确的信息与尚未明确的信息。"
        "可以建议用户咨询人力资源部门或相关负责人，"
        "但不得将建议表述为公司已经规定的要求。"
        
        "不得自行举例补充资料中没有列出的票据、凭证或审批环节。"
        "回答用户询问的具体事项时，只提供与问题直接相关的制度内容。"
        "不得为了让回答显得完整而补充推测、常见做法或经验性建议。"
        "如果资料只规定了原则，没有列出具体材料或流程，"
        "必须保留这一限制，不得自行扩展细节。"
        
        "回答必须遵守最小充分原则。"
        "回答前必须先判断用户具体询问的事项，并筛选直接回答该问题所必需的原文信息。"
        "只输出直接回答问题所必需的内容，不输出其他相关制度条款。"
        "当用户询问需要提交哪些材料时，只列出原文明确规定需要提交的材料，"
        "以及原文明确要求在申请中注明的信息。"
        "不得把提交材料、申请填写信息、审批流程、费用标准和事后总结混为一类。"
        "即使其他制度条款与问题相关，也不能仅因为相关就加入回答。"
        
        "优先直接回答用户的问题，不主动扩展相关制度。"
        "除非用户明确要求举例，否则不得添加制度原文没有列出的具体示例。"
        "不得把不同制度中的要求合并成用户所问事项的额外必备条件。"
        "不要罗列用户没有询问的材料、流程或例外情况。"
        "回答制度问题时，优先使用简洁的条目；资料没有明确规定的内容，只需简短说明无法确认。"

        "请使用清晰、简洁的中文回答。"
    ),
)
"""
system_prompt 已经包含了三类约束：
    1. 事实约束：只能依据工具检索到的制度资料回答。
    2. 范围约束：只回答用户询问的具体事项，不混入其他制度要求。
    3. 输出约束：遵守最小充分原则，不主动扩展内容。
"""

### 4、调用agent
def ask_agent(question: str) -> str:
    """
    接收用户问题，调用 Agent，并返回最终回答。
    """
    result = agent.invoke(
        {
            "messages": [
                            {
                                "role": "user",
                                "content": question,
                            }
                        ]
        }
    )

    # 获取最后一条消息，即 Agent 最终返回的消息
    return result["messages"][-1].content

# 用户提问 → Agent 决定调用 Tool → Tool 检索 Redis → 返回检索结果 → Agent 生成回答。
# Agent：分析问题、决定调用工具、生成最终回答。
# Tool：执行具体任务，例如调用检索器查询知识库。
# Redis：存储知识库数据，供检索器查询

if __name__ == '__main__':
    question = "员工报销时需要提交哪些材料？"

    answer = ask_agent(question)

    print("用户问题：", question)
    print("\nAgent 回答：")
    print(answer)
