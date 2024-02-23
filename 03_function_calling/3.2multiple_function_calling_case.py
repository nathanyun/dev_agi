from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
import os
import json
import requests

_ = load_dotenv(find_dotenv())

client = OpenAI()


# 多function calling的例子， 调用高德地图获取酒店等信息。
def get_completion(messages):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.6,
        seed=1024,  # 随机种子保持不变，temperature 和 prompt 不变的情况下，输出就会不变
        tool_choice="auto",  # 默认值，由 GPT 自主决定返回 function call 还是返回文字回复。也可以强制要求必须调用指定的函数
        tools=[{
            "type": "function",
            "function": {
                # 定义函数名称
                "name": "search_pois",
                "description": "搜索坐标附近的POI",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "longitude": {
                            "type": "string",
                            "description": "经度"
                        },
                        "latitude": {
                            "type": "string",
                            "description": "维度"
                        },
                        "keyword": {
                            "type": "string",
                            "description": "目标POI的关键字"
                        }
                    }
                }
                # ,"required": ["longitude", "latitude", "keyword"]  这个写不写貌似都可
            }}, {
            "type": "function",
            "function": {
                # 定义函数名称
                "name": "get_location",
                "description": "根据POI名称，获取POI的经纬度坐标",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "POI的名称，必须是中文"
                        },
                        "city": {
                            "type": "string",
                            "description": "POI所在城市，必须是中文"
                        }
                    },
                    "required": ["location", "city"]
                }
            }}
        ]
    )
    if response and response.choices and response.choices[0].message:
        return response.choices[0].message
    return None


# 高德地图APP KEY
# amap_key = "88065c081c9a981e2bb5cd11f3d047e4"
amap_key = os.environ.get("AMAP_KEY")


# 调用高德地图的API接口，获取地址的经纬度坐标
def get_location(location, city):
    url = f"https://restapi.amap.com/v5/place/text?key={amap_key}&keywords={location}&region={city}"
    print(url)
    try:
        r = requests.get(url, timeout=5)  # 设置超时时间为5秒
        r.raise_for_status()  # 检查是否有错误的响应码
        result = r.json()
        if result is not None and 'pois' in result:
            return result['pois'][0]  # 返回第一个结果
        else:
            print(f"UnknownResponse: {result}")
    except requests.exceptions.RequestException as e:
        print(f"Error by get_location: {e}")
    return None


# 调用高德地图的API接口，搜索坐标附近的POI
def search_pois(longitude, latitude, keyword):
    url = f"https://restapi.amap.com/v5/place/around?key={amap_key}&keywords={keyword}&location={longitude},{latitude}"
    print(url)
    try:
        result = requests.get(url, timeout=5)
        print(result)
        return result
    except requests.exceptions.RequestException as e:
        print(f"Error by search_pois: {e}")
    return None


def handel_func_calling(tool_call):
    result = None
    # 获取参数
    args_json = json.loads(tool_call.function.arguments)
    # calling 函数名称
    func_name = tool_call.function.name
    if func_name == 'get_location':
        result = get_location(**args_json)  # 调用函数，并传入参数
    elif func_name == 'search_pois':
        result = search_pois(**args_json)  # 调用函数，并传入参数
    return result


# 定义一个prompt
prompt = "推荐几个北京大望路附近评分4.8分以上的的咖啡店，请列出名称和地址"
print('Prompt==>', prompt)

messages = [
    {"role": "system", "content": '你是一个地理专家，所有地址你都知道'},
    {"role": "user", "content": prompt}
]

response = get_completion(messages)
print('GPT回复==>', response)

# 把大模型生成的答案追加到prompt中
messages.append(response)
max_iter = 3
while response.tool_calls is not None and max_iter > 0:
    max_iter -= 1  # 防止死循环，设置一个最大调用次数
    for tool_call in response.tool_calls:
        result = handel_func_calling(tool_call)
        # 追加到prompt中，这样GPT就能知道这个结果了
        messages.append({
            "tool_call_id": tool_call.id,
            "role": "tool",
            "name": tool_call.function.name,
            "content": str(result)  # 必须转成字符串
        })
        response = get_completion(messages)
        messages.append(response)  # 把大模型的回复追加到prompt中
    # for循环结束，说明没有tool_calls了，说明已经调用完所有的函数了

print('最终GPT回复==>\n', response.content)
