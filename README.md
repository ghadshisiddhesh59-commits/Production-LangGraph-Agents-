# Production LangGraph AI Agent

A production-oriented AI agent built with **LangGraph, LangChain, FastAPI, Streamlit, and persistent conversation memory**.

The project demonstrates how to build an AI agent that can reason through a LangGraph workflow, use external tools, maintain conversation history, expose an API, stream responses, and provide a simple web interface.

---

## Features

- LangGraph-based agent workflow
- Tool calling with LangChain tools
- Mathematical calculator tool
- Current date and time tool
- Persistent conversation memory using SQLite and SQLAlchemy
- FastAPI backend
- Streaming API responses
- Streamlit frontend
- Ollama LLM support
- Google Gemini LLM support
- Environment-based configuration
- Request logging
- Global API exception handling
- Request ID generation
- Automated tests with pytest
- GitHub-ready project structure

---

## Architecture

```text
                         User
                           |
                           v
                  Streamlit Frontend
                           |
                           v
                    FastAPI Backend
                           |
                           v
                    Agent Service
                           |
                           v
                    LangGraph Agent
                           |
                 +---------+---------+
                 |                   |
                 v                   v
              LLM Node           Tool Node
                 |                   |
                 |             +-----+------+
                 |             |            |
                 |             v            v
                 |        Calculator   Current Time
                 |
                 v
             Final Response
                 |
                 v
          Persistent Memory
                 |
                 v
             SQLite DB