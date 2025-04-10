from langchain.schema import HumanMessage
from langchain_community.chat_models import ChatOpenAI

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.7, 
    max_tokens=300 # ограничение токенов
)

# Отправляет промт сети и возвращает ответ
def generate_hint(prompt: str) -> str:
    response = llm.invoke([HumanMessage(content=prompt)])
    return response.content