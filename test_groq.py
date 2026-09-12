from langchain_groq import ChatGroq
from Backend.config.settings import MODEL_NAME, GROQ_API_KEY


llm = ChatGroq(
    model=MODEL_NAME,
    temperature=0,
    api_key=GROQ_API_KEY,
)

response = llm.invoke("Say hello in one sentence.")

print(response.content)