# Progressive Coding Agent Framework

A simple educational framework demonstrating the evolution from basic LLM calls to a complete coding agent, built for teaching the internals of agentic systems.

## Overview

This project showcases how to build a "Claude-like" coding agent from scratch through 6 progressive phases, each adding core capabilities that transform a chat model into an intelligent coding assistant.

## Prerequisites

- Python 3.11+
- [ollama](https://ollama.ai/) running locally with `devstral-2-small` model
- uv (for dependency management)

## Setup

```bash
# Install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e .

# Ensure ollama is running with devstral-2-small
ollama pull devstral-2-small
ollama serve  # In another terminal
```

