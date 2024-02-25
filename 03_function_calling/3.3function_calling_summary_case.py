from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json


# 需求：从一段文字中提取联系人姓名、地址、电话号码

_ = load_dotenv(find_dotenv())
client = OpenAI()

def get_completion(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        response_format={"type": "json_object"},  # 指定返回格式为 json_object
        temperature=0,
        seed=1024,  # 随机种子保持不变，temperature 和 prompt 不变的情况下，输出就会不变
        tool_choice="auto",
        tools=[{
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
    )
    if response and response.choices and response.choices[0].message:
        return response.choices[0].message
    return None

def print_json(data):
    """
    打印参数。如果参数是有结构的（如字典或列表），则以格式化的 JSON 形式打印；
    否则，直接打印该值。
    """
    if hasattr(data, 'model_dump_json'):
        data = json.loads(data.model_dump_json())

    if (isinstance(data, (list, dict))):
        print(json.dumps(
            data,
            indent=4,
            ensure_ascii=False
        ))
    else:
        print(data)

prompt = "帮我寄件给刘新，地址是：北京市朝阳区金地中心66层，电话是18812345678"

messages = [
    {"role": "system", "content": "你是一个联系人录入员。"},
    {"role": "user", "content": prompt}
]

response = get_completion(messages)
print_json(response)
args = json.loads(response.tool_calls[0].function.arguments)
print("解析结果==>")
print_json(args)

