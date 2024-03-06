from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer
from elasticsearch7 import Elasticsearch, helpers
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import nltk
import re
import warnings
import ssl

"""
# 安装 pdf 解析库
!pip install pdfminer.six
"""


def extract_text_from_pdf(filename, page_numbers=None, min_line_length=1):
    """从 PDF 文件中（按指定页码）提取文字"""
    paragraphs = []
    buffer = ''
    full_text = ''
    # 提取全部文本
    for i, page_layout in enumerate(extract_pages(filename)):
        # 如果指定了页码范围，跳过范围外的页
        if page_numbers is not None and i not in page_numbers:
            continue
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                full_text += element.get_text() + '\n'
    # 按空行分隔，将文本重新组织成段落
    lines = full_text.split('\n')
    for text in lines:
        if len(text) >= min_line_length:
            buffer += (' ' + text) if not text.endswith('-') else text.strip('-')
        elif buffer:
            paragraphs.append(buffer)
            buffer = ''
    if buffer:
        paragraphs.append(buffer)
    return paragraphs


# 仅此类自身运行， 被外部引用不会执行这段代码
# if __name__ == '__main__':
#     # 从llama2.pdf提取数据
#     paragraphs = extract_text_from_pdf("llama2.pdf", min_line_length=10)
#
#     for grap in paragraphs[0:3]:
#         print(grap + '\n')  # 打印3行


if __name__ == '__main__':
    """
    # 安装NLTK（文本处理方法库）
    !pip install nltk
    """
    # 创建一个SSL上下文对象并禁用SSL验证, 解决nltk下载失败的问题
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # 将SSL上下文应用到全局
    ssl._create_default_https_context = ssl._create_unverified_context

    # 设置nltk下载器使用修改后的SSL上下文
    # nltk.set_proxy('http://your_proxy')  # 如果有代理的话，可以设置代理
    # nltk.setenv('SSL_CERT_FILE', '/path/to/your/custom/certificate.pem')  # 可选：如果你有自定义的SSL证书

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


# 屏蔽 ES 的 Warnings
warnings.simplefilter("ignore")

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

# 本地运行会删除索引重建
if __name__ == '__main__':

    # 3. 如果索引已存在，删除它（仅供演示，实际应用时不需要这步）
    if es.indices.exists(index=index_name):
        es.indices.delete(index=index_name)

    # 4. 创建索引 ignore 400 状态码，如果索引已经存在则忽略
    es.indices.create(index=index_name, ignore=400)

    # 5. 从llama2.pdf提取数据
    paragraphs = extract_text_from_pdf("llama2.pdf", min_line_length=10)

    # 6. 灌库指令
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


# ES提供的检索方法
def search(query_string, top_n=3):
    # ES 的查询语言
    search_query = {
        "match": {
            "keywords": to_keywords(query_string)
        }
    }
    res = es.search(index=index_name, query=search_query, size=top_n)
    return [hit["_source"]["text"] for hit in res["hits"]["hits"]]


if __name__ == "__main__":
    # 检索ES，统计llama2有哪些参数
    results = search("how many parameters does llama 2 have?", 3)
    print(results)


def build_prompt(prompt_template, **kwargs):
    """将 Prompt 模板赋值"""
    prompt = prompt_template
    for k, v in kwargs.items():
        if isinstance(v, str):
            val = v
        elif isinstance(v, list) and all(isinstance(elem, str) for elem in v):
            val = '\n'.join(v)
        else:
            val = str(v)
        prompt = prompt.replace(f"__{k.upper()}__", val)
    return prompt