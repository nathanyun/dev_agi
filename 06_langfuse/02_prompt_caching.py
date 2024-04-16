"""
使用langfuse来管理prompt的好处
1. 解耦，无需重新部署程序来更新prompt
2. 非技术人员可以在控制台创建和更新prompt
3. 可快速回滚指定版本
"""
from dotenv import load_dotenv, find_dotenv
from langfuse import Langfuse

# 加载 .env 到环境变量
_ = load_dotenv(find_dotenv())

# Initialize Langfuse client
langfuse = Langfuse()

# Get current production version
# 默认缓存时间是60秒， 这里设置为300秒， 如果要禁用缓存，设置为0即可
langfuse_prompt = langfuse.get_prompt("test_v1", cache_ttl_seconds=300)

# 参数赋值
prompt = langfuse_prompt.compile(user_input="Hello, how are you?", outlines="test")
print(prompt)
