import marimo

__generated_with = "0.18.4"
app = marimo.App(width="medium")

@app.cell
def __():
    import marimo as mo
    import httpx
    import json
    import subprocess
    import os
    import glob
    import re
    import ast
    return mo, httpx, json, subprocess, os, glob, re, ast

@app.cell
def __(mo):
    mo.md("""
# 🤖 Building a Coding Agent from Scratch

## From Basic LLM to Multi-Tool Agentic System

An interactive journey through 6 progressive phases showing how to build a sophisticated
coding agent, starting from simple LLM communication and building up to a full development agent.
""")

@app.cell
def __(mo):
    mo.md("""
## The Problem

Basic Large Language Models (LLMs) have a critical limitation:
- ✓ They can think and reason
- ✓ They can generate text
- ✗ They **cannot take actions** (read files, execute code, call APIs)

### What We're Building

An agentic system that:
1. **Communicates** with an LLM (streaming)
2. **Uses tools** to perform actions
3. **Understands context** about projects
4. **Plans tasks** with structured reasoning
5. **Generates code** from descriptions
6. **Tests code** and validates results

The framework demonstrates **progressive enhancement** - each phase adds capabilities
without breaking previous functionality.
""")

@app.cell
def __(mo):
    mo.md("""
## The 6-Phase Journey

| Phase | Capability | Tools | Key Pattern |
|-------|-----------|-------|-------------|
| 1️⃣ | Basic Chat | 0 | Streaming LLM communication |
| 2️⃣ | Tool Usage | 2 | Agentic loop with tool calling |
| 3️⃣ | Context Aware | 4 | Project understanding |
| 4️⃣ | Planning | 4 | Structured reasoning |
| 5️⃣ | Code Generation | 6 | Code creation |
| 6️⃣ | Testing | 8 | Full development cycle |

Each phase builds on the previous, progressively adding new capabilities and tools.
""")

@app.cell
def __(mo):
    mo.md("""
## Core Concepts We'll Learn

### 🛠️ Tool Pattern
Functions become automatically discoverable tools through docstrings.

### 🔄 Agent Loop
The iterative process: LLM → Tool Call Parsing → Tool Execution → Result Integration

### 🧠 Context Awareness
Agents can understand and analyze the projects they're working on.

### 📋 Planning
Structured task decomposition using LLM-guided planning.

### 💻 Code Generation
Using LLMs to write working Python code from descriptions.

### ✅ Testing & Validation
Executing generated code and validating results.
""")

# ============================================================================
# PHASE 1: BASIC LLM CHAT
# ============================================================================

@app.cell
def __(mo):
    mo.md("""
## Phase 1: Basic LLM Chat 🗣️

**Foundation**: Direct streaming communication with local LLM

**Why**: Every agent needs to talk to an LLM. This phase establishes the foundation.

**Key Metric**: ~10 lines of code for streaming communication

**Concepts**:
- HTTP streaming to local LLM (Ollama)
- Token-by-token output
- Real-time response handling
""")

@app.cell
def __(mo, httpx, json):
    def chat_stream(prompt: str, system_prompt: str = "") -> str:
        """Stream-based chat interface with local LLM.

        Communicates with Ollama API using HTTP streaming for real-time token output.
        """
        response = ""
        full_prompt = f"System prompt: {system_prompt}\nUser: {prompt}"
        try:
            with httpx.stream("POST", "http://localhost:11434/api/generate",
                             json={'model': 'devstral-small-2', 'prompt': full_prompt, 'stream': True},
                             timeout=None) as r:
                for line in r.iter_lines():
                    if line and (token := json.loads(line).get('response', '')):
                        response += token
        except Exception as e:
            response = f"Error: {e}"
        return response

    mo.md("""
### Phase 1 Code: `chat_stream()`

```python
def chat_stream(prompt: str, system_prompt: str = "") -> str:
    response = ""
    full_prompt = f"System prompt: {system_prompt}\\nUser: {prompt}"

    with httpx.stream("POST", "http://localhost:11434/api/generate",
                     json={'model': 'devstral-small-2', 'prompt': full_prompt, 'stream': True},
                     timeout=None) as r:
        for line in r.iter_lines():
            if line and (token := json.loads(line).get('response', '')):
                response += token
    return response
```

### Key Points
- `httpx.stream()` for streaming responses
- Token-by-token extraction from JSONL responses
- Real-time response handling
- `timeout=None` to wait indefinitely for LLM
""")
    return chat_stream

@app.cell
def __(mo):
    mo.md("""
### Phase 1 Demo

The simplest agent: just chat with an LLM.

**Features**:
- Direct streaming to local LLM (Ollama)
- Token-by-token output for responsiveness
- Foundation for all future phases

**Use Case**: Ask questions, get streamed responses

**Requires**: Ollama running locally (`ollama serve`)
""")

# ============================================================================
# PHASE 2: TOOL-ENABLED AGENT
# ============================================================================

@app.cell
def __(mo):
    mo.md("""
## Phase 2: Tool-Enabled Agent 🛠️

**New Capability**: Agent can now USE TOOLS to perform actions

**Why**: LLMs can't actually read files or access systems. Tools enable real actions.

**Key Metrics**:
- 2 tools (read_python_file, list_python_files)
- 3-iteration max for agent loop
- Regex parsing with TOOL:name(params) format

**Concepts**:
- Tool discovery via docstrings
- Agentic loop: LLM → Parse → Execute → Feedback
- Error handling for malformed inputs
""")

@app.cell
def __(mo, glob, os, re, json, httpx):
    def read_python_file(filepath: str) -> str:
        """Read and return the contents of a Python file."""
        try:
            with open(filepath, 'r') as f:
                return f.read()
        except FileNotFoundError:
            return f"File not found: {filepath}"

    def list_python_files(directory: str = ".") -> str:
        """List all Python files in a directory."""
        files = glob.glob(os.path.join(directory, "**", "*.py"), recursive=True)
        return "\n".join(sorted(files)) if files else "No Python files found"

    def agent_with_tools(prompt: str) -> str:
        """Agent loop with tool calling capability."""
        TOOLS = [read_python_file, list_python_files]
        tool_descriptions = "\n".join([f"- {t.__name__}: {t.__doc__}" for t in TOOLS])

        agent_system = f"""You are an agent with access to these tools:
{tool_descriptions}

When you need to use a tool, format: TOOL:tool_name(parameter)"""

        for iteration in range(3):
            response = ""
            full_prompt = f"{agent_system}\n\nUser: {prompt}"

            try:
                with httpx.stream("POST", "http://localhost:11434/api/generate",
                                 json={'model': 'devstral-small-2', 'prompt': full_prompt, 'stream': True},
                                 timeout=None) as r:
                    for line in r.iter_lines():
                        if line and (token := json.loads(line).get('response', '')):
                            response += token
            except Exception as e:
                return f"Error: {e}"

            pattern = r'TOOL:(\w+)\((.*?)\)'
            matches = re.findall(pattern, response, re.DOTALL)

            if not matches:
                return response

            for tool_name, params in matches:
                tool = next((t for t in TOOLS if t.__name__ == tool_name), None)
                if tool:
                    try:
                        params = params.strip().strip('"').strip("'")
                        result = tool(params)
                        prompt = f"Tool result: {result}\n\nContinue response"
                    except Exception as e:
                        prompt = f"Tool error: {e}"

        return response

    mo.md("""
### Phase 2: Agent Loop Pattern

```
1. LLM generates response with possible tool calls
2. Parse tool names: TOOL:name(params)
3. Execute the tool
4. Feed result back to LLM
5. Repeat max 3 times
```

**Tool Calling Format:**
```
TOOL:read_python_file("/path/to/file.py")
TOOL:list_python_files(".")
```

**Key Advancement:** Agent can now read files and list directories!
""")
    return agent_with_tools, read_python_file, list_python_files

@app.cell
def __(mo):
    mo.md("""
### Phase 2 Demo

Agent now has access to:
- 📁 List files in directories
- 📄 Read file contents
- 🔄 Iterate and refine using file data

The agent moves from "just chat" to "can take actions".
""")

# ============================================================================
# PHASE 3: CONTEXT-AWARE AGENT
# ============================================================================

@app.cell
def __(mo):
    mo.md("""
## Phase 3: Context-Aware Agent 🧠

**New Capability**: Agent understands PROJECT structure

**Why**: Context-aware agents make better decisions

**New Tools**: analyze_project, find_functions

**Concepts**:
- Project structure analysis
- Function extraction from code
- Context building for decisions
""")

@app.cell
def __(mo, ast, json, glob, os):
    def analyze_project(directory: str = ".") -> str:
        """Analyze and describe the project structure."""
        try:
            py_files = glob.glob(os.path.join(directory, "**", "*.py"), recursive=True)
            stats = {
                "python_files": len(py_files),
                "total_lines": sum(len(open(f).readlines()) for f in py_files if os.path.isfile(f))
            }
            return json.dumps(stats, indent=2)
        except Exception as e:
            return f"Error: {e}"

    def find_functions(filepath: str) -> str:
        """Extract function names and signatures from a Python file."""
        try:
            with open(filepath, 'r') as f:
                tree = ast.parse(f.read())
            functions = []
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    args = [arg.arg for arg in node.args.args]
                    functions.append(f"{node.name}({', '.join(args)})")
            return "\n".join(functions) if functions else "No functions found"
        except Exception as e:
            return f"Error: {e}"

    mo.md("""
### Phase 3: Context Building

Agents now understand:
- Project structure and metrics
- Available functions and signatures
- Code organization

This enables better decision-making and planning.
""")
    return analyze_project, find_functions

@app.cell
def __(mo):
    mo.md("""
### Phase 3 Demo

Agent can now:
- 📊 Analyze project metrics
- 🔍 Find functions in files
- 🧠 Use context for decisions

"Find all functions in main.py"
→ Agent locates file, extracts functions, reports findings
""")

# ============================================================================
# PHASE 4: PLANNING AGENT
# ============================================================================

@app.cell
def __(mo):
    mo.md("""
## Phase 4: Planning Agent 📋

**New Capability**: Agent creates structured plans

**Why**: Complex tasks need decomposition

**Key Pattern**: Prompt engineering for structured output

**Concepts**:
- Task decomposition into steps
- Resource planning
- Structured decision-making
""")

@app.cell
def __(mo, httpx, json):
    def create_plan(objective: str) -> str:
        """Generate a structured plan for an objective."""
        planning_prompt = f"""Objective: {objective}

Create a 3-step plan. Format:
Step 1: [action]
Step 2: [action]
Step 3: [action]

Plan:"""

        try:
            response = ""
            with httpx.stream("POST", "http://localhost:11434/api/generate",
                             json={'model': 'devstral-small-2', 'prompt': planning_prompt, 'stream': True},
                             timeout=None) as r:
                for line in r.iter_lines():
                    if line and (token := json.loads(line).get('response', '')):
                        response += token
            return response
        except Exception as e:
            return f"Error: {e}"

    mo.md("""
### Phase 4: Planning First

Agent now plans before acting:

1. Parse objective
2. Create step-by-step plan
3. Assign tools to each step
4. Execute in order
5. Verify completion

Agent is now **strategic**, not just reactive.
""")
    return create_plan

@app.cell
def __(mo):
    mo.md("""
### Phase 4 Demo

Request: "Analyze the codebase for improvements"

Agent Response:
```
Step 1: Analyze project structure
Step 2: Find all functions and dependencies
Step 3: Identify improvement opportunities
```

Agent has become structured and deliberate.
""")

# ============================================================================
# PHASE 5: CODE GENERATION AGENT
# ============================================================================

@app.cell
def __(mo):
    mo.md("""
## Phase 5: Code Generation Agent 💻

**New Capability**: Agent writes Python code

**Why**: Automating code creation increases productivity

**New Tools**: generate_code, create_python_file

**Concepts**:
- LLM-based code synthesis
- Syntax validation (AST parsing)
- Safe file creation
""")

@app.cell
def __(mo, ast, httpx, json):
    def generate_code(description: str) -> str:
        """Generate Python code from a description."""
        prompt = f"Write Python code for: {description}\n\nCode:"

        try:
            response = ""
            with httpx.stream("POST", "http://localhost:11434/api/generate",
                             json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': True},
                             timeout=None) as r:
                for line in r.iter_lines():
                    if line and (token := json.loads(line).get('response', '')):
                        response += token
            return response
        except Exception as e:
            return f"Error: {e}"

    def create_python_file(filename: str, content: str) -> str:
        """Create a Python file with validated content."""
        try:
            ast.parse(content)
            with open(filename, 'w') as f:
                f.write(content)
            return f"File created: {filename}"
        except SyntaxError as e:
            return f"Syntax error: {e}"
        except Exception as e:
            return f"Error: {e}"

    mo.md("""
### Phase 5: Code Synthesis

Agent pipeline for code generation:

1. **Parse Request** - Understand what code is needed
2. **Generate** - LLM writes the code
3. **Validate** - AST parsing checks syntax
4. **Create** - Safe file writing
5. **Report** - Success/failure feedback

Agents now **AUTOMATE coding work**.
""")
    return generate_code, create_python_file

@app.cell
def __(mo):
    mo.md("""
### Phase 5 Demo

Request: "Create a function to validate email addresses"

Agent generates:
```python
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

File: `email_validator.py` ✅ Created

Agents are now **productive**.
""")

# ============================================================================
# PHASE 6: TESTING AGENT
# ============================================================================

@app.cell
def __(mo):
    mo.md("""
## Phase 6: Testing Agent ✅

**New Capability**: Agent tests generated code

**Why**: Working code beats existing code

**New Tool**: run_python_file

**Concepts**:
- Safe code execution
- Output capture and validation
- Full development cycle closure
""")

@app.cell
def __(mo, subprocess, ast, httpx, json):
    def run_python_file(filepath: str) -> str:
        """Run a Python file and capture output."""
        try:
            result = subprocess.run(
                ["python", filepath],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return f"✅ Success:\n{result.stdout}"
            else:
                return f"❌ Error:\n{result.stderr}"
        except subprocess.TimeoutExpired:
            return "⏱️ Timeout: Execution took too long"
        except Exception as e:
            return f"❌ Error: {e}"

    mo.md("""
### Phase 6: Full Development Cycle

Complete agent lifecycle:

1. **Understand** - Parse the request
2. **Generate** - LLM writes solution
3. **Validate** - AST checks syntax
4. **Execute** - Run code safely
5. **Verify** - Capture output
6. **Report** - Success/failure results

Agents now provide **COMPLETE SOLUTIONS**.
""")
    return run_python_file

@app.cell
def __(mo):
    mo.md("""
### Phase 6 Demo

Request: "Create and test a reversal function"

Agent Process:
1. ✅ Generate string reversal code
2. ✅ Validate syntax
3. ✅ Create `reverse.py`
4. ✅ Execute with test input
5. ✅ Capture output: "dcba" for "abcd"
6. ✅ Report success

Agent has evolved from reactive to **complete**.
""")

# ============================================================================
# INTEGRATION & SUMMARY
# ============================================================================

@app.cell
def __(mo):
    mo.md("""
## 🎯 Complete Agent Framework

### Tool Evolution

| Phase | Tools | Capability |
|-------|-------|-----------|
| 1 | chat_stream() | Talk to LLM |
| 2 | + file tools | Read/list files |
| 3 | + analysis tools | Understand code |
| 4 | + planning | Create plans |
| 5 | + generation | Write code |
| 6 | + testing | Validate code |

### Core Patterns

1. **🛠️ Tool Pattern**: Functions with docstrings become tools
2. **🔄 Agent Loop**: LLM → Parse → Execute → Feedback (max 3x)
3. **🧠 Context**: Agents understand their environment
4. **📋 Planning**: Structured task decomposition
5. **💻 Generation**: LLMs write working code
6. **✅ Testing**: Validate programmatically

### Extensibility

Add new tools instantly by:
- Writing a function
- Adding a docstring
- Including in TOOLS list

Each new tool multiplies agent capability.
""")

@app.cell
def __(mo):
    mo.md("""
## 🚀 Real-World Applications

- **Code Review Agents**: Analyze and improve code
- **Documentation Generators**: Auto-generate API docs
- **Automated Refactoring**: Improve code structure
- **Testing Assistants**: Generate and run tests
- **CI/CD Automation**: Integrate into pipelines
- **Bug Fixers**: Identify and propose solutions

### The Framework is Infinitely Extensible

Start simple, add tools progressively. Each tool adds exponential capability.

---

**Created with marimo 📊**
Interactive presentation of progressive agent development.
""")

if __name__ == "__main__":
    app.run()
