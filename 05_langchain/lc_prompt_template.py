from langchain.prompts import PromptTemplate

prompt_template = PromptTemplate.from_template(
    "Tell me a {adjective} joke about {content}."
)
prompt = prompt_template.format(adjective="funny", content="fox")
print(prompt)