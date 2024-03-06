from devagi import client  # 引入初始化好的OpenAI客户端

# 创建一个聊天对话，让其生成一段文本
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