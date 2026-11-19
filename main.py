
"""总入口"""
"""
P03 基于 RAG 的 AI Agent 知识库助手入口。
    执行流程：
        1. 接收用户问题。
        2. 将用户问题交给 Agent。
        3. Agent 根据用户问题决定是否调用知识库检索工具。
        4. Agent 根据检索结果生成最终答案。
同时提供 FastAPI 服务。
"""

from fastapi import FastAPI
from pydantic import BaseModel, Field

from agent import ask_agent
import uvicorn


### 1、创建 FastAPI 应用对象，负责接收 HTTP 请求
app = FastAPI(title="P03 RAG Agent 知识库助手")


### 2、定义用户请求的数据结构
class QuestionRequest(BaseModel):
    question: str = Field(min_length=1, description="用户提出的问题")


### 3、定义 Agent 问答入口函数
def agent_qa(question: str) -> str:
    """接收用户问题，调用 Agent，返回最终回答。"""

    # 调用 Agent，内部会完成问题分析、工具调用和答案生成
    answer = ask_agent(question)

    return answer


### 4、定义 GET 接口，访问根路径时返回项目介绍
@app.get("/")
def root():
    return {
        "introduce": "欢迎使用 P03 基于 RAG 的 AI Agent 知识库助手"
    }


### 5、定义 POST 接口，接收用户问题并返回 Agent 回答
@app.post("/ask")
def agent_endpoint(request: QuestionRequest):

    # 获取用户提交的问题
    question = request.question

    # 调用 Agent 问答函数
    answer = agent_qa(question)

    # 将答案作为 JSON 数据返回
    return {
        "question": question,
        "answer": answer
    }


### 6、直接运行当前文件时，启动 FastAPI 服务
if __name__ == "__main__":


    # 启动 FastAPI 服务，允许本机浏览器访问
    uvicorn.run(app, host="127.0.0.1", port=8000)
