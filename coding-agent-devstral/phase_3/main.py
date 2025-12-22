import glob

from phase_1.main import chat_stream
from phase_2.main import agent_with_tools, read_python_file, list_python_files


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
    return functions

TOOLS = [read_python_file, list_python_files, analyze_project, find_functions]

def context_aware_agent(user_input):
    return agent_with_tools(user_input, tools=TOOLS)

if __name__ == "__main__":
    print(context_aware_agent(input("Ask: ")))
