import requests
import glob
import os

def chat(prompt):
    """Send prompt to ollama, return response"""
    try:
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   'model': 'devstral-small-2',
                                   'prompt': prompt,
                                   'stream': False
                               })
        return response.json()['response']
    except Exception as e:
        return f"Error: {e}"

def analyze_project():
    """Analyze Python project structure"""
    files = glob.glob("**/*.py", recursive=True)
    context = "Project Analysis:\n"

    for f in files[:5]:  # Limit to 5 files to avoid context overflow
        try:
            with open(f, 'r') as file:
                content = file.read()[:200]  # First 200 chars
                context += f"\nFile {f}:\n{content}...\n"
        except Exception as e:
            context += f"\nFile {f}: Error reading - {e}\n"

    return context

def find_functions():
    """Find all functions in Python files"""
    files = glob.glob("**/*.py", recursive=True)
    functions = []

    for f in files:
        try:
            with open(f, 'r') as file:
                lines = file.readlines()
                for line_num, line in enumerate(lines, 1):
                    if line.strip().startswith('def '):
                        func_name = line.strip().split('(')[0].replace('def ', '')
                        functions.append(f"{f}:{line_num} - {func_name}")
        except Exception:
            continue

    return functions

def context_aware_agent(prompt):
    """Agent that understands project context"""
    prompt_lower = prompt.lower()

    if "analyze this python project" in prompt_lower or "analyze project" in prompt_lower:
        context = analyze_project()
        analysis_prompt = f"Based on this project structure: {context}\nProvide a summary of what this codebase does."
        return chat(analysis_prompt)

    elif "what does this codebase do" in prompt_lower:
        context = analyze_project()
        summary_prompt = f"Based on these files: {context}\nExplain what this codebase is for."
        return chat(summary_prompt)

    elif "find all functions" in prompt_lower or "list functions" in prompt_lower:
        functions = find_functions()
        if functions:
            return f"Functions found:\n" + "\n".join(functions)
        else:
            return "No functions found in Python files."

    else:
        return chat(prompt)

if __name__ == "__main__":
    print(context_aware_agent(input("Ask: ")))