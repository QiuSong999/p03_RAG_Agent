
"""
知识库向量化模块
    主要职责：
        1. 加载 DashScope API 配置。
        2. 创建 Embedding 模型对象。
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings


### 1、获取 P03 项目根目录
base_dir = Path(__file__).resolve().parent.parent

### 2、加载 .env 环境变量
load_dotenv(base_dir / ".env")

### 3、读取 DashScope API Key
api_key = os.getenv("dashscope_api_key")

if not api_key:
    raise ValueError(
        "没有读取到 dashscope_api_key，请检查项目根目录下的 .env 文件"
    )

### 4、初始化 Embedding 模型
embeddings_model = OpenAIEmbeddings(
    model="text-embedding-v3",
    api_key=api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    check_embedding_ctx_length=False,
)
