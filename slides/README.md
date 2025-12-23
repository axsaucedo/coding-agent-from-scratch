# Progressive Coding Agent Framework - Interactive Presentation

An interactive marimo-based presentation showing how to build a coding agent from scratch, progressing through 6 phases from basic LLM communication to a full development agent with code generation and testing.

## Overview

This presentation demonstrates the evolution of an agentic system through progressive phases:

| Phase | Capability | Tools | Key Pattern |
|-------|-----------|-------|-------------|
| 1️⃣ | Basic Chat | 0 | Streaming LLM communication |
| 2️⃣ | Tool Usage | 2 | Agentic loop with tool calling |
| 3️⃣ | Context Aware | 4 | Project understanding |
| 4️⃣ | Planning | 4 | Structured reasoning |
| 5️⃣ | Code Generation | 6 | Code creation |
| 6️⃣ | Testing | 8 | Full development cycle |

## Prerequisites

### Required
- **Python 3.8+**
- **marimo** - Interactive Python presentation framework
- **Local LLM** - Ollama with devstral-small-2 model running

### Installation

1. Install marimo:
```bash
pip install marimo
```

2. Install Ollama and run the LLM:
```bash
# Download and install Ollama from https://ollama.ai
# Then run:
ollama pull devstral-small-2
ollama serve
```

Keep the Ollama server running in a separate terminal while viewing the presentation.

### Optional Dependencies

The presentation code already imports all required modules:
- `httpx` - HTTP streaming
- `json` - JSON parsing
- `subprocess` - Code execution
- `os`, `glob` - File operations
- `re`, `ast` - Regex and AST parsing

All are standard library or already in your environment.

## Running the Presentation

From the project root directory:

```bash
marimo run slides/main.py
```

Or for interactive editing mode:

```bash
marimo edit slides/main.py
```

The presentation will open in your browser at `http://localhost:3000`.

## Slide Structure

### Introduction (5 slides)
- **Title Slide**: Overview of the 6-phase journey
- **Problem Statement**: What's missing in basic LLMs
- **Journey Map**: The 6 phases at a glance
- **Key Concepts**: Core patterns we'll learn

### Phase 1: Basic LLM Chat 🗣️
- **Foundation**: Streaming communication with Ollama
- **Key Code**: `chat_stream()` function (lines 18-29 of phase_1/main.py)
- **Demo**: Interactive prompt with live LLM streaming output
- **Key Metric**: ~10 lines of code for streaming

### Phase 2: Tool-Enabled Agent 🛠️
- **Capability**: Agent can use tools to perform actions
- **New Tools**: `read_python_file()`, `list_python_files()`
- **Key Pattern**: Tool calling loop (3 iterations max)
- **Demo**: Agent reads/lists files using tool calls

### Phase 3: Context-Aware Agent 🧠
- **Capability**: Agent understands project structure
- **New Tools**: `analyze_project()`, `find_functions()`
- **Key Pattern**: Recursive project analysis
- **Demo**: Agent discovers functions and project structure

### Phase 4: Planning Agent 📋
- **Capability**: Agent breaks down tasks into structured steps
- **Key Pattern**: Prompt engineering for numbered steps
- **Demo**: Agent creates step-by-step plans
- **Reuses**: Previous tools + LLM planning

### Phase 5: Code Generation Agent 💻
- **Capability**: Agent can write working Python code
- **New Tools**: `generate_code()`, `create_python_file()`
- **Key Pattern**: Markdown block parsing and cleaning
- **Demo**: Generate code from descriptions

### Phase 6: Testing & Execution Agent ✅
- **Capability**: Agent runs and validates generated code
- **New Tool**: `run_python_file()`
- **Key Pattern**: Subprocess execution with error detection
- **Demo**: End-to-end: generate → save → test → validate

### Integration & Summary
- Full tool ecosystem overview
- Core patterns recap
- Next steps and extensibility
- Real-world applications

## How It Works

All code in this presentation is **self-contained** and written directly into the marimo notebook. No external files are imported - everything is defined inline with comments referencing the original source files from the phase folders.

### Key Features

1. **Progressive Building**: Each phase adds functionality to previous phases
2. **Live Interaction**: Input fields let you test each agent capability
3. **Full Source References**: Comments show exact source files and line numbers
4. **Streaming Output**: See LLM responses in real-time with token streaming
5. **Tool Discovery**: Docstrings automatically become tool descriptions

### Architecture

The core patterns demonstrated:

```
Phase 1: chat_stream()
         ↓
Phase 2: + agent_with_tools() + tool functions
         ↓
Phase 3: + project analysis tools
         ↓
Phase 4: + planning with prompt engineering
         ↓
Phase 5: + code generation and file creation
         ↓
Phase 6: + code execution and validation
```

## Important Notes

### Ollama Requirement
All interactive demos require Ollama running locally with the `devstral-small-2` model:

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Run marimo
marimo run slides/main.py
```

If Ollama is not available, the presentation still displays all code and explanations - only the interactive demos will fail gracefully.

### Performance
- **First LLM call**: May take 10-30 seconds (model startup)
- **Subsequent calls**: 2-10 seconds depending on prompt length
- **Code generation**: 5-15 seconds (more complex for larger functions)
- **Timeouts**: Set to 10 seconds for code execution

### Customization
You can modify the demo prompts directly in the marimo interface:
- Each phase has an input field
- Change the default values
- Run multiple demos to see different outputs
- The agent loop shows up to 3 iterations per request

## What You'll Learn

1. **🛠️ Tool Pattern**: How to make functions discoverable as tools
2. **🔄 Agent Loop**: Iterative LLM interaction with tool execution
3. **🧠 Context Awareness**: How agents understand projects
4. **📋 Planning**: Structured task decomposition
5. **💻 Code Generation**: Using LLMs to write working code
6. **✅ Testing**: Validating generated code programmatically

## Extending the Framework

The framework is infinitely extensible. To add new tools:

1. Define a function with a docstring:
```python
def new_tool(param: str) -> str:
    """Description of what this tool does."""
    return result
```

2. Add it to the agent's tools list:
```python
tools=[read_python_file, list_python_files, ..., new_tool]
```

New tools automatically become available to the agent!

## Real-World Applications

- **Code Review Agents**: Analyze and improve code
- **Documentation Generators**: Auto-generate API docs
- **Automated Refactoring**: Improve code structure
- **Testing Assistants**: Generate test cases
- **CI/CD Automation**: Integrate into pipelines

## Troubleshooting

### "Cannot connect to Ollama"
- Ensure Ollama is running: `ollama serve`
- Check localhost:11434 is accessible
- Model must be pulled: `ollama pull devstral-small-2`

### Slow responses
- First request takes longer (model loading)
- Check system resources
- LLM response time depends on model size

### Input not updating
- Marimo cells are reactive - click "Run" or modify input
- Some cells may take time to compute
- Check browser console for errors

## File Structure

```
/slides/
├── main.py          # Single file with complete presentation
└── README.md        # This file
```

All code is self-contained in `main.py`. No external dependencies or utils files.

## Architecture Notes

The presentation implements the core agent patterns:

- **Tool Parsing**: Regex pattern `TOOL:name(params)` with DOTALL flag
- **Docstring Tools**: Functions with docstrings automatically become tools
- **Iterative Loop**: Max 3 iterations per request
- **Error Handling**: Graceful fallback if LLM unavailable
- **Parameter Parsing**: Handles JSON and string parameters

## Credits

This presentation demonstrates the progressive development of a coding agent framework, showing how to build sophisticated AI systems from basic LLM communication up to full code generation and testing capabilities.

## Resources

- [Ollama Documentation](https://ollama.ai)
- [Marimo Documentation](https://marimo.io)
- [Python AST Module](https://docs.python.org/3/library/ast.html)
- [Regular Expressions](https://docs.python.org/3/library/re.html)

---

**Created with marimo 📊** - Interactive Python presentation framework
