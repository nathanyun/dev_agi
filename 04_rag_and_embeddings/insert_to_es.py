from elasticsearch7 import Elasticsearch, helpers
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re

import warnings

import split_pdf # 引入自定义Lib


"""
# 安装 ES 客户端
!pip install elasticsearch7
# 安装NLTK（文本处理方法库）
!pip install nltk
"""

warnings.simplefilter("ignore")  # 屏蔽 ES 的ip些Warnings

nltk.download('punkt')  # 英文切词、词根、切句等方法
nltk.download('stopwords')  # 英文停用词库


def to_keywords(input_string):
    """（英文）文本只保留关键字"""
    # 使用正则表达式替换所有非字母数字的字符为空格
    no_symbols = re.sub(r'[^a-zA-Z0-9\s]', ' ', input_string)
    word_tokens = word_tokenize(no_symbols)
    # 加载停用词表
    stop_words = set(stopwords.words('english'))
    ps = PorterStemmer()
    # 去停用词，取词根
    filtered_sentence = [ps.stem(w)
                         for w in word_tokens if not w.lower() in stop_words]
    return ' '.join(filtered_sentence)


# 1. 创建Elasticsearch连接
es = Elasticsearch(
    hosts=['http://localhost:9200'],  # 服务地址与端口
    http_auth=("elastic", "89D24Ypppiib*uEKE+w2"),  # 用户名，密码
)

# 2. 定义索引名称
index_name = "my_demo_index202403021014"

# 3. 创建索引 ignore 400状态码，如果索引已经存在则忽略
es.indices.create(index=index_name, ignore=400)

# 4. 从llama2.pdf提取数据
paragraphs = split_pdf.extract_text_from_pdf("llama2.pdf", min_line_length=10)

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