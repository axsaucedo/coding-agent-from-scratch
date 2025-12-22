import json
from phase_1.main import chat_stream
from phase_2.main import agent_with_tools, read_python_file, list_python_files
from phase_3.main import analyze_project, find_functions

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

TOOLS = [read_python_file, list_python_files, analyze_project, find_functions]

def planning_agent(user_input):
    return agent_with_tools(user_input, tools=TOOLS)

if __name__ == "__main__":
    print(planning_agent(input("Describe your task: ")))
