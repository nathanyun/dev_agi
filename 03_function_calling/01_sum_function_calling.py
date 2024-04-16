from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import json

_ = load_dotenv(find_dotenv())

client = OpenAI()

"""
OpenAI详细参数文档：https://platform.openai.com/docs/api-reference/chat/create
"""


def get_completions(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        # 模型可能调用的工具列表。目前，仅支持将函数作为工具。使用它来提供模型可能为其生成 JSON 输入的函数列表。
        tools=[{
            "type": "function",  # 必填，工具的类型。目前仅支持function
            "function": {
                "name": "sum",  # 必填，要调用的函数名。必须是 a-z、A-Z、0-9，或包含下划线和短划线，最大长度为 64。
                "description": "给一组数求和",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "numbers": {
                            "type": "array",
                            "items": {
                                "type": "number"
                            }
                        }
                    }
                }
            }
        }]
    )
    return response.choices[0].message


# 定义一个prompt
# prompt = "请问1+2+3+4+5+...+100，然后再加等于多少？"
prompt = "桌子上有3个苹果，2个香蕉，3本书，问总共有几个水果？"
# prompt = "太阳从哪边升起？"  # 不需要算加法，会怎样？
print('Prompt==>', prompt)

messages = [
    {"role": "system",
     "content": '你是一个数学家还是一个统计学家，只能回答数学和统计学相关的知识，其他领域的问题直接拒绝回答'},
    {"role": "user", "content": prompt}
]

response = get_completions(messages)
print('GPT回复==>', response)
"""
ChatCompletionMessage(content=None, role='assistant', function_call=None, tool_calls=[ChatCompletionMessageToolCall(id='call_ymkrre5QnwC8VusC6uTucn2H', function=Function(arguments='{"numbers":[1,2,3,50]}', name='sum'), type='function')])
"""
# 把大模型生成的答案追加到prompt中
messages.append(response)

# 判断返回的tool_calls是否为空
if response.tool_calls is not None:

    tool_call = response.tool_calls[0]  # 有概率会返回多个，这里只取第一个

    if tool_call.function.name == 'sum':
        # 转换成JSON
        argsJson = json.loads(tool_call.function.arguments)
        print(f"argsJson {argsJson}")

        # 调用函数，并传入参数
        result = sum(argsJson['numbers'])
        print('函数调用结果==>', result)

        # 追加到prompt中，这样GPT就能知道这个结果了
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": "sum",
            "content": str(result)  # 必须转成字符串
        })

        print('再次调用GPT获取自然语言回复==>', get_completions(messages).content)
