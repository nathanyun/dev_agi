"""
ChatPDF 是一个基于 Langchain 的 Gradio 应用。
它使用 Langchain 提供的 PDF 解析和向量数据库功能，
并使用 OpenAI 的大模型来回答用户的问题。
"""
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv, find_dotenv

# 加载 OpenAI key 到环境变量
_ = load_dotenv(find_dotenv())

# 定义 prompt模板
prompt_template = PromptTemplate.from_template("""
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
确保你的回复完全依据下述已知信息。不要编造答案。
如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

已知信息:
{documents}

用户问：
{query}

请用中文回答用户问题。
""")


def process_pdf(upload_file):
    print("upload_file ==> ", upload_file)
    # 加载知识库资料
    loader = PyPDFLoader(upload_file[0])
    pages = loader.load_and_split()
    print(f"===正在加载PDF内容并初始化到向量数据库==={str(pages[0])[0:100]}")  # 仅打印第一页前100个字符

    # 将文本向量化并添加到向量数据库中
    db = FAISS.from_documents(pages, OpenAIEmbeddings())
    return db


def chat_func(file_path, question):
    print(question)
    db = process_pdf(file_path)

    # 向量化
    docs = db.similarity_search_by_vector(OpenAIEmbeddings().embed_query(question))
    search_docs = ''.join(doc.page_content for doc in docs)
    print(f"===Similarity Search Completed==>{search_docs[0:100]}")

    prompt = prompt_template.format(documents=search_docs, query=question)  # 将prompt模板定义的参数赋值
    print(f"===Prompt==={prompt}")

    # 调用大模型回复
    llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0)
    response = llm.invoke(prompt)
    print(f"===AI Response==={response.content}")
    return response.content


if __name__ == "__main__":
    # 创建Gradio界面
    interface = gr.Interface(fn=chat_func,
                             inputs=[gr.Files(label="UploadPDF", file_types=["pdf"]),
                                     gr.Textbox(label="Question",
                                                placeholder="您可以问关于PDF中的任何问题",
                                                min_width=500)],
                             outputs=[gr.Textbox(label="Answer")],
                             title="ChatPDF",
                             allow_flagging="never",
                             theme="soft",
                             description="确保您上传的PDF文件是可读的，并且包含您需要的问题的答案。\n\n"
                             )
    # 启动Gradio界面
    interface.launch(share=True)
