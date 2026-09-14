from langchain_ollama import ChatOllama
from Backend.config.settings import MODEL_NAME


llm = ChatOllama(
    model=MODEL_NAME,
    temperature=0,
)

response = llm.invoke("Say hello in one sentence.")

print(response.content)