import numpy as np
from numpy import dot
from numpy.linalg import norm
from devagi import client

"""
- 将文本转成一组浮点数：每个下标 i ，对应一个维度
- 整个数组对应一个 n 维空间的一个点，即文本向量又叫 Embeddings
- 向量之间可以计算距离，距离远近对应语义相似度大小

依赖： pip install numpy 
"""


# 定义cossim余弦距离
def cossim(a, b):
    """余弦距离 -- 越大越相似"""
    return dot(a, b) / (norm(a) * norm(b))


# 定义欧氏距离
def l2(a, b):
    """欧式距离 -- 越小越相似"""
    x = np.asarray(a) - np.asarray(b)
    return norm(x)


def get_embeddings(texts, model="text-embedding-ada-002", dimensions=None):
    """封装 OpenAI 的 Embedding 模型接口"""
    if model == "text-embedding-ada-002":
        dimensions = None
    if dimensions:
        data = client.embeddings.create(input=texts, model=model, dimensions=dimensions).data
    else:
        data = client.embeddings.create(input=texts, model=model).data
    return [x.embedding for x in data]


# query = "国际争端"
# 且能支持跨语言
query = "global conflicts"

documents = [
    "联合国就苏丹达尔富尔地区大规模暴力事件发出警告",
    "土耳其、芬兰、瑞典与北约代表将继续就瑞典“入约”问题进行谈判",
    "日本岐阜市陆上自卫队射击场内发生枪击事件 3人受伤",
    "国家游泳中心（水立方）：恢复游泳、嬉水乐园等水上项目运营",
    "我国首次在空间站开展舱外辐射生物学暴露实验",
]

query_vec = get_embeddings([query])[0]
doc_vecs = get_embeddings(documents)

print("Cosine distance:")
print(cossim(query_vec, query_vec))
for vec in doc_vecs:
    print(cossim(query_vec, vec))

print("\nEuclidean distance:")
print(l2(query_vec, query_vec))
for vec in doc_vecs:
    print(l2(query_vec, vec))

