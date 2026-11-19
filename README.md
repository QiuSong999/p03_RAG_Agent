# P03：基于 RAG 的 AI Agent 企业知识库助手

## 一、项目介绍

本项目使用 LangChain、RAG（检索增强生成）、AI Agent 和 FastAPI 构建企业规章制度知识库助手。

用户可以通过自然语言询问企业制度相关问题，AI Agent 根据问题决定是否调用知识库检索工具，检索相关制度内容，再结合检索结果生成回答。

同时，项目使用 FastAPI 提供 HTTP 接口，允许用户通过 API 提交问题并获取 AI Agent 的回答。

## 二、项目功能

- 加载企业规章制度文本。
- 使用文本分割器将知识库切分为多个文本块。
- 使用 DashScope `text-embedding-v3` 模型生成文本向量。
- 使用 Redis 向量存储保存知识库内容。
- 根据用户问题检索相关制度文本。
- 使用 LangChain Agent 调用知识库检索工具。
- 使用大语言模型生成制度问答结果。
- 使用 FastAPI 提供 HTTP 问答接口。
- 使用 Pydantic 定义和校验用户请求数据。
- 提供 FastAPI 自动生成的 Swagger API 文档。

## 三、技术栈

- Python
- FastAPI
- Uvicorn
- Pydantic
- LangChain
- LangChain Agent
- RAG
- Embedding
- Redis 向量存储
- DashScope API
- Qwen 模型

## 四、项目结构

```text
p03_RAG_Agent/
├── agent.py
├── main.py
├── knowledge/
│   └── knowledge.txt
├── rag/
│   ├── embedding.py
│   ├── loader.py
│   ├── retriever.py
│   └── tools.py
├── .env
├── .gitignore
└── README.md
```

## 五、核心模块说明

### 1. agent.py

创建 AI Agent，配置大语言模型、系统提示词和知识库检索工具，处理用户提出的问题。

提供 `ask_agent()` 函数，接收用户问题并返回 Agent 生成的最终回答。

### 2. main.py

项目总入口，使用 FastAPI 提供 HTTP 服务。

主要功能：

- 创建 FastAPI 应用对象。
- 使用 Pydantic 定义用户请求数据结构。
- 定义 `agent_qa()` 函数，调用 Agent 处理用户问题。
- 提供 GET `/` 接口，返回项目介绍。
- 提供 POST `/ask` 接口，接收用户问题并返回 Agent 回答。
- 使用 Uvicorn 启动 FastAPI 服务。

### 3. knowledge/knowledge.txt

存放企业规章制度文本，作为 RAG 知识库的数据来源。

### 4. rag/loader.py

使用 `TextLoader` 加载知识库，并使用 `RecursiveCharacterTextSplitter` 切分文本，返回 `Document` 对象列表。

### 5. rag/embedding.py

配置 DashScope Embedding 模型，将文本转换为向量表示。

### 6. rag/retriever.py

负责将知识库文本存入 Redis 向量存储，并根据用户问题检索相关文档。

### 7. rag/tools.py

定义知识库检索工具，供 AI Agent 根据问题调用。

## 六、运行环境

- Windows
- Python 3.12
- PyCharm
- Redis（运行在 Linux 虚拟机的 Docker 容器中）
- DashScope API

## 七、环境变量配置

在项目根目录创建 `.env` 文件，并配置自己的 DashScope API Key：

```dotenv
dashscope_api_key=你的DashScope_API_Key
```

注意：请使用自己的有效 API Key，不要将 `.env` 文件上传到 GitHub。

## 八、运行说明

1. 使用 PyCharm 打开项目。
2. 选择项目对应的 Python 虚拟环境。
3. 安装项目所需的 Python 依赖，包括 FastAPI 和 Uvicorn。
4. 确认 `.env` 中已配置有效的 DashScope API Key。
5. 确认 Linux 虚拟机中的 Redis 服务已启动，且 Windows 主机可以连接 Redis。
6. 在 PyCharm 中运行 `main.py`，启动 FastAPI 服务。
7. 服务启动后，可以通过以下地址访问：

   - 项目介绍：`http://127.0.0.1:8000/`
   - API 文档：`http://127.0.0.1:8000/docs`
   - 问答接口：`POST http://127.0.0.1:8000/ask`

### POST /ask 请求示例

请求 JSON：

```json
{
    "question": "请假一天需要谁审批？"
}
```

返回 JSON：

```json
{
    "question": "请假一天需要谁审批？",
    "answer": "根据企业规章制度，一天以内的事假或年假由直属主管审批。"
}
```

## 九、项目流程

```text
用户通过 HTTP 接口提交问题
        ↓
FastAPI 接收请求
        ↓
main.py 调用 ask_agent()
        ↓
AI Agent 分析用户问题
        ↓
判断是否需要调用知识库工具
        ↓
search_company_policies
        ↓
Redis 向量检索
        ↓
返回相关制度文本
        ↓
大语言模型生成回答
        ↓
FastAPI 返回 JSON 响应
        ↓
用户获取最终答案
```

## 十、项目目标

通过本项目学习并实践 RAG、向量检索、工具调用、AI Agent 和 FastAPI 的协作方式，理解如何让大语言模型结合企业知识库回答问题，并通过 HTTP API 将 AI Agent 封装成可供外部系统调用的服务。