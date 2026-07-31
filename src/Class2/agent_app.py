import gradio as gr
import json
from Class2.agent import agent

def chat(message, history):
    return agent(message)

gr.ChatInterface(
    fn=chat,
    title="🛍️ Smart Shop Assistant",
    description="Ask me the price of shoes, hat, bat, short or pants - I will tell you the price.",
).launch(share=True)