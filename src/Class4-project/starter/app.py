# app.py — the FACE of your Sidekick: a Gradio chat UI with a public link.
# Almost done for you. TODOs: give it memory, and theme it for your flavor.
# Run:  python app.py    then open the link it prints.

import gradio as gr
from agent import run_agent


def chat(message, history):
    # Gradio fills in `message` (newest) and `history` (all past turns) for you.
    #
    # ── TODO 2 (Milestone 2): pass `history` so it REMEMBERS the conversation!
    #    (Exactly the homework hint from class-2/app.py.)
    return run_agent(message)          # <- change to: run_agent(message, history)


gr.ChatInterface(
    fn=chat,
    type="messages",                   # history arrives as {"role","content"} dicts
    # ── TODO (Milestone 6): theme the title/description/examples for YOUR flavor
    title="🤖 My Research Sidekick",
    description="Share a link and I'll read it, save the key bits, and recall them later.",
    examples=[
        "Read https://en.wikipedia.org/wiki/Large_language_model and save the 3 key ideas",
        "What findings have you saved so far?",
    ],
).launch(share=True)                   # share=True -> also prints a public link
