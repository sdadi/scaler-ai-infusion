import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv(Path(__file__).with_name(".env"))


@lru_cache(maxsize=10)
def create_model() -> ChatOpenAI:
    """Create the OpenAI-compatible chat client used by the LangChain chains."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Set GROQ_API_KEY in the Class8 .env file before using the LLM.")
    return ChatOpenAI(
        model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
        temperature=0,
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1",
    )