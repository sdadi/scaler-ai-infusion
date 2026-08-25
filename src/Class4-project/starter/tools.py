# tools.py — the agent's "hands": a MENU of tools.
# A tool is a normal Python function + a description so the model knows it
# exists (like get_price in class-2/agent.py). You'll build THREE:
#   • read_webpage   — READ the live web   (given to you)
#   • save_finding   — WRITE to notes.json (you build it — Milestone 3)
#   • list_findings  — READ notes.json back (you build it — Milestone 3 & 4)
#
# save + list are what give the agent memory ACROSS restarts, using nothing but
# Python's own json + files. No database. Follow the numbered TODOs.

import os
import json
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

MAX_CHARS = 6000
NOTES_FILE = "notes.json"


# ── Tool 1: read a web page (GIVEN — your Class 1 scraper) ───────────────────
def read_webpage(url):
    """Fetch a URL and return its readable text."""
    print(f"🔧 tool called: read_webpage({url})")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return f"Could not fetch the website. Error: {e}"

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "No title found"

    for tag in soup(["script", "style", "nav", "footer", "header", "img", "input"]):
        tag.decompose()

    text = soup.get_text(separator="\n", strip=True)
    return f"Title: {title}\n\nPage contents:\n{text[:MAX_CHARS]}"


# ── helpers for the notes file (GIVEN — plain Python) ───────────────────────
def _load_notes():
    if not os.path.exists(NOTES_FILE):
        return []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def _save_notes(notes):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


# ── TODO 3a (Milestone 3): Tool 2 — save a finding to the file ──────────────
def save_finding(topic, finding):
    """Append {topic, finding} to the notes, save the file, return a message."""
    print(f"🔧 tool called: save_finding(topic={topic!r})")
    # notes = _load_notes()
    # ... append {"topic": topic, "finding": finding} ...
    # _save_notes(notes)
    # return f"Saved. You now have N findings."
    return "TODO: implement save_finding"


# ── TODO 3b (Milestone 3 & 4): Tool 3 — list saved findings ─────────────────
def list_findings(topic=None):
    """Return saved findings as text. If `topic` given, only matching ones."""
    print(f"🔧 tool called: list_findings(topic={topic!r})")
    # notes = _load_notes()
    # if topic: keep only notes whose topic contains `topic`
    # if empty: return "No saved findings yet."
    # else: return them as readable lines
    return "TODO: implement list_findings"


# ── TODO 1 (Milestone 1) + TODO 3c (Milestone 3): the tool schema ───────────
# Describe EACH tool so the model knows it exists and WHEN to use it.
# Start with read_webpage (Milestone 1), then add save_finding & list_findings
# (Milestone 3). Copy the shape from class-2/agent.py.
TOOLS_SCHEMA = [
    # {
    #     "type": "function",
    #     "function": {
    #         "name": "read_webpage",
    #         "description": "... say WHEN to use it ...",
    #         "parameters": {
    #             "type": "object",
    #             "properties": {"url": {"type": "string", "description": "..."}},
    #             "required": ["url"],
    #         },
    #     },
    # },
    # ... add save_finding (topic, finding) and list_findings (optional topic) ...
]

# ── TODO 2: registry so the loop can find each function by name ─────────────
TOOL_FUNCTIONS = {
    # "read_webpage": read_webpage,
    # "save_finding": save_finding,
    # "list_findings": list_findings,
}


if __name__ == "__main__":
    print(read_webpage("https://anthropic.com")[:300])
    print(save_finding("demo", "This is a saved finding."))
    print(list_findings())
