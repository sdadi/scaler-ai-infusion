import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

load_dotenv()
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a witty travel guide."},
        {"role": "user", "content": "Suggest one thing to do in Bangalore."}
    ]
)

print(response.choices[0].message.content)