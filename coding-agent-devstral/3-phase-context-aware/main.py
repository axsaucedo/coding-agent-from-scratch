import glob
import httpx
import json

def chat_stream(prompt):
    print(f"Received prompt: {prompt}")
    full = ""
    with httpx.stream("POST", "http://localhost:11434/api/generate",
                     json={
                         'model': 'devstral-small-2',
                         'prompt': prompt,
                         'stream': True
                     }) as r:
        for line in r.iter_lines():
            if line and (token := json.loads(line).get('response', '')):
                print(token, end='', flush=True)
                full += token
    print()
    return full

def analyze_project():
    files = glob.glob("**/*.py", recursive=True)
    context = "Project Analysis:\n"
    for f in files[:5]:
        with open(f, 'r') as file:
            content = file.read()[:200]
            context += f"\nFile {f}:\n{content}...\n"
    return context

def find_functions():
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

def context_aware_agent(prompt):
    prompt_lower = prompt.lower()
    if "analyze this python project" in prompt_lower or "analyze project" in prompt_lower:
        context = analyze_project()
        return chat_stream(f"Based on this project structure: {context}\nProvide a summary of what this codebase does.")
    elif "what does this codebase do" in prompt_lower:
        context = analyze_project()
        return chat_stream(f"Based on these files: {context}\nExplain what this codebase is for.")
    elif "find all functions" in prompt_lower or "list functions" in prompt_lower:
        functions = find_functions()
        return f"Functions found:\n" + "\n".join(functions) if functions else "No functions found in Python files."
    else:
        return chat_stream(prompt)

if __name__ == "__main__":
    print(context_aware_agent(input("Ask: ")))