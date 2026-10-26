"""封装成可调用的工具"""
"""
企业规章制度检索工具
    主要职责：
        1. 调用 Redis 检索器查询企业规章制度。
        2. 将检索结果整理成文本。
        3. 将查询功能封装成 Agent 可以调用的 Tool。
"""

from langchain.tools import tool

from rag.retriever import get_retriever

### 1、将检索工具封装成查询工具
@tool
def search_company_policies(question: str) -> str:
    """
    查询企业规章制度知识库。
    当用户询问公司考勤、请假、费用报销、出差、
    办公设备或信息安全制度时，调用此工具检索相关规定。

    参数：
        question：用户想查询的企业制度问题。
    返回：
        检索到的制度文本。
    """
    ## 1.1 获取 Redis 检索器
    retriever = get_retriever()

    ## 1.2 根据问题检索相关文档
    documents = retriever.invoke(question)
    """
    document是检索到的两条内容
        结构为：
        documents = [
                      Document(page_content="请假应提前提交申请。一天以内的事假或年假由直属主管审批。"),
                      Document(page_content="超过一天的事假或年假，需直属主管审核并由部门负责人审批。")
                    ]
    """

    ## 1.3 没有检索到相关文档
    if not documents:
        return "知识库中没有检索到相关制度资料。"

    ## 1.4 提取检索结果中的文本内容
    results = []

    for index, document in enumerate(documents, start=1):
        results.append(
            f"制度资料 {index}：\n{document.page_content}"
        )
    """
    从每个 Document 中提取 page_content，并添加编号和标题,添加到列表中
    此时 results 是一个 字符串列表 list[str],即
         result=[
                  "制度资料 1：\n请假应提前提交申请。一天以内的事假或年假由直属主管审批。",
                  "制度资料 2：\n超过一天的事假或年假，需直属主管审核并由部门负责人审批。"
                ]
    """

    # 将多个检索结果合并成一个字符串
    return "\n\n".join(results)     #把列表中的多个字符串拼接成一个完整字符串，中间用两个换行符分隔
    """
    最终返回的是纯字符串，如
        制度资料 1：
        请假应提前提交申请。一天以内的事假或年假由直属主管审批。
        
        制度资料 2：
        超过一天的事假或年假，需直属主管审核并由部门负责人审批。
    """

    #最终流程为：Redis 返回文档对象 → 工具提取文档文本 → 返回字符串 → Agent 根据文本生成最终答案。
