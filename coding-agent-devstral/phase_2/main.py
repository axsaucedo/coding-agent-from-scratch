import glob
import re
import ast

from phase_1.main import chat_stream

def read_python_file(filepath):
    """Read and return the contents of a Python file."""
    with open(filepath, 'r') as f:
        return f.read()

def list_python_files():
    """List all Python files in the current directory."""
    return glob.glob("*.py")

TOOLS = [read_python_file, list_python_files]
TOOL_MAP = {fn.__name__: fn for fn in TOOLS}

def agent_with_tools(user_input, tools=None):
    if tools is None:
        tools = TOOLS

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
        response = chat_stream(prompt)

        tool_match = re.search(r'TOOL:(\w+)\((.*?)\)', response)

        if not tool_match:
            return response

        tool_name = tool_match.group(1)
        params_str = tool_match.group(2).strip()

        if tool_name == "NONE":
            return response

        if tool_name in tool_map:
            if params_str:
                params = ast.literal_eval(f"[{params_str}]")
            else:
                params = []

            result = tool_map[tool_name](*params)
            prompt = f"{system}\n\nTool executed: {tool_name}({params_str})\nResult:\n{result}\n\nNow provide your analysis:"
        else:
            return response

    return response

if __name__ == "__main__":
    print(agent_with_tools(input("Ask: ")))
