import uuid

from langchain_core.prompts import ChatPromptTemplate

from langchain_openai import ChatOpenAI
from langfuse import Langfuse
from langfuse.callback import CallbackHandler
from dotenv import load_dotenv, find_dotenv
import AgiUtil
import gradio as gr

"""
使用Langfuse和Langchain的读取prompt演示tracing实际示例

AGI 课堂跟课助手，根据课程内容，判断学生问题是否需要老师解答
- 判断该问题是否需要老师解答，回复'Y'或'N'
- 判断该问题是否已有同学问过

"""
# 加载 .env 环境变量, 并设置langfuse与openai环境变量
_ = load_dotenv(find_dotenv())

# 初始化Langfuse 客户端 (prompt management)
langfuse = Langfuse()

# 获取 langfuse prompt
base_prompt = langfuse.get_prompt("agi_class_bot")

# 创建OpenAI客户端（langchain）， 获取 langfuse prompt配置
model = ChatOpenAI(model=base_prompt.config["model"],
                   temperature=str(base_prompt.config["temperature"]))

# 创建outputParser
# parser = StrOutputParser() （from langchain_core.output_parsers import StrOutputParser）
parser = AgiUtil.AGIOutputParser()

# 获取 langchain prompt 格式, 因为langfuse的参数格式是双花括号 {{}} 而langchain是单花括号
neet_answer_prompt = ChatPromptTemplate.from_template(base_prompt.get_langchain_prompt())
# 创建chain
answer_chain = neet_answer_prompt | model | parser  # Build chain with LCEL

# 验重 prompt
check_prompt = ChatPromptTemplate.from_template(
    langfuse.get_prompt("check_duplicated_prompt").get_langchain_prompt())
# 创建chain
check_chain = check_prompt | model | parser


def create_trace(user_id):
    # 创建一个不重复的 id
    trace_id = str(uuid.uuid4())
    trace = langfuse.trace(
        name="my_trace_name",
        id=trace_id,
        user_id=user_id,
        metadata={'user_id': user_id, 'test': '哈哈哈'}
    )
    return trace


# 主流程： 先验证问题是否要回答， 若需要回答再次验证问题是否重复，验证通过后还会将此问题添加进去， 最终返回结果
def verify_question(
        question: str,
        user_id: str,
        outlines: str,
        question_list: list,
) -> bool:
    print(f"\nUser: {question}\n"
          f"User ID: {user_id}\n"
          f"Outlines: {outlines}\n"
          f"Question List: {question_list}")

    # 使用下面2行代码，可实现2个chain用同一个trace管理
    trace = create_trace(user_id)
    handler = trace.get_langchain_handler()
    # tracing_callback = CallbackHandler(user_id=user_id, version="0.1", release="release:v0.1")
    # 判断是否需要回答
    if answer_chain.invoke(
            {"user_input": question, "outlines": outlines},
            config={"callbacks": [handler]}
    ) == 'Y':
        # 判断是否为重复问题
        if check_chain.invoke(
                {"user_input": question,
                 "question_list": "\n".join(question_list)},
                config={"callbacks": [handler]}
        ) == 'N':
            question_list.append(question)
            return True
    return False


if __name__ == "__main__":
    # 模拟用户输入示例
    __outlines = """
   LangChain
   模型 I/O 封装
   模型的封装
   模型的输入输出
   PromptTemplate
   OutputParser
   数据连接封装
   文档加载器：Document Loaders
   文档处理器
   内置RAG：RetrievalQA
   记忆封装：Memory
   链架构：Chain/LCEL"""

    __question_list = ["LangChain支持Java吗", "LangChain和SK哪个好用"],

    # response = verify_question(question="老师langchain中的LCEL的作用是什么",
    #                            outlines=__outlines,
    #                            question_list=["LangChain支持Java吗", "LangChain和SK哪个好用"],
    #                            user_id="123")
    #
    # print(f"\nResponse: {response}")

    gr.Interface(
        title="AGI 课堂跟课助手",
        description="根据课程内容，判断学生问题是否需要老师解答，已经重复的问题不需要解答",
        fn=verify_question,
        inputs=[gr.Textbox(placeholder="请输入你的问题", value="LangChain支持Java吗"),
                gr.Textbox(placeholder="请输入你的ID", value="u123"),
                gr.Textbox(placeholder="课堂内容", value=__outlines),
                gr.CheckboxGroup(label="请选择已存在的问题选项",
                                 choices=["你好", "LangChain和SK哪个好用", "LangChain支持Java吗"]),
                ],
        outputs=["text"],
        stop_btn=gr.Button("Stop", variant="stop", visible=True)
    ).launch(share=True)
