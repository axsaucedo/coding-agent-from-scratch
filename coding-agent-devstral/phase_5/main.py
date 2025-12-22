import os

from phase_1.main import chat_stream
from phase_2.main import agent_with_tools, read_python_file, list_python_files
from phase_3.main import analyze_project, find_functions
from phase_4.main import create_plan

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

TOOLS = [read_python_file, list_python_files, analyze_project, find_functions, create_plan, generate_code, create_python_file]

def code_creator_agent(user_input):
    return agent_with_tools(user_input, tools=TOOLS)

if __name__ == "__main__":
    print(code_creator_agent(input("Describe what to create: ")))
