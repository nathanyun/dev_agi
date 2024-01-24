import os
from openai import OpenAI

"""
Tips：执行前，确保.env已经配置， 注意请更换.evn环境变量配置的GPT key

注意，如果无法导入 openai 和 dotenv 包，需要在下载如下依赖：
pip install python-dotenv openai

若无法下载依赖包，请更换pip国内镜像源，换源后再重新下载依赖，例如设置为清华源：
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
"""
# 加载 .env 到环境变量
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

# 配置 OpenAI 服务

client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "今天很早就下班了，我",
        }
    ],
    model="gpt-3.5-turbo",
)

# 打印推理内容
print(response)

"""
响应内容如下：

ChatCompletion(id='chatcmpl-8kQa7yY50Rn0rDjtrKfJ4JZwVsZ04', 

choices=[Choice(finish_reason='stop', index=0, logprobs=None, 
        message=ChatCompletionMessage(content='感到很开心。有时候工作压力很大，能提前下班放松一下是一件很让人愉快的事情。我可以利用这个时间做一些自己喜欢的事情，比如和朋友出去吃饭或看电影，或者在家里放松地看书或看电视。提前下班也可以让我有更多的时间与家人相处，享受一起的晚餐或聊天时光。总之，能够早点下班给我带来了更多的自由和快乐。', 
        role='assistant', 
        function_call=None, 
        tool_calls=None))], 
        created=1706075959, model='gpt-3.5-turbo-0613', 
        object='chat.completion', 
        system_fingerprint=None, 
        usage=CompletionUsage(completion_tokens=172, prompt_tokens=20, total_tokens=192))

"""