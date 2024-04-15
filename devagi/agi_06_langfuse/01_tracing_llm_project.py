import os
import random
import gradio as gr
from dotenv import load_dotenv, find_dotenv
from langchain.schema import AIMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langfuse.callback import CallbackHandler

"""
为什么要做LLM程序的监控和跟踪？
1.捕获执行的完整上下文，包括：API 调用、上下文、提示、并行性等(api calls, context, prompts, parallelism)
2.跟踪模型使用情况和成本(model and cost)
3.收集用户反馈(user feedback)
4.识别低质量输出
5.构建微调和测试数据集（fine-tuning, testing datasets）
"""
# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

# Initialize Langfuse handler
langfuse_handler = CallbackHandler(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host="https://cloud.langfuse.com",  # 🇪🇺 EU region
    # host="https://us.cloud.langfuse.com", # 🇺🇸 US region
    user_id="u188",
    session_id="u188_" + str(random.uniform(30, 50)).replace('.', ''),
    tags=["dev", "test", "prod"]
)


# 定义对话函数
def chat_func(message, history, system_prompt, tokens):
    print(f"System Prompt : {system_prompt}, Tokens : {tokens}")

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
    gr.ChatInterface(chat_func,
                     title='Chatbot',
                     theme='soft',
                     additional_inputs=[
                         gr.Textbox("You are helpful AI.", label="System Prompt"),
                         gr.Slider(10, 100)
                     ]
                     ).launch(share=True)
