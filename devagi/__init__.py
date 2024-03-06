import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json

"""
Tips：确保.env已经配置， 注意请更换.evn环境变量配置的GPT key

注意，如果无法导入 openai 和 dotenv 包，需要在下载如下依赖：
pip install python-dotenv openai

若无法下载依赖包，请更换pip国内镜像源，换源后再重新下载依赖，例如设置为清华源：
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
"""

# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

#  初始化OpenAI客户端
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)


#  OpenAI chat completions
def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.0):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content


def print_pretty(data):
    # 如果datab中包含model_dump_json字段， 将其转为JSON对象
    if hasattr(data, 'model_dump_json'):
        data = json.load(data.model_dump_json())

    # 若包含列表或字典， 格式为JSON字符串打印, 否则原样打印
    if isinstance(data, (list, dict)):
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print(data)
