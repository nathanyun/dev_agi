"""
思维树案例：
小明运动科目成绩如下：
- 100 米跑成绩：10.5 秒
- 1500 米跑成绩：3 分 20 秒
- 铅球成绩：12 米。
问：他适合参加哪些搏击运动训练？
"""

import json
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = OpenAI()


def get_completion(prompt, model="gpt-3.5-turbo", temperature=0.0):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature  # 模型输出的随机性，0 表示随机性最小
    )
    return response.choices[0].message.content


# 必须以GPT-4才支持
def performance_analyser(text):
    prompt = f"{text}\n请根据以上成绩，分析候选人在速度、耐力、力量三方面素质的分档。分档包括：强（3），中（2），弱（1）三档。\
                \n以JSON格式输出，其中key为素质名，value为以数值表示的分档。"
    response = get_completion(prompt, model="gpt-4")
    return json.loads(response)

def possible_sports(talent, category):
    prompt = f"需要{talent}强的{category}运动有哪些。给出10个例子，以array形式输出。确保输出能由json.loads解析。"
    response = get_completion(prompt, temperature=0.8)
    return json.loads(response)


def evaluate(sports, talent, value):
    prompt = f"分析{sports}运动对{talent}方面素质的要求: 强（3），中（2），弱（1）。\
                \n直接输出挡位数字。输出只包含数字。"
    response = get_completion(prompt)
    val = int(response)
    print(f"{sports}: {talent} {val} {value>=val}")
    return value >= val


def report_generator(name, performance, talents, sports):
    level = ['弱', '中', '强']
    _talents = {k: level[v-1] for k, v in talents.items()}
    prompt = f"已知{name}{performance}\n身体素质：{_talents}。\n生成一篇{name}适合{sports}训练的分析报告。"
    response = get_completion(prompt)
    return response

# 测试开始~~~~~~~~~~~~~~~~
name = "小明"
performance = """
运动科目成绩如下：
- 100 米跑成绩：10.5 秒
- 1500 米跑成绩：3 分 20 秒
- 铅球成绩：12 米。
"""

# 分析小明的各项指标
talents = performance_analyser(name+performance)
print("===talents===")
print(talents)

cache = set()
# 深度优先

# 第一层节点
for k, v in talents.items():
    if v < 3:  # 剪枝
        continue
    leafs = possible_sports(k, "搏击")  # 随机给出某些达标的10项运动
    print(f"==={k} leafs===")
    print(leafs)
    # 第二层节点
    for sports in leafs:
        if sports in cache:
            continue
        cache.add(sports)
        suitable = True
        for t, p in talents.items():
            if t == k:
                continue
            # 第三层节点
            if not evaluate(sports, t, p):  # 剪枝
                suitable = False
                break
        if suitable:
            report = report_generator(name, performance, talents, sports)
            print("****")
            print(report)
            print("****")

"""
运行结果：
===talents===
{'速度': 3, '耐力': 3, '力量': 2}
===速度 leafs===
['拳击', '跆拳道', '泰拳', '综合格斗', '散打', '巴西柔术', '空手道', '九节鞭', '硬气功', '跆拳道散打']
拳击: 耐力 3 True
拳击: 力量 3 False
跆拳道: 耐力 3 True
跆拳道: 力量 3 False
泰拳: 耐力 3 True
泰拳: 力量 3 False
综合格斗: 耐力 3 True
综合格斗: 力量 3 False
散打: 耐力 3 True
散打: 力量 3 False
巴西柔术: 耐力 3 True
巴西柔术: 力量 3 False
空手道: 耐力 3 True
空手道: 力量 3 False
九节鞭: 耐力 3 True
九节鞭: 力量 3 False
硬气功: 耐力 3 True
硬气功: 力量 3 False
跆拳道散打: 耐力 3 True
跆拳道散打: 力量 3 False
===耐力 leafs===
['拳击', '泰拳', '综合格斗', '跆拳道', '空手道', '散打', '巴西柔术', '自由搏击', '踢拳', '绳击']
自由搏击: 速度 3 True
自由搏击: 力量 3 False
踢拳: 速度 3 True
踢拳: 力量 3 False
绳击: 速度 3 True
绳击: 力量 3 False

"""