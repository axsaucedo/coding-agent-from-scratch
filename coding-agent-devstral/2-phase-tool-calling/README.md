# Phase 2: Tool Calling

## What it does
Agent with an agentic loop that can use tools (read_file, list_python_files). LLM sees tool descriptions and can request tool usage. Agent detects requests, executes tools, and feeds results back.

## Run it
```bash
python main.py
pytest test.py  # Run tests
```

## Key concepts
- Tool definitions with docstrings
- Agentic loop with tool execution
- LLM prompt includes tool descriptions
- Tool detection and execution cycle