"""
数据集导入
"""
import json
from concurrent.futures import ThreadPoolExecutor

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

from langfuse import Langfuse
from dotenv import load_dotenv, find_dotenv
from tqdm import tqdm  # 进度条显示
import AgiUtil

# 调整数据格式 {"input":{...},"expected_output":"label"}
data = []
with open('my_annotations.jsonl', 'r', encoding='utf-8') as fp:
    for line in fp:
        example = json.loads(line.strip())
        item = {
            "input": {
                "outlines": example["outlines"],
                "user_input": example["user_input"]
            },
            "expected_output": example["label"]
        }
        data.append(item)

# 加载 .env 环境变量, 并设置langfuse与openai环境变量
_ = load_dotenv(find_dotenv())

# 初始化 Langfuse
langfuse = Langfuse()

# 创建数据集，如果已存在不会重复创建
langfuse.create_dataset(name="agi-datasets")

# 创建数据集子项，为演示运行速度仅上传前30条数据
for item in tqdm(data[0:10], desc="Importing dataset"):
    langfuse.create_dataset_item(dataset_name="agi-datasets",
                                 input=item["input"],
                                 expected_output=item["expected_output"],
                                 )


# 定义评估函数，用于评估样本数据集和模型输出
def simple_evaluation(output, expected_output):
    return output == expected_output


# 运行数据集
def run_datasets(chain_handler, dataset_name):
    dataset = langfuse.get_dataset(dataset_name)

    def process_item(item):
        handler = item.get_langchain_handler(run_name="agi-run")

        # 执行数据集
        output = chain_handler.invoke(input=item.input, config={"callbacks": [handler]})

        # 评估数据集
        handler.root_span.score(
            name="exact_match",
            value=simple_evaluation(output, item.expected_output)
        )

    # 建议并行处理
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_item, dataset.items)

    # for _item in dataset.items:
    #     process_item(_item)


if __name__ == '__main__':
    # Build chain
    prompt = ChatPromptTemplate.from_template(langfuse.get_prompt("agi_class_bot", type="text").get_langchain_prompt())
    model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, model_kwargs={"seed": 40})
    parser = AgiUtil.AGIOutputParser()
    chain = prompt | model | parser

    # Run datasets
    run_datasets(chain, "agi-datasets")
