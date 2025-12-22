import httpx
import json
import subprocess
import os
import glob

def chat_stream(prompt):
    full = ""
    with httpx.stream("POST", "http://localhost:11434/api/generate",
                     json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': True}) as r:
        for line in r.iter_lines():
            if line and (token := json.loads(line).get('response', '')):
                print(token, end='', flush=True)
                full += token
    return full

def analyze_project():
    files = glob.glob("**/*.py", recursive=True)
    context = "Project structure:\n"
    for f in files[:5]:
        with open(f, 'r') as file:
            content = file.read()[:150]
            context += f"\n{f}:\n{content}...\n"
    return context

def create_plan(task):
    prompt = f"""Create a detailed development plan for: {task}

Format as numbered steps:
1. Step one
2. Step two
etc.

Be specific and actionable for Python development."""

    response = chat_stream(prompt)
    steps = []
    for line in response.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            steps.append(line)
    return steps

def generate_code(description, filename=None):
    if not filename:
        if "test" in description.lower():
            filename = "test_generated.py"
        elif "main" in description.lower():
            filename = "main_generated.py"
        else:
            filename = "generated.py"

    prompt = f"""Write complete Python code for: {description}

Requirements:
- Working, executable code
- Proper functions and classes
- Error handling where needed
- Include main section if appropriate

Return only Python code."""

    code = chat_stream(prompt)

    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    return code, filename

def test_code(filename):
    if not os.path.exists(filename):
        return False, f"File {filename} not found"

    with open(filename, 'r') as f:
        code = f.read()
    compile(code, filename, 'exec')

    result = subprocess.run(['python', filename],
                          capture_output=True, text=True, timeout=10)

    if result.returncode == 0:
        return True, f"✓ {filename} works correctly"
    else:
        return False, f"✗ Runtime error: {result.stderr}"

def full_development_workflow(request):
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
    code, filename = generate_code(request)

    with open(filename, 'w') as f:
        f.write(code)
    result += f"Created {filename}:\n{code[:200]}...\n\n"

    result += "🧪 Step 4: Testing & Validation\n"
    success, message = test_code(filename)
    result += message + "\n\n"

    result += "📊 Step 5: Summary\n"
    if success:
        result += f"✅ Successfully completed: {request}\n"
        result += f"📁 Generated file: {filename}\n"
    else:
        result += f"⚠️  Task completed with issues. Check {filename}\n"

    return result

def main():
    print("🤖 Full Python Development Agent")
    print("Type 'quit' to exit\n")

    while True:
        request = input("Describe your development task: ").strip()

        if request.lower() == 'quit':
            break

        if not request:
            continue

        print("\n" + full_development_workflow(request))
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
