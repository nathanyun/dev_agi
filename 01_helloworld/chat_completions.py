from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

# 引入初始化好的OpenAI客户端
client = OpenAI()

# 创建一个聊天对话，让其生成一段文本
response = client.chat.completions.create(
    messages=[
        {"role": "user", "content": "今天天气不错"}
    ],
    model="gpt-3.5-turbo")

# 打印推理内容
print(response.choices[0].message.content)

# {"role": "system", "content": "You are a helpful assistant. 不要跟我对话，直接续写文本"},
