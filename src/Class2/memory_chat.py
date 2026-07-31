import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()          # <-- this reads your .env file
model = ChatOpenAI(
    model="llama-3.3-70b-versatile",  # a free LLM on Groq
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a friendly tutor."),
    MessagesPlaceholder("history"),
    ("human", "{question}")
])

chain = prompt | model

history = []
print("Chat with bot (type 'quit' to exit).")
while True:
    question = input("You: ")
    if question.strip().lower() in {"quit", "exit"}:
        break
    answer = chain.invoke({"question": question, "history": history}).content
    print(f"Bot: {answer}")
    history.append(HumanMessage(content=question))
    history.append(AIMessage(content=answer))
    print(f"    (history now has {len(history)} messages)")