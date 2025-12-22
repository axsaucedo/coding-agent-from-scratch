import subprocess
import os
import glob

from phase_2.main import agent_with_tools, read_python_file, list_python_files
from phase_3.main import analyze_project, find_functions
from phase_4.main import create_plan
from phase_5.main import generate_code, create_python_file
from phase_6.main import test_python_file, validate_code

def full_development_workflow(request):
    """Execute complete development workflow: analyze, plan, code, test."""
    result = f"🤖 Full Development Agent\n{'='*50}\n"

    result += "📋 Step 1: Project Analysis\n"
    context = analyze_project()
    result += context + "\n"

    result += "📝 Step 2: Development Plan\n"
    plan = create_plan(request)
    if plan:
        for step in plan:
            result += f"  {step}\n"
    result += "\n"

    result += "💻 Step 3: Code Generation\n"
    code = generate_code(request)

    filename = "generated.py"
    with open(filename, 'w') as f:
        f.write(code)
    result += f"Created {filename}:\n{code[:200]}...\n\n"

    result += "🧪 Step 4: Testing & Validation\n"
    test_result = test_python_file(filename)
    result += test_result + "\n\n"

    result += "📊 Step 5: Summary\n"
    if "✓" in test_result:
        result += f"✅ Successfully completed: {request}\n"
        result += f"📁 Generated file: {filename}\n"
    else:
        result += f"⚠️  Task completed with issues. Check {filename}\n"

    return result

TOOLS = [read_python_file, list_python_files, analyze_project, find_functions, create_plan,
         generate_code, create_python_file, test_python_file, validate_code, full_development_workflow]

def full_agent(user_input):
    return agent_with_tools(user_input, tools=TOOLS)

def main():
    print("🤖 Full Python Development Agent")
    print("Type 'quit' to exit\n")

    while True:
        request = input("Describe your development task: ").strip()

        if request.lower() == 'quit':
            break

        if not request:
            continue

        print("\n" + full_agent(request))
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
