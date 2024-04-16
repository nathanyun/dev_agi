# Dev AGI

## Overview

基于Python的AI开发实践, 包括：生成式AI、LLM应用开发案例、LLM应用开发工具。

## Guides
- [Quickstart ](01_helloworld)：一个简单的生成式AI
- [Prompt Engineering](02_prompt)
  - [基于GPT的多轮对话客服机器人](02_prompt/01_prompt_customer_service_bot.py)
  - [基于思维链prompt客服质检](02_prompt/02_prompt_quality_inspection.py)
- [Function Calling](03_function_calling)
  - [Local function calling: 数学计算](03_function_calling/01_sum_function_calling.py)
  - [Remote function calling: 高德地图API实现多轮function calling](03_function_calling/02_amap_multiple_function_calling.py)
  - [Fake function calling: 联系人地址提取](03_function_calling/03_addr_summary_function_calling.py)
- [RAG](04_rag)
  - [基于Elasticsearch、NLTK 的RAG问答](04_rag/02_es_llm.py)
  - [OpenAI embedding、chromadb 实现文本相似度检索](04_rag/03_text_embeddings_by_chromadb.py)
  - [RAG 生成式问答Bot](04_rag/rag_bot.py)
- [LangChain](05_langchain)
  - [LangChain 实现 OpenAI 多轮对话](05_langchain/lc_multi_conversition.py)
  - [LangChain 管理 prompt](05_langchain/lc_prompt_template.py)
  - [LangChain 的向量数据库及向量检索](05_langchain/lc_vector_stores_faiss.py)
  - [基于 LangChain 实现向量检索的 RAG 生成式问答](05_langchain/lc_chat_pdf.py)
  - [一个实际应用：ChatPDF](05_langchain/chat_pdf_view.py)

- [Langfuse](06_langfuse)
  - [使用langfuse来监控跟踪LLM应用](06_langfuse/01_tracing_llm_project.py)
  - [使用langfuse来管理prompt模板](06_langfuse/02_prompt_management.py)
  - [Prompt 缓存](06_langfuse/02_prompt_caching.py) 
  - [通过Python代码来创建langfuse的prompt](06_langfuse/02_prompt_create_by_code.py) 
  - [langfuse整合langchain做监控追踪和prompt管理](06_langfuse/02_tracing_and_prompt_with_langchain.py) 


## About me

- Wechat：406811520
- Email：nasheng.yun@gmail.com

## Donate
If you found the code examples helpful, please give me a :star:! Thank you!