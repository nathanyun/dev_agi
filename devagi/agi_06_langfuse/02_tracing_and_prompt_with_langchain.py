from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langfuse import Langfuse
from langfuse.callback import CallbackHandler
from dotenv import load_dotenv, find_dotenv
import AgiUtil

"""
使用Langfuse和Langchain的读取prompt演示tracing示例
"""
# 加载 .env 环境变量, 并设置langfuse与openai环境变量
_ = load_dotenv(find_dotenv())

# 初始化Langfuse 客户端 (prompt management)
langfuse = Langfuse()

# 初始化 Langfuse CallbackHandler for Langchain (tracing)
tracing_callback = CallbackHandler()

# Optional, verify that Langfuse is configured correctly
assert langfuse.auth_check()
assert tracing_callback.auth_check()

# 获取 langfuse prompt
langfuse_prompt = langfuse.get_prompt("agi_class_bot")

# 获取 langfuse prompt配置
model = langfuse_prompt.config["model"]
temperature = str(langfuse_prompt.config["temperature"])
print(f"Prompt model configurations\nModel: {model}\nTemperature: {temperature}")


def langchain_invoke():
    # 获取 langchain prompt 格式, 因为langfuse的参数格式是双花括号 {{}} 而langchain是单花括号
    langchain_prompt = langfuse_prompt.get_langchain_prompt()
    print(f"\nLangchainPrompt: {langchain_prompt}")

    # 加载为langchain模板
    prompt = ChatPromptTemplate.from_template(langchain_prompt)

    # 创建OpenAI客户端（langchain）
    llm = ChatOpenAI(model=model, temperature=temperature)

    # parser = StrOutputParser()
    parser = AgiUtil.AGIOutputParser()

    # Build chain with LCEL
    chain = prompt | llm | parser

    # 模拟用户输入示例
    __outlines = """
    LangChain
    模型 I/O 封装
    模型的封装
    模型的输入输出
    PromptTemplate
    OutputParser
    数据连接封装
    文档加载器：Document Loaders
    文档处理器
    内置RAG：RetrievalQA
    记忆封装：Memory
    链架构：Chain/LCEL
    """
    example_input = {
        "outlines": __outlines,
        "user_input": "老师langchain中的LCEL的作用是什么?"
    }

    # 运行chain并监控
    response = chain.invoke(input=example_input, config={"callbacks": [tracing_callback]})
    print(f"\nResponse: {response}")


if __name__ == "__main__":

    langchain_invoke()
