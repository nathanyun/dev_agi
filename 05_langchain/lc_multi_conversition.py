from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv
from langchain.schema import (
    AIMessage,  # 等价于OpenAI接口中的assistant role
    HumanMessage,  # 等价于OpenAI接口中的user role
    SystemMessage  # 等价于OpenAI接口中的system role
)


# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

# 定义模型
llm = ChatOpenAI(temperature=0.5)

# 多轮对话示例
messages = [
    SystemMessage(content="你是课程助理。"),
    HumanMessage(content="我是学员，我叫Jack，来自火星"),
    AIMessage(content="欢迎！"),
    HumanMessage(content="我是谁，我来自哪里？")
]

ret = llm.invoke(messages)

print(ret.content)