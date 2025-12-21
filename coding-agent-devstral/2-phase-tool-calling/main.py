import requests
import os
import glob

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

def read_file(path):
    """Read file content"""
    try:
        with open(path, 'r') as f:
            return f.read()
    except Exception as e:
        return f"Error reading {path}: {e}"

def list_python_files():
    """List Python files in current directory"""
    return glob.glob("*.py")

def agent_with_tools(prompt):
    """Agent that can use tools based on prompt"""
    if "read file" in prompt.lower():
        # Extract file path - simple approach
        words = prompt.split()
        for word in words:
            if word.endswith('.py'):
                return read_file(word)
        return "Please specify a .py file to read"

    elif "list python files" in prompt.lower() or "python files" in prompt.lower():
        files = list_python_files()
        return f"Python files found: {', '.join(files)}"

    elif "what's in" in prompt.lower() and ".py" in prompt.lower():
        # Extract filename
        words = prompt.split()
        for word in words:
            if word.endswith('.py'):
                content = read_file(word)
                return f"Content of {word}:\n{content}"
        return "Please specify a .py file"

    else:
        return chat(prompt)

if __name__ == "__main__":
    print(agent_with_tools(input("Ask: ")))