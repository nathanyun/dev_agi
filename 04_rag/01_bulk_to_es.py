from elasticsearch7 import Elasticsearch, helpers
from util import extract_text_from_pdf, to_keywords, search

"""
# 安装 ES 客户端
!pip install elasticsearch7
"""

# 1. 创建Elasticsearch连接
es = Elasticsearch(
    hosts=['http://localhost:9200'],  # 服务地址与端口
    http_auth=("elastic", "89D24Ypppiib*uEKE+w2"),  # 用户名，密码
)

# 2. 定义索引名称
index_name = "my_demo_index202403021314"

# 3. 如果索引已存在，删除它（仅供演示，实际应用时不需要这步）
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)

# 3. 创建索引 ignore 400 状态码，如果索引已经存在则忽略
es.indices.create(index=index_name, ignore=400)

# 4. 从llama2.pdf提取数据
paragraphs = extract_text_from_pdf("llama2.pdf", page_numbers=[2, 3], min_line_length=10)

# 5. 灌库指令
actions = [
    {
        "_index": index_name,
        "_source": {
            "keywords": to_keywords(para),
            "text": para
        }
    }
    for para in paragraphs
]

# 6. 文本灌库
helpers.bulk(es, actions)

# 检索ES，统计llama2有哪些参数
results = search("how many parameters does llama 2 have?", 3)
for r in results:
    print(r + "\n")
