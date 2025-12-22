import subprocess
import os

from phase_2.main import agent_with_tools, read_python_file, list_python_files
from phase_3.main import analyze_project, find_functions
from phase_4.main import create_plan
from phase_5.main import generate_code, create_python_file

def run_python_file(filepath):
    """Run a Python file and check if it executes without errors."""
    if not os.path.exists(filepath):
        return f"File {filepath} not found"

    with open(filepath, 'r') as f:
        code = f.read()

    compile(code, filepath, 'exec')

    result = subprocess.run(['python', filepath],
                          capture_output=True, text=True, timeout=10)

    if result.returncode == 0:
        return f"{filepath} runs successfully"
    else:
        return f"{filepath} failed: {result.stderr}"

TOOLS = [read_python_file, list_python_files, analyze_project, find_functions, create_plan,
         generate_code, create_python_file, run_python_file]

def code_testing_agent(user_input):
    return agent_with_tools(user_input, tools=TOOLS)

if __name__ == "__main__":
    print(code_testing_agent(input("What would you like to create and test: ")))
