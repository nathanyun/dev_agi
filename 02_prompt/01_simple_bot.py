"""
实现一个多轮对话的流量推荐客服助手
"""

import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

# 加载.env配置文件(代码中，_ 是一个占位符，表示忽略返回值。)
_ = load_dotenv(find_dotenv())


def print_json(data):
    # 如果datab中包含model_dump_json字段， 将其转为JSON对象
    if hasattr(data, 'model_dump_json'):
        data = json.load(data.model_dump_json())

    # 若包含列表或字典， 格式为JSON字符串打印, 否则原样打印
    if isinstance(data, (list, dict)):
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print(data)


# 初始化OpenAI客户端
client = OpenAI()

# 定义 message ，指定system基本要求
message = [
    {
        "role": "system",
        "content": """
你是一个手机流量套餐的客服代表，你叫Bonny。可以帮助用户选择最合适的流量套餐产品，除此之外你不可以回答其他问题。可以选择的套餐包括：
- 经济套餐，月费50元，10G流量
- 畅游套餐，月费180元，100G流量
- 无限套餐，月费300元，1000G流量
- 校园套餐，月费150元，200G流量(仅限学生)。
"""
    }
]


# 多轮对话 assistant记录历史对话
def get_completion(prompt):
    # 把用户的prompt追加到message中
    message.append({"role": "user", "content": prompt})

    # 调用OpenAI客户端生成内容
    response = client.chat.completions.create(model="gpt-3.5-turbo",
                                              messages=message,
                                              temperature=0)
    # 获取结果
    msg = response.choices[0].message.content

    # 将结果再写入 assistant角色：加入历史消息，否则下次调用模型时，模型拿不到上下文
    message.append({"role": "assistant", "content": msg})
    return msg


# 发起对话
get_completion('你们都有哪些套餐啊？')
get_completion('不好意思，我没记住，最便宜的套餐是多少钱啊，我平时就刷刷抖音流量够用嘛？')
get_completion('10个G不太够用，有没有那种流量大一点的？')
get_completion('有没有50块以内的那种流量多一点的套餐？')
get_completion('我是学生，有合适的套餐推荐吗？')
get_completion('你工号多少？')
print_json(message)
