from dotenv import load_dotenv, find_dotenv
from langfuse import Langfuse
from langchain_core.prompts import ChatPromptTemplate

# 加载 .env 环境变量, 并设置langfuse与openai环境变量
_ = load_dotenv(find_dotenv())

# 初始化Langfuse 客户端 (prompt management)
langfuse = Langfuse()

# Optional, verify that Langfuse is configured correctly
assert langfuse.auth_check()

# 生产环境不建议将prompt写程序里，耦合性太高，使用langfuse UI配置更灵活
__local_prompt = '''
*********
你是AIGC课程的助教，你的工作是从学员的课堂交流中选择出需要老师回答的问题，加以整理以交给老师回答。

你的选择需要遵循以下原则：
1 需要老师回答的问题是指与课程内容或AI/LLM相关的技术问题；
2 评论性的观点、闲聊、表达模糊不清的句子，不需要老师回答；
3 学生输入不构成疑问句的，不需要老师回答；
4 学生问题中如果用“这”、“那”等代词指代，不算表达模糊不清，请根据问题内容判断是否需要老师回答。
 
课程内容:
{{outlines}}
*********
学员输入:
{{user_input}}
*********
Analyse the student's input according to the lecture's contents and your criteria.
Output your analysis process step by step.
Finally, output a single letter Y or N in a separate line.
Y means that the input needs to be answered by the teacher.
N means that the input does not needs to be answered by the teacher.
'''

# 创建一个prompt
langfuse.create_prompt(
    name="agi_class_bot",
    prompt=str(__local_prompt),
    config={
        "model": "gpt-3.5-turbo-1106",
        "temperature": 0,
    },
    is_active=True
)

# 获取prompt
langfuse_prompt_client = langfuse.get_prompt(name='agi_class_bot')
print(f"Prompt: {langfuse_prompt_client.prompt}")
