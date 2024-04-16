"""
一个使用langchain框架实现的QA问答机器人
基于PDF内容进行RAG embedding，使用OpenAI的gpt-3.5-turbo模型进行问答

依赖：
pip install langchain
pip install langchain-openai
pip install pypdfium2
pip install chromadb
"""

from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders import PyPDFium2Loader  # Using PyPDFium2
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

query = "llama2有聊天版本吗？"

# 1.加载PDF
loader = PyPDFium2Loader("llama2.pdf")
pages = loader.load()

print("===Document===")
print(pages[0])

# 2.将文本向量化并添加到向量数据库中
# 这langchain 的 chroma版本和chroma官方版本兼容有问题，跑不通
db = Chroma.from_documents(pages, OpenAIEmbeddings())
# docs = db.similarity_search(query)
# print(docs[0].page_content)

"""
报错：
ValueError: Expected EmbeddingFunction.__call__ to have the following signature: odict_keys(['self', 'input']), got odict_keys(['args', 'kwargs'])
Please see https://docs.trychroma.com/embeddings for details of the EmbeddingFunction interface.
Please note the recent change to the EmbeddingFunction interface: https://docs.trychroma.com/migration#migration-to-0416---november-7-2023 
"""