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

history = []#[HumanMessage(content="My name is Satish"), AIMessage(content="Hello Satish!")]
answer = chain.invoke({"question": "What is my name?", "history": history})
print(answer.content)

print ('after history')
history = [HumanMessage(content="My name is Satish"), AIMessage(content="Hello Satish!")]
answer = chain.invoke({"question": "What is my name?", "history": history})
print(answer.content)