import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1",
)

PRICES = json.loads('{"shoes":799, "hat":499,"bag":599, "shirt":999, "pants":1299}')

def get_price(item):
    print(f"🔧 tool called: get_price({item})")
    return f"${PRICES.get(item.lower(), 'unknown')}"

tools = [{
    "type": "function",
    "function":{
        "name": "get_price",
        "description": "Get the price of a shop item the user asks about.",
        "parameters": {
            "type": "object",
            "properties": {
                "item": {
                    "type": "string",
                    "description": "The name of the item to get the price for."
                }
            },
            "required": ["item"]
    }
    }
}]

def agent(user_message):
    messages = [{"role": "user", "content": user_message}]

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        tools=tools
    )
    msg = response.choices[0].message

    if msg.tool_calls:
        messages.append(msg)
        for call in msg.tool_calls:
            args = json.loads(call.function.arguments)
            tool_response = get_price(args["item"])
            messages.append({
                "role": "tool",
                "tool_call_id": call.id,
                "content": tool_response
            })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    msg = response.choices[0].message
    return msg.content

if __name__ == "__main__":
    print(agent("How much are the shoes?"))            
    print(agent("Hi! What can you help with?"))