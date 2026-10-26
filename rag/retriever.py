"""存入数据库并检索"""
"""
知识库向量存储与检索模块
    主要职责：
        1. 加载切分后的 Document 对象。
        2. 创建 Redis 向量库。
        3. 将 Document 对象存入 Redis。
        4. 根据用户问题检索相关文档。
"""

from pathlib import Path

from dotenv import load_dotenv
from langchain_redis import RedisConfig, RedisVectorStore   #导入redis依赖

from rag.loader import load_and_split_knowledge     #导入加载和分割函数
from rag.embedding import embeddings_model          #导入bedding 模型


### 1、获取 P03 项目根目录
base_dir = Path(__file__).resolve().parent.parent

### 2、加载 .env 环境变量
load_dotenv(base_dir / ".env")


### 3、创建 Redis 向量库配置
config = RedisConfig(
    index_name="p03_enterprise_policy",
    redis_url="redis://192.168.88.130:6379",
)


### 4、创建 Redis 向量库对象
vector_store = RedisVectorStore(
    embeddings_model,
    config=config,
)


### 5、构建知识库并存入 Redis
def build_knowledge_base():
    """
    加载并切分企业规章制度，
    将 Document 对象列表存入 Redis。
    """

    # 调用函数：加载并切分知识库
    chunks = load_and_split_knowledge()

    ## 将 Document 对象存入 Redis
    ids = vector_store.add_documents(chunks)

    print(f"知识库切分得到 {len(chunks)} 个文本块")
    print(f"成功存入 {len(ids)} 个文档")
    print(f"前 5 个文档 ID：{ids[:5]}")

    return vector_store


### 6、获取检索器
def get_retriever():
    """
    将向量库转换为检索器，每次检索返回最相关的 2 个文档。
    """

    return vector_store.as_retriever(
        search_kwargs={"k": 2}
    )

"""
构建知识库：build_knowledge_base() → add_documents(chunks)，向 Redis 写入文档。

查询知识库：get_retriever() → retriever.invoke(question)，检索文档，不会主动写入。
"""


### 7、测试知识库存储与检索
if __name__ == "__main__":

    # 构建知识库并存入 Redis（首次时需要，后续只检索就不需要存了）
    build_knowledge_base()

    # 创建检索器
    retriever = get_retriever()

    # 设置测试问题
    query = "员工报销时需要提交哪些材料？"

    # 执行检索
    results = retriever.invoke(query)

    print(f"\n检索问题：{query}")

    for index, document in enumerate(results, start=1):
        print(f"\n~~~~~~~~~检索结果 {index}~~~~~~~~~")
        print("文本内容：", document.page_content)
        print("元数据：", document.metadata)
