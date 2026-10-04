import os

def battle(prompt):
    msgs = [{"role": "user", "content": prompt}]

    # Model A â€” OpenAI's GPT
    a = openai_client.chat.completions.create(model=os.getenv("OPENAI_LLM_MODEL"), messages=msgs)

    # Model B â€” Llama on Groq (same code, different brain!)
    b = groq_client.chat.completions.create(model=os.getenv("GROQ_LLM_MODEL"), messages=msgs)

    return a.choices[0].message.content, b.choices[0].message.content
# â€¦now we wrap this in Gradio with two columns + thumbs up/down ðŸ‘‡