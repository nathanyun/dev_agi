from langchain_core.output_parsers import BaseOutputParser
import re


class AGIOutputParser(BaseOutputParser):
    """自定义parser，从思维链中取出最后的Y/N"""

    def parse(self, text: str) -> str:
        matches = re.findall(r'[YN]', text)
        return matches[-1] if matches else 'N'
