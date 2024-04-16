"""
一个使用langchain框架实现的QA问答机器人
基于PDF内容进行RAG embedding，使用OpenAI的gpt-3.5-turbo模型进行问答

依赖：
pip install langchain
pip install langchain-openai
pip install pypdf 或 pip install pypdfium2   看你用哪个加载器了
pip install faiss-cpu 来支持FAISS 包
"""

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import PyPDFium2Loader   # Using PyPDFium2
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv

# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

query = "llama2有聊天版本吗？"

# 加载PDF
loader = PyPDFLoader("llama2.pdf")
pages = loader.load_and_split()
# loader = PyPDFium2Loader("llama2.pdf")
# pages = loader.load()

print("===Document===")
print(pages[0])

# 将文本向量化并添加到向量数据库中
db = FAISS.from_documents(pages, OpenAIEmbeddings())

# 相似度检索
#docs = db.similarity_search(query='chat', k=20)

# 向量相似度检索
docs = db.similarity_search_by_vector(OpenAIEmbeddings().embed_query(query))
print(docs[0].page_content)

print("===Similarity Search===")
for doc in docs:
    print(str(doc.metadata["page"]) + "==>", doc.page_content[:10])


