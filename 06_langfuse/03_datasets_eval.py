"""
数据集评估
"""
import uuid
from concurrent.futures import ThreadPoolExecutor

from dotenv import load_dotenv, find_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from langchain_openai import ChatOpenAI
from langfuse import Langfuse


# 加载 .env 环境变量, 并设置langfuse与openai环境变量
_ = load_dotenv(find_dotenv())

# 初始化 Langfuse
langfuse = Langfuse()


# 定义评估函数，用于评估样本数据集和模型输出
def simple_evaluation(output, expected_output):
    return output == expected_output


# 运行数据集
def run_datasets(chain_handler, dataset_name):
    dataset = langfuse.get_dataset(dataset_name)

    def process_item(item):
        handler = item.get_langchain_handler(run_name="v1.1-"+str(uuid.uuid4())[:8])

        # 执行数据集
        output = chain_handler.invoke(item.input, config={"callbacks": [handler]})

        # 评估数据集
        handler.root_span.score(
            name="exact_match",
            value=simple_evaluation(output, item.expected_output)
        )
        print('.', end='', flush=True)

    # 建议并行处理
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(process_item, dataset.items)


if __name__ == '__main__':
    # Build chain
    prompt = PromptTemplate.from_template(langfuse.get_prompt("agi_simple").get_langchain_prompt())
    model = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0, model_kwargs={"seed": 40})
    parser = StrOutputParser()
    chain = prompt | model | parser

    # Run datasets
    run_datasets(chain, "agi-datasets")
