"""
一个使用langchain框架实现的QA问答机器人
基于PDF内容进行RAG embedding，使用OpenAI的gpt-3.5-turbo模型进行问答

依赖：
pip install langchain
pip install langchain-openai
pip install pypdf
pip install faiss-cpu
"""

from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv

# 加载 OpenAI key 到环境变量
_ = load_dotenv(find_dotenv())

query = "llama2有聊天版本吗？"

# 1.加载知识库资料
loader = PyPDFLoader("llama2.pdf")
pages = loader.load_and_split()
print("===Document===")
print(str(pages[0])[0:20])  # 仅打印第一页前20个字符

# 2.将文本向量化并添加到向量数据库中
db = FAISS.from_documents(pages, OpenAIEmbeddings())

# 向量相似度检索
#docs = db.similarity_search(query=query, k=3)
docs = db.similarity_search_by_vector(OpenAIEmbeddings().embed_query(query))
search_docs = ''.join(doc.page_content for doc in docs)

print("===Similarity Search Completed==>" + search_docs[0:50])

# 3 定义 prompt模板
prompt_template = PromptTemplate.from_template("""
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
确保你的回复完全依据下述已知信息。不要编造答案。
如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

已知信息:
{documents}

用户问：
{query}

请用中文回答用户问题，简短回答。
""")
print("===Prompt===")
prompt = prompt_template.format(documents=search_docs, query=query)  # 将prompt模板定义的参数赋值
print(prompt)

# 4.调用大模型回复
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.0)
response = llm.invoke(prompt)
print("===AI Response===")
print(response.content)
