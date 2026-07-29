import gradio as gr
from summarizer import summarize

gr.Interface(
    fn=summarize,
    inputs=gr.Textbox(lines=10, placeholder="Enter text to summarize..."),
    outputs=gr.Textbox(lines=10, placeholder="Summary will appear here..."),
    title="AI Website Summarizer",
).launch(share=True)