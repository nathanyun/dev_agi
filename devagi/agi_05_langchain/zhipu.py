from zhipuai import ZhipuAI
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

# 安装智普依赖
# pip install --upgrade zhipuai
api_key = os.getenv("ZHI_API_KEY")

client = ZhipuAI(api_key=api_key)  # 填写您自己的APIKey
response = client.chat.completions.create(
    model="glm-4",  # 填写需要调用的模型名称
    messages=[
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
        {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "跨境汇款"},
        {"role": "assistant", "content": "轻松跨越，汇款无界——让您的资金在全球自由流转。"},
        {"role": "user", "content": "还行吧，再请准一点"}
    ],
)
print(response.choices[0].message)