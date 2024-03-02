from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

"""
# 安装 pdf 解析库
!pip install pdfminer.six
"""


def extract_text_from_pdf(filename, page_numbers=None, min_line_length=1):
    '''从 PDF 文件中（按指定页码）提取文字'''
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


if __name__ == '__main__':
    # 从llama2.pdf提取数据
    paragraphs = extract_text_from_pdf("llama2.pdf", min_line_length=10)

    for grap in paragraphs[0:3]:
        print(grap + '\n')  # 打印3行
