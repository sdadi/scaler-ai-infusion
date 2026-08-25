# agent.py — brain + loop.
# This is Class 2's agent.py, upgraded:
#   • runs on FREE Groq (class-1/groq_call.py trick),
#   • takes `history` so it REMEMBERS the chat (class-2/memory_chat.py),
#   • drives a whole TOOL MENU (read the web / save / recall).
# Fill in every TODO. TODO numbers match the milestones in the problem statement.

import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from tools import TOOLS_SCHEMA, TOOL_FUNCTIONS

load_dotenv()

# ── TODO 0 (Milestone 0): point the SAME OpenAI client at Groq ──────────────
# See class-1/groq_call.py — set api_key from GROQ_API_KEY and the Groq base_url.
client = OpenAI(
    # api_key=...,
    # base_url=...,
)
MODEL = "llama-3.3-70b-versatile"   # free Groq model that supports tools

# ── TODO (Milestone 6): write a system prompt for YOUR flavor ───────────────
# Tell it its job AND how to use the tools: read pages, save important findings,
# recall them when asked, and never make things up.
SYSTEM_PROMPT = "You are a helpful research assistant."

MAX_TOOL_HOPS = 8   # safety cap so the loop can't run forever


def run_agent(user_message, history=None):
    """One turn: think -> maybe use tools -> answer. `history` = chat memory."""

    # ── TODO 2 (Milestone 2): build the messages list ──
    # system prompt, then `history` (past turns, if any), then the new message.
    # Gradio gives history as [{"role","content"}, ...] — same format the API wants.
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    # if history: messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    # ── TODO 1 & 5 (Milestones 1 and 5): the tool loop ──
    # Compare with class-2/agent.py, but wrap it in a loop so the agent can use
    # SEVERAL tools in a row (that's what makes multi-step jobs work):
    #   for _ in range(MAX_TOOL_HOPS):
    #       call the model with messages + TOOLS_SCHEMA
    #       if no tool_calls -> return msg.content        (final answer)
    #       else: append msg, run each requested tool from TOOL_FUNCTIONS,
    #             append each result as {"role":"tool","tool_call_id":..,"content":..}
    #       loop again
    response = client.chat.completions.create(
        model=MODEL, messages=messages, tools=TOOLS_SCHEMA)
    msg = response.choices[0].message

    # ... your loop here ...

    return msg.content


if __name__ == "__main__":
    print(run_agent("Read https://anthropic.com and save one key finding about them."))
    print("---")
    print(run_agent("What have you saved so far?"))
