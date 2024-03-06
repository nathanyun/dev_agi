# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:03:59 2018
@author: <nathan yun>

chromadb是一个开源的嵌入式向量数据库, 官方文档：https://docs.trychroma.com/

pip install chromadb
"""
import chromadb
from chromadb.config import Settings
from devagi.agi_04_rag import extract_text_from_pdf
from devagi import client


def get_embeddings(texts, model="text-embedding-ada-002", dimensions=None):
    """封装 OpenAI 的 Embedding 模型接口"""
    if model == "text-embedding-ada-002":
        dimensions = None
    if dimensions:
        data = client.embeddings.create(input=texts, model=model, dimensions=dimensions).data
    else:
        data = client.embeddings.create(input=texts, model=model).data
    return [x.embedding for x in data]


# 定义一个向量的函数，用于向 chroma 添加或检索文档
class MyVectorDBConnector:
    def __init__(self, collection_name, embedding_fn):
        settings = Settings(allow_reset=True)
        # 创建一个 chroma 客户端
        chroma_client = chromadb.Client(settings)

        # 为了演示，实际不需要每次 reset()
        chroma_client.reset()

        # 创建一个 collection
        self.collection = chroma_client.get_or_create_collection(name=collection_name)
        self.embedding_fn = embedding_fn

    def add_documents(self, documents):
        """向 collection 中添加文档与向量"""
        self.collection.add(
            embeddings=self.embedding_fn(documents),  # 每个文档的向量
            documents=documents,  # 文档的原文
            ids=[f"id{i}" for i in range(len(documents))]  # 每个文档的 id
        )

    def search(self, query, top_n):
        """检索向量数据库"""
        results = self.collection.query(
            query_embeddings=self.embedding_fn([query]),
            n_results=top_n
        )
        return results


# 读取PDF文件，并提取需要的内容
paragraphs = extract_text_from_pdf(
    "llama2.pdf",
    page_numbers=[2, 3],
    min_line_length=10
)

# 创建一个向量数据库对象
vector_db = MyVectorDBConnector("demo", get_embeddings)
# 向向量数据库中添加文档（从PDF读取的数据）
vector_db.add_documents(paragraphs)

user_query = "Llama 2有多少参数"
results = vector_db.search(user_query, 2)

# 打印检索结果
for para in results['documents'][0]:
    print(para+"\n")