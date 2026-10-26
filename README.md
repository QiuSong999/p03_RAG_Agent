# P03：基于 RAG 的 AI Agent 企业知识库助手

## 一、项目介绍

本项目使用 LangChain、RAG（检索增强生成）和 AI Agent 构建企业规章制度知识库助手。

用户可以通过自然语言询问企业制度相关问题，AI Agent 根据问题调用知识库检索工具，检索相关制度内容，再结合检索结果生成回答。

## 二、项目功能

- 加载企业规章制度文本。
- 使用文本分割器将知识库切分为多个文本块。
- 使用 DashScope `text-embedding-v3` 模型生成文本向量。
- 使用 Redis 向量存储保存知识库内容。
- 根据用户问题检索相关制度文本。
- 使用 LangChain Agent 调用知识库检索工具。
- 使用大语言模型生成制度问答结果。

## 三、技术栈

- Python
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
├── knowledge/
│   └── knowledge.txt
├── rag/
│   ├── embedding.py
│   ├── loader.py
│   ├── retriever.py
│   └── tools.py
├── .gitignore
└── README.md
```

## 五、核心模块说明

### 1. agent.py

创建 AI Agent，配置大语言模型、系统提示词和知识库检索工具，处理用户提出的问题。

### 2. knowledge/knowledge.txt

存放企业规章制度文本，作为 RAG 知识库的数据来源。

### 3. rag/loader.py

使用 `TextLoader` 加载知识库，并使用 `RecursiveCharacterTextSplitter` 切分文本，返回 `Document` 对象列表。

### 4. rag/embedding.py

配置 DashScope Embedding 模型，将文本转换为向量表示。

### 5. rag/retriever.py

负责将知识库文本存入 Redis 向量存储，并根据用户问题检索相关文档。

### 6. rag/tools.py

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
3. 安装项目所需的 Python 依赖。
4. 确认 `.env` 中已配置有效的 DashScope API Key。
5. 确认 Linux 虚拟机中的 Redis 服务已启动，且 Windows 主机可以连接 Redis。
6. 在 PyCharm 中运行 `agent.py`，按照该文件当前定义的入口进行交互。

## 九、项目流程

```text
用户问题
   ↓
AI Agent
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
返回用户
```

## 十、项目目标

通过本项目学习并实践 RAG、向量检索、工具调用和 AI Agent 的协作方式，理解如何让大语言模型结合企业知识库回答问题。