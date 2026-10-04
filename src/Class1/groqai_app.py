# pip install openai   (yes â€” the same library!)
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

# point the SAME client at Groq instead of OpenAI ðŸ‘‡
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

response = client.chat.completions.create(
    model=os.getenv("GROQ_LLM_MODEL"),
    messages=[
        {"role": "system", "content": "You are a witty travel guide."},
        {"role": "user",   "content": "Suggest one thing to do in Bangalore."},
    ],
)
print(response.choices[0].message.content)