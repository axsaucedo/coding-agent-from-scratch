from phase_2.main import agent_with_tools, read_python_file, list_python_files
from phase_3.main import analyze_project, find_functions

def create_plan(task):
    """Create a detailed step-by-step plan for a development task."""
    from phase_1.main import chat_stream

    prompt = f"""Create a detailed step-by-step plan for: {task}

Format your response as numbered steps:
1. Step one
2. Step two
etc.

Be specific and actionable."""

    response = chat_stream(prompt)
    steps = []
    for line in response.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            steps.append(line)
    return steps

TOOLS = [read_python_file, list_python_files, analyze_project, find_functions, create_plan]

def planning_agent(user_input):
    return agent_with_tools(user_input, tools=TOOLS)

if __name__ == "__main__":
    print(planning_agent(input("Describe your task: ")))
