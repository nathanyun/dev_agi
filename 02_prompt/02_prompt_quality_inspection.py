import os

from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

#  初始化OpenAI客户端
client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)

#  OpenAI chat completions
def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.0):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content

"""
思维链，是大模型涌现出来的一种神奇能力

有人在提问时以「Let’s think step by step」开头，结果发现 AI 会把问题分解成多个步骤，然后逐步解决，使得输出的结果更加准确。

其原理是让 AI 生成更多相关的内容，构成更丰富的「上文」，从而提升「下文」正确的概率
对涉及计算和逻辑推理等复杂问题，尤为有效
"""

"""
下面以客服质检案例验证思维链的效果
客服质检的任务是，验证客服在服务客户过程中的对话中是否符合规范。
"""

# 任务
instruction = """
# 给定一段客服与用户的对话，你的任务是判断客服介绍产品信息的准确性：
> 当向用户介绍流量套餐产品时，客服人员必须准确提及产品名称、月费价格和月流量总量 上述信息缺失一项或多项，或信息与实时不符，都算信息不准确

# 已知产品包括：
* 经济套餐：月费50元，月流量10G
* 畅游套餐：月费180元，月流量100G
* 无限套餐：月费300元，月流量1000G
* 校园套餐：月费150元，月流量200G，限在校学生办理
"""

# 输出描述
output_format = """
以JSON格式输出：
如果信息准确，输出：{"accurate" : true}
如果信息不准确，输出：{"accurate" : false}
"""

context = """
用户：流量大的套餐有什么
客服：我们推荐畅游套餐，180元每月，100G流量，大多数人都够用的
用户：学生有什么优惠吗
客服：如果是在校生的话，可以办校园套餐，150元每月，含200G流量，比非学生的畅游套餐便宜流量还多
"""

context2 = """
用户：流量大的套餐有什么
客服：我们推荐经济套餐，18000元每月，1G流量，大多数人都够用的
用户：学生有什么优惠吗
客服：如果是在校生的话，比非学生的畅游套餐便宜流量还多
"""

prompt = f"""
{instruction}
{output_format}
请一步一步分析以下对话：
对话记录：{context}
"""

# prompt例子如果去掉「一步一步」，context 的分析就会出错。

completion = get_completion(prompt)
print(completion)

"""
正常输出如下：
根据对话记录，我们可以逐步分析客服介绍产品信息的准确性。

首先，用户询问流量大的套餐有哪些，客服回答推荐畅游套餐，每月180元，100G流量。根据已知产品信息，畅游套餐的月费和月流量是准确的。

接下来，用户询问学生是否有优惠，客服回答如果是在校生可以办校园套餐，每月150元，含200G流量，比非学生的畅游套餐便宜流量还多。根据已知产品信息，校园套餐的月费和月流量也是准确的。

综上所述，客服介绍的产品信息是准确的。因此，输出结果为：{"accurate" : true}



注意：大模型存在幻觉，同样的prompt执行结果可能不一致。
"""
