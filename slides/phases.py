# %% Notebook: Progressive Coding Agent - Interactive Phase Exploration
import marimo

__generated_with = "0.18.4"
app = marimo.App()

# %% markdown
md = """
# Progressive Coding Agent: From Chat to Full Development Cycle

This notebook demonstrates the evolution of an AI agent through 6 progressive phases,
building from basic LLM communication to a complete code generation and testing system.

Each phase builds on the previous one, adding new capabilities while maintaining existing functionality.
"""

# %% markdown
md_setup = """
## Setup: Verifying Ollama Connection
"""

# %% Setup cell - Verify Ollama and imports
import httpx
import json
import requests
import glob
import re
import ast
import subprocess
import os

# Verify Ollama is running
try:
    response = httpx.get("http://localhost:11434/api/tags", timeout=2)
    if response.status_code == 200:
        print("✓ Ollama is running on localhost:11434")
        print("✓ Using model: devstral-small-2")
    else:
        print("✗ Ollama endpoint returned error")
except Exception as e:
    print(f"✗ Could not connect to Ollama: {e}")

# %% markdown
md_phase1 = """
## Phase 1: Basic LLM Chat - Foundation

The simplest agent - direct streaming communication with Ollama.
"""

# %% Phase 1: Code
def chat(prompt, system_prompt=""):
    response, full_prompt = "", f"System prompt: {system_prompt}\nUser: {prompt}"
    print(f"Received: {full_prompt}")
    response = requests.post('http://localhost:11434/api/generate',
                           json={
                               'model': 'devstral-small-2',
                               'prompt': prompt,
                               'stream': False
                           })
    val = response.json()['response']
    print(f"Result: {val}")
    return val


def chat_stream(prompt, system_prompt=""):
    response, full_prompt = "", f"System prompt: {system_prompt}\nUser: {prompt}"
    print(f"Received: {full_prompt}")
    with httpx.stream("POST", "http://localhost:11434/api/generate",
                     json={'model': 'devstral-small-2', 'prompt': full_prompt, 'stream': True},
                     timeout=None) as r:
        for line in r.iter_lines():
            if line and (token := json.loads(line).get('response', '')):
                print(token, end='', flush=True)
                response += token
    print()
    return response

# %% Phase 1: Example
print("Phase 1 Example: Basic Chat")
print("=" * 50)
result = chat_stream("What is the capital of France?")
print(f"\nFinal response: {result[:100]}...")

# %% markdown
md_phase2 = """
## Phase 2: Tool-Enabled Agent - Taking Actions

Agent can now use tools to read files and explore directories via TOOL:name(params) format.
"""

# %% Phase 2: Code
def read_python_file(filepath):
    """Read and return the contents of a Python file."""
    with open(filepath, 'r') as f:
        return f.read()

def list_python_files():
    """List all Python files in the current directory."""
    return glob.glob("*.py")

TOOLS_PHASE2 = [read_python_file, list_python_files]
TOOL_MAP_PHASE2 = {fn.__name__: fn for fn in TOOLS_PHASE2}

def agent_with_tools(user_input, tools=TOOLS_PHASE2, system_prompt=""):
    tool_map = {fn.__name__: fn for fn in tools}
    tools_desc = "\n".join([f"- {fn.__name__}: {fn.__doc__}" for fn in tools])

    system = f"""You are a helpful assistant with access to tools.

Available tools:
{tools_desc}

When you need to use a tool, call it using TOOL:<tool_name>(params).

Examples:
- TOOL:read_python_file("hello.py")
- TOOL:list_python_files()

When done using tools or if no tools required, respond with TOOL:NONE.

After using a tool, the output will be provided as context."""

    prompt = f"{system}\n\nUser: {user_input}"

    for iteration in range(3):
        response = chat_stream(prompt, system_prompt=system_prompt)

        tool_match = re.search(r'TOOL:(\w+)\((.*?)\)', response, re.DOTALL)

        if not tool_match:
            return response

        tool_name = tool_match.group(1)
        params_str = tool_match.group(2).strip()

        if tool_name == "NONE":
            return response

        if tool_name in tool_map:
            if params_str:
                try:
                    params = ast.literal_eval(f"[{params_str}]")
                except (SyntaxError, ValueError):
                    params = [params_str]
            else:
                params = []

            result = tool_map[tool_name](*params)
            prompt = f"{system}\n\nTool executed: {tool_name}({params_str})\nResult:\n{result}\n\nNow provide your response; do not comment about the tools and only provide the response on the original request from the user:"
        else:
            return response

    return response

# %% Phase 2: Example
print("\nPhase 2 Example: Tool-Enabled Agent")
print("=" * 50)
result = agent_with_tools("List Python files in this directory")
print(f"Result:\n{result[:200]}...")

# %% markdown
md_phase3 = """
## Phase 3: Context-Aware Agent - Project Understanding

Agent now understands project structure and can find functions within files.
"""

# %% Phase 3: Code
def analyze_project():
    """Analyze Python project structure and summarize contents."""
    files = glob.glob("**/*.py", recursive=True)
    context = "Project structure:\n"
    for f in files[:5]:
        with open(f, 'r') as file:
            content = file.read()[:150]
            context += f"\n{f}:\n{content}...\n"
    return context

def find_functions():
    """Find all function definitions in Python files."""
    files = glob.glob("**/*.py", recursive=True)
    functions = []
    for f in files:
        with open(f, 'r') as file:
            lines = file.readlines()
            for line_num, line in enumerate(lines, 1):
                if line.strip().startswith('def '):
                    func_name = line.strip().split('(')[0].replace('def ', '')
                    functions.append(f"{f}:{line_num} - {func_name}")
    return functions[:10]  # Limit output

TOOLS_PHASE3 = [read_python_file, list_python_files, analyze_project, find_functions]

def context_aware_agent(user_input):
    return agent_with_tools(user_input, tools=TOOLS_PHASE3)

# %% Phase 3: Example
print("\nPhase 3 Example: Context-Aware Agent")
print("=" * 50)
functions = find_functions()
print(f"Found functions:\n{chr(10).join(functions[:5])}")

# %% markdown
md_phase4 = """
## Phase 4: Planning Agent - Structured Reasoning

Agent creates detailed step-by-step plans for complex tasks.
"""

# %% Phase 4: Code
def create_plan():
    "Create a detailed step by step plan for simple and complex applications."
    guiding_prompt = f"""Create a detailed step-by-step plan for the text provided by the user.

Format your response as numbered steps:
1. Step one
2. Step two
etc.

Be specific and actionable. Keep it to only a few simple steps and keep it simple and basic unless specified otherwise.

Only reply with the plan and do not reply with anything else."""
    return guiding_prompt

TOOLS_PHASE4 = [read_python_file, list_python_files, analyze_project, find_functions]

def planning_agent(user_input):
    return agent_with_tools(user_input, tools=TOOLS_PHASE4)

# %% Phase 4: Example
print("\nPhase 4 Example: Planning Agent")
print("=" * 50)
plan = planning_agent("Build a web scraper for news websites")
print(f"Generated plan:\n{plan[:300]}...")

# %% markdown
md_phase5 = """
## Phase 5: Code Generation Agent - Creating Code

Agent can now generate Python code from descriptions and save it to files.
"""

# %% Phase 5: Code
def generate_code(description):
    """Generate Python code from a description."""
    code_prompt = f"""Write Python code for: {description}

Requirements:
- Complete, working Python code
- Include proper function definitions
- Add basic error handling where appropriate
- Include a main section if it's a script
- Make it simple and functional

Only return the Python code, nothing else (e.g. no text, explanations, etc)."""

    code = chat_stream(code_prompt)

    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    return code

def create_python_file(description, filename="generated.py"):
    """Create and save a Python file from description."""
    code = generate_code(description)
    with open(filename, 'w') as f:
        f.write(code)
    return filename

TOOLS_PHASE5 = [read_python_file, list_python_files, analyze_project, find_functions, create_plan, generate_code, create_python_file]

def code_creator_agent(user_input):
    return agent_with_tools(user_input, tools=TOOLS_PHASE5)

# %% Phase 5: Example
print("\nPhase 5 Example: Code Generation")
print("=" * 50)
code = generate_code("A function that calculates the factorial of a number")
print(f"Generated code:\n{code[:200]}...")

# %% markdown
md_phase6 = """
## Phase 6: Testing Agent - Full Development Cycle

The complete agent: generates code, saves it, executes it, and validates results.
"""

# %% Phase 6: Code
def run_python_file(filepath):
    """Run a Python file and check if it executes without errors."""
    if not os.path.exists(filepath):
        return f"File {filepath} not found"

    with open(filepath, 'r') as f:
        code = f.read()

    try:
        compile(code, filepath, 'exec')
    except SyntaxError as e:
        return f"Syntax error in {filepath}: {e}"

    try:
        result = subprocess.run(['python', filepath],
                              capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            return f"✓ {filepath} runs successfully\nOutput:\n{result.stdout}"
        else:
            return f"✗ {filepath} failed:\n{result.stderr}"
    except subprocess.TimeoutExpired:
        return f"✗ {filepath} timed out (>10 seconds)"
    except Exception as e:
        return f"✗ Error running {filepath}: {e}"

TOOLS_PHASE6 = [read_python_file, list_python_files, analyze_project, find_functions, create_plan,
         generate_code, create_python_file, run_python_file]

def code_testing_agent(user_input):
    return agent_with_tools(user_input, tools=TOOLS_PHASE6)

# %% Phase 6: Example - Full Pipeline
print("\nPhase 6 Example: Full Pipeline (Generate → Save → Execute)")
print("=" * 50)

# Generate a simple function
code = generate_code("A function that returns the sum of numbers 1 to N")
with open("/tmp/demo_phase6.py", 'w') as f:
    f.write(code)
print("✓ Code generated and saved")

# Execute it
result = run_python_file("/tmp/demo_phase6.py")
print(f"Execution result:\n{result}")

# %% markdown
md_summary = """
## Summary: The Complete Agent Framework

We built a progressive agent system that evolved through 6 phases:

1. **Phase 1**: Basic LLM communication with streaming
2. **Phase 2**: Tool calling with regex-based parsing
3. **Phase 3**: Project analysis and code understanding
4. **Phase 4**: Structured task planning
5. **Phase 5**: Code generation from descriptions
6. **Phase 6**: Full development cycle with execution

Each phase **builds on previous capabilities** while adding new ones.
The same `agent_with_tools()` function powers all phases - just with different tool sets.

### Key Takeaways
- ✓ Tool pattern: Docstrings become auto-discovered tools
- ✓ Agent loop: LLM → Parse → Execute → Feedback
- ✓ Progressive enhancement: Simple → Complex
- ✓ Extensible: Add tools, extend capabilities infinitely
"""
