import os

import gradio as gr
from dotenv import load_dotenv, find_dotenv
from langchain.schema import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

# Initialize Langfuse handler
from langfuse.callback import CallbackHandler

langfuse_handler = CallbackHandler(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host="https://cloud.langfuse.com",  # 🇪🇺 EU region
    # host="https://us.cloud.langfuse.com", # 🇺🇸 US region
)

"""
message: 用户输入
history: 对话历史
"""

# 定义对话函数
def chat_func(message, history):
    """langchain 多轮对话"""
    history_langchain_format = []
    for human, ai in history:
        history_langchain_format.append(HumanMessage(content=human))
        history_langchain_format.append(AIMessage(content=ai))

    # 添加用户输入到历史记录
    history_langchain_format.append(HumanMessage(content=message))

    llm = ChatOpenAI(temperature=1.0, model='gpt-3.5-turbo-0613')

    # Add Langfuse handler as callback (classic and LCEL)
    gpt_response = llm.invoke(history_langchain_format, config={"callbacks": [langfuse_handler]})
    return gpt_response.content


if __name__ == "__main__":
    # 启用gradio
    gr.ChatInterface(chat_func, title='Chatbot', theme='soft').launch(share=True)
