import os
from openai import OpenAI
from dotenv import load_dotenv
from scraper import fetch_website_contents
from scraper import fetch_website_contents

load_dotenv()          # <-- this reads your .env file
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url=os.getenv("GROQ_BASE_URL"),
)
# client = OpenAI()

system_prompt = """You analyze the contents of a website and
give a short, friendly summary. Ignore navigation menus.
Respond in markdown."""

def summarize(url):
    website = fetch_website_contents(url)
    response = client.chat.completions.create(
        model=os.getenv("GROQ_LLM_MODEL"),
        messages=[
            {"role":"system", "content": system_prompt},
            {"role":"user",   "content": f"Summarize this website:\n\n{website}"},
        ],
    )
    return response.choices[0].message.content