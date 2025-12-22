import httpx
import json
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

def create_python_file(description, filename=None):
    if not filename:
        if "hello" in description.lower():
            filename = "hello.py"
        elif "calculator" in description.lower() or "calc" in description.lower():
            filename = "calculator.py"
        elif "test" in description.lower():
            filename = "test_" + description.lower().split()[1] + ".py" if len(description.split()) > 1 else "test.py"
        else:
            filename = "generated_code.py"

    code_prompt = f"""Write Python code for: {description}

Requirements:
- Complete, working Python code
- Include proper function definitions
- Add basic error handling where appropriate
- Include a main section if it's a script
- Make it simple and functional

Only return the Python code, no explanations."""

    code = chat_stream(code_prompt)

    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    with open(filename, 'w') as f:
        f.write(code)
    return filename, code

def code_creator_agent(user_input):
    user_input_lower = user_input.lower()

    if "create" in user_input_lower and ("python" in user_input_lower or "program" in user_input_lower):
        filename = None
        words = user_input.split()
        for i, word in enumerate(words):
            if word.endswith('.py'):
                filename = word
                break

        created_file, result = create_python_file(user_input, filename)

        if created_file:
            return f"Created {created_file}:\n\n{result}"
        else:
            return result

    else:
        return chat_stream(user_input)

if __name__ == "__main__":
    user_request = input("Describe what to create: ")
    print("\n" + code_creator_agent(user_request))