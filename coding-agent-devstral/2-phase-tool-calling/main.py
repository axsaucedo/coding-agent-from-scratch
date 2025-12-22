import httpx
import json
import glob
import re
import ast

MAX_TOOL_ATTEMPTS=3

def read_python_file(filepath):
    """Read and return the contents of a Python file."""
    with open(filepath, 'r') as f:
        return f.read()

def list_python_files():
    """List all Python files in the current directory."""
    return glob.glob("*.py")

TOOLS = [read_python_file, list_python_files]
TOOL_MAP = {fn.__name__: fn for fn in TOOLS}

def chat_stream(prompt):
    full = ""
    with httpx.stream("POST", "http://localhost:11434/api/generate",
                     json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': True},
                     timeout=None) as r:
        for line in r.iter_lines():
            if line and (token := json.loads(line).get('response', '')):
                print(token, end='', flush=True)
                full += token
    print()
    return full

def agent_with_tools(user_input):
    tools_desc = "\n".join([f"- {fn.__name__}: {fn.__doc__}" for fn in TOOLS])

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

    for iteration in range(MAX_TOOL_ATTEMPTS):
        response = chat_stream(prompt)

        tool_match = re.search(r'TOOL:(\w+)\((.*?)\)', response)

        if not tool_match:
            return response

        tool_name = tool_match.group(1)
        params_str = tool_match.group(2).strip()

        if tool_name == "NONE":
            return response

        if tool_name in TOOL_MAP:
            if params_str:
                params = ast.literal_eval(f"[{params_str}]")
            else:
                params = []

            result = TOOL_MAP[tool_name](*params)
            prompt = f"{system}\n\nTool executed: {tool_name}({params_str})\nResult:\n{result}\n\nNow provide your analysis:"
        else:
            return response

    return response

if __name__ == "__main__":
    print(agent_with_tools(input("Ask: ")))
