# -*- coding: utf-8 -*-
"""
Created on 2024-03-06 19:16:56
@author: <nathan yun>
"""
from devagi import get_completion
from devagi.agi_04_rag import build_prompt, extract_text_from_pdf
import rag_03_text_embeddings_by_chromadb as chroma

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
vector_db = chroma.MyVectorDBConnector("demo", chroma.get_embeddings)
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

