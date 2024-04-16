"""
数据集导入
"""
import json

from dotenv import load_dotenv, find_dotenv
from langfuse import Langfuse
from tqdm import tqdm  # 进度条显示

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
