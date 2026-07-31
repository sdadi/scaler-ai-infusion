import os
import sys
from pyclbr import Class 
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from Class1.scraper import fetch_website_contents

load_dotenv()          # <-- this reads your .env file

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # <-- this adds the parent directory to the path  


prompt = ChatPromptTemplate.from_template(
    "Give a short, friendly summary of this website: \n\n{website}"
)
model = ChatOpenAI(
    model="llama-3.3-70b-versatile",  # a free LLM on Groq
    temperature=0.3,
    api_key=os.getenv("GROQ_API_KEY"), 
    base_url="https://api.groq.com/openai/v1",
)
parser = StrOutputParser()
chain = prompt | model | parser

def summarize(url):
    return chain.invoke({"website": fetch_website_contents(url)})

print(summarize("https://anthropic.com"))