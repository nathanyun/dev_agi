# -*- coding: utf-8 -*-
"""
Created on 2024-03-06 19:16:56
@author: <nathan yun>
"""
import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from util import extract_text_from_pdf, build_prompt
from chromadb.config import Settings
import chromadb

# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

#  初始化OpenAI客户端
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


#  OpenAI chat completions
def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.0):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content

def get_embeddings(texts, model="text-embedding-ada-002", dimensions=None):
    # 封装 OpenAI 的 Embedding 模型接口
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


prompt_template = """
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
确保你的回复完全依据下述已知信息。不要编造答案。
如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

已知信息:
__INFO__

用户问：
__QUERY__

请用中文回答用户问题。
"""

"""
定义一个RAG Bot类,该类将使用向量数据库和语言模型进行交互。
"""


class RagBot:
    def __init__(self, vector_db, llm_api, n_results=2):
        self.vector_db = vector_db
        self.llm_api = llm_api
        self.n_results = n_results

    def chat(self, user_query):
        # 1. 检索
        search_results = self.vector_db.search(user_query, self.n_results)

        # 2. 构建 Prompt
        prompt = build_prompt(
            prompt_template, info=search_results['documents'][0], query=user_query)

        # 3. 调用 LLM
        response = self.llm_api(prompt)
        return response


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

# 创建一个RAG机器人
bot = RagBot(
    vector_db,
    llm_api=get_completion
)

user_query = "llama 2有对话版吗？"

response = bot.chat(user_query)
print(response)
