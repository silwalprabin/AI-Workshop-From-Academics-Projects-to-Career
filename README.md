# Building Portfolio-Ready AI Agents with Open-Source LLMs

A one-day, hands-on workshop where CS/IT students build **two portfolio projects** using **100% open-source, local LLMs** — no paid API keys, no cloud bills. Everything runs on your own machine with [Ollama](https://ollama.com/).

By the end of the day you'll have two working, demo-able, GitHub-ready projects:

1. **AI Resume Assistant** — a RAG app (ChromaDB + Streamlit) that compares a resume against a job description and suggests tailored improvements.
2. **GitHub Code Review Agent** — a multi-agent system (LangGraph) that reviews code and produces structured findings.

---

## Everything runs locally, for free

- **No paid API keys.** All inference runs on open-source models via Ollama on your laptop.
- **Private.** Your resume and code never leave your machine.
- **Offline-capable.** Once models are pulled, you can build without internet.

**Stack:** Python 3.12 · Ollama · LangGraph · ChromaDB/FAISS · Streamlit · FastAPI · Docker · Git/GitHub

---

## Prerequisites

- Check Workshop_Prerequisites.pdf
---

## Folder structure

```
workshop/
├── README.md                          # You are here
├── datasets/
│   └── Graduate-Resume-Example-Information-Technology.pdf
│   └── sample_repo/                   # Sample code for the review agent
├── docs/
│   ├── TROUBLESHOOTING.md             # Top 30 errors, with fixes
│   ├── INSTALLATION_GUIDE.md          # Per-OS install guide + hardware table
└── projects/
    ├── resume_assistant/              # Project 1 — RAG (ChromaDB + Streamlit)
    │   ├── README.md
    │   ├── src/
    │   ├── data/
    │   ├── tests/
    │   ├── Dockerfile
    │   └── docker-compose.yml
    └── code_review_agent/             # Project 2 — Multi-agent (LangGraph)
        ├── README.md
        ├── main.py
        ├── src/
        ├── tests/
        ├── Dockerfile
        └── docker-compose.yml
```

---

## Project READMEs

- **Project 1 — AI Resume Assistant:** [`projects/resume_assistant/README.md`](projects/resume_assistant/README.md)
- **Project 2 — GitHub Code Review Agent:** [`projects/code_review_agent/README.md`](projects/code_review_agent/README.md)


Happy building — everything here is yours to keep.

Thank you.

## Your Instructor

**Er. Prabin Silwal**

- LinkedIn: <https://www.linkedin.com/in/prabin-silwal/>
- Instagram: <http://instagram.com/silwalprabin2023>
- Facebook: <https://www.facebook.com/Er.PrabinSilwal/>
- Website: <https://www.prabinsilwal.com.np/>
