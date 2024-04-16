from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json

_ = load_dotenv(find_dotenv())

client = OpenAI()


def get_completions_choices(messages, tools, model="gpt-3.5-turbo", temperature=0.7):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        seed=1024,  # 随机种子保持不变，temperature 和 prompt 不变的情况下，输出就会不变
        tool_choice="auto",  # 默认值，由 GPT 自主决定返回 function call 还是返回文字回复。也可以强制要求必须调用指定的函数
        # 模型可能调用的工具列表。目前，仅支持将函数作为工具。使用它来提供模型可能为其生成 JSON 输入的函数列表。
        tools=tools
    )
    if response and response.choices and response.choices[0].message:
        return response.choices[0].message
    return None


# 需求：从一段文字中提取联系人姓名、地址、电话号码
tools = [{
    "type": "function",
    "function": {
        "name": "get_address_info",
        "description": "提取联系人姓名电话与地址",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "姓名"
                },
                "phone_number": {
                    "type": "string",
                    "description": "电话号码"
                },
                "address": {
                    "type": "string",
                    "description": "联系地址"
                }
            }
        }
    }}
]

prompt = "帮我寄件给刘新，地址是：北京市朝阳区金地中心66层，电话是18812345678"

messages = [
    {"role": "system", "content": "你是一个联系人录入员。"},
    {"role": "user", "content": prompt}
]

response = get_completions_choices(messages, tools=tools)
print(response)
args = json.loads(response.tool_calls[0].function.arguments)
print("解析结果==>\n", args)
