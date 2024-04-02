from langchain_openai import ChatOpenAI
from dotenv import load_dotenv, find_dotenv

# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

# 一个简单的langchain示例
llm = ChatOpenAI(model='gpt-3.5-turbo', temperature=0.5)
response = llm.invoke(["中国的首都是哪里?"])
print(response.content)