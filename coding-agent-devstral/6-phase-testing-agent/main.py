import httpx
import json
import subprocess
import os

def chat_stream(prompt):
    full = ""
    with httpx.stream("POST", "http://localhost:11434/api/generate",
                     json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': True}) as r:
        for line in r.iter_lines():
            if line and (token := json.loads(line).get('response', '')):
                print(token, end='', flush=True)
                full += token
    return full

def test_python_file(filepath):
    if not os.path.exists(filepath):
        return False, f"File {filepath} not found"

    with open(filepath, 'r') as f:
        code = f.read()

    compile(code, filepath, 'exec')

    result = subprocess.run(['python', filepath],
                          capture_output=True, text=True, timeout=10)

    if result.returncode == 0:
        return True, f"✓ {filepath} runs successfully"
    else:
        return False, f"✗ {filepath} failed: {result.stderr}"

def create_and_test_code(description):
    if "hello" in description.lower():
        filename = "hello_test.py"
    elif "calculator" in description.lower():
        filename = "calc_test.py"
    else:
        filename = "generated_test.py"

    code_prompt = f"""Write working Python code for: {description}

Requirements:
- Complete, runnable code
- Include proper error handling
- Make it simple but functional
- If it's a function, include a test call in main section

Only return the Python code."""

    code = chat_stream(code_prompt)

    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    with open(filename, 'w') as f:
        f.write(code)

    success, message = test_python_file(filename)

    result = f"Created {filename}:\n{code}\n\nTest result: {message}"

    return result

def testing_agent(user_input):
    user_input_lower = user_input.lower()

    if "create" in user_input_lower and "test" in user_input_lower:
        return create_and_test_code(user_input)

    elif "check" in user_input_lower and "syntax" in user_input_lower:
        words = user_input.split()
        for word in words:
            if word.endswith('.py'):
                success, message = test_python_file(word)
                return message

        return "Please specify a .py file to check"

    elif user_input_lower.startswith("create ") and ("hello" in user_input_lower or
                                                      "calculator" in user_input_lower or
                                                      "function" in user_input_lower):
        return create_and_test_code(user_input)

    else:
        return chat_stream(user_input)

if __name__ == "__main__":
    user_request = input("What would you like to create and test: ")
    print("\n" + testing_agent(user_request))