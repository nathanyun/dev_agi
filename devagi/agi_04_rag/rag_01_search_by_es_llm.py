from devagi import get_completion
from devagi.agi_04_rag import search, build_prompt

prompt_template = """
你是一个问答机器人。
你的任务是根据下述给定的已知信息回答用户问题。
确保你的回复完全依据下述已知信息。不要编造答案。
如果下述已知信息不足以回答用户的问题，请直接回复"我无法回答您的问题"。

已知信息:
__INFO__

用户问：
__QUERY__

请用中文回答用户问题。
"""
user_query = "how many parameters does llama 2 have?"
# user_query = "llama 2 有聊天模型吗?"

# 1. 从ES检索知识库
search_results = search(user_query, 2)
print("===检索ES==>")

# 2. 构建 Prompt
prompt = build_prompt(prompt_template, info=search_results, query=user_query)
print("===Built Prompt===\r\n", prompt)

# 3. 调用 LLM
response = get_completion(prompt, temperature=0.2)
print("===回复===\r\n", response)
