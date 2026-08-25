# AI Engineering · Class Project — Build Your Own AI Sidekick

This is the hands-on capstone for learners who have finished **Class 1**
(APIs, Groq, scraping, summarizing, Gradio) and **Class 2** (LangChain,
memory, tool-using agents). It uses **only** those concepts — nothing new,
nothing paid.

## What's in this folder

| Path | Who it's for | What it is |
|------|--------------|-----------|
| `PROBLEM_STATEMENT.md` | **Learners** | The mission, rules, rubric, and idea menu. Hand this out. |
| `INSTRUCTOR_GUIDE.md`  | **You** | How to pitch it, run the session, help with setup, and grade. |
| `requirements.txt`     | Both | The exact (free) libraries needed. |
| `.env.example`         | Both | Template for the one secret they need (a free Groq key). |
| `starter/`             | **Learners** | Skeleton files with `TODO`s. This is what you share. |
| `solution/`            | **You only** | A complete, working reference build. Do **not** share. |

## The 30-second summary

> Build a chat app, powered by a **free** Groq model, that (1) **reads the live
> web** on demand, (2) **remembers** — both within the chat *and across restarts*
> (it saves findings to a file), and (3) **chooses between a menu of tools** to
> complete multi-step jobs (read → save → recall → report). Then point it at a
> real problem *you* care about. Built in 6 timed milestones over ~2 hours.

Everything is free: Groq gives a generous free API tier, Gradio runs locally
and hands you a public share link, and scraping is just `requests`.
