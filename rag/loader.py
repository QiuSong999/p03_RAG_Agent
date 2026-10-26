"""知识库加载"""
"""
知识库加载模块
    主要职责：
        1. 使用 TextLoader 读取企业规章制度。
        2. 使用 RecursiveCharacterTextSplitter 切分文档。
        3. 返回切分后的 Document 对象列表。
"""


from pathlib import Path
from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter   #文本分割器


### 0、 获取 P03 项目的根目录
base_dir = Path(__file__).resolve().parent.parent
"""
解释结构：
    __file__ ： Python内置变量，代表当前正在运行的 Python 脚本文件的绝对路径（本文件所在的路径）
    Path(__file__ )：把上面的字符串变成一个“路径对象”
    .resolve()：把路径变成绝对路径。有时候 __file__ 拿到的可能是相对路径，加上.resolve() 就会强制解析成完整的绝对路径
    .parent：当前路径的上一级目录。
"""
# 拼接企业规章制度知识库文件路径
knowledge_file = base_dir / "knowledge" / "knowledge.txt"

### 1、加载知识库，并切分文档
def load_and_split_knowledge():
    """
    使用 TextLoader 加载知识库，再将文档切分成多个文本块。
    返回：
        list：切分后的 Document 对象列表。
    """

    ### 2、 检查知识库文件是否存在
    if not knowledge_file.exists():
        raise FileNotFoundError(
            f"知识库文件不存在：{knowledge_file}"
        )

    ### 3、 使用 TextLoader 加载文本文件
    loader = TextLoader(
                        str(knowledge_file),
                        encoding="utf-8",
                        )
    documents = loader.load()

    ### 4、 检查加载结果
    if not documents or not any(
            document.page_content.strip() for document in documents
    ):
        raise ValueError("知识库文件内容为空，请先添加制度资料。")

    ### 5、 创建文本切分器
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=0,
        separators=[
            "\n## ",
            "\n",
            "。",
            "！",
            "？",
            "；",
            "，",
            "",
        ],
    )

    ## 切分 Document 对象（具体的切分动作）
    chunks = text_splitter.split_documents(documents)
    return chunks



if __name__ == "__main__":
    chunks = load_and_split_knowledge()
    print(f"切分后共得到 {len(chunks)} 个文本块")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n~~~~~~~~~~~~第 {index} 个文本块~~~~~~~~~~~~")
        print(chunk)    #输出的是切分好的一个个Document对象
        # ⭐Document 对象确实存在，只是 print(chunk) 展示的是对象的字符串表示，而不是必须带有 Document() 包裹的构造形式
