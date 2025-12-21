import requests
import subprocess
import os

def chat(prompt):
    """Send prompt to ollama, return response"""
    try:
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   'model': 'devstral-2-small',
                                   'prompt': prompt,
                                   'stream': False
                               })
        return response.json()['response']
    except Exception as e:
        return f"Error: {e}"

def test_python_file(filepath):
    """Test if Python file runs without errors"""
    if not os.path.exists(filepath):
        return False, f"File {filepath} not found"

    try:
        # Check syntax first
        with open(filepath, 'r') as f:
            code = f.read()

        compile(code, filepath, 'exec')

        # Try to run the file
        result = subprocess.run(['python', filepath],
                              capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            return True, f"✓ {filepath} runs successfully"
        else:
            return False, f"✗ {filepath} failed: {result.stderr}"

    except SyntaxError as e:
        return False, f"✗ Syntax error in {filepath}: {e}"
    except subprocess.TimeoutExpired:
        return False, f"✗ {filepath} timed out"
    except Exception as e:
        return False, f"✗ Error testing {filepath}: {e}"

def create_and_test_code(description):
    """Create code from description and test it"""
    # Generate filename
    if "hello" in description.lower():
        filename = "hello_test.py"
    elif "calculator" in description.lower():
        filename = "calc_test.py"
    else:
        filename = "generated_test.py"

    # Generate code
    code_prompt = f"""Write working Python code for: {description}

Requirements:
- Complete, runnable code
- Include proper error handling
- Make it simple but functional
- If it's a function, include a test call in main section

Only return the Python code."""

    code = chat(code_prompt)

    # Clean up response
    if "```python" in code:
        code = code.split("```python")[1].split("```")[0].strip()
    elif "```" in code:
        code = code.split("```")[1].split("```")[0].strip()

    # Write and test file
    try:
        with open(filename, 'w') as f:
            f.write(code)

        success, message = test_python_file(filename)

        result = f"Created {filename}:\n{code}\n\nTest result: {message}"

        return result

    except Exception as e:
        return f"Error creating/testing file: {e}"

def testing_agent(user_input):
    """Agent that creates code and validates it works"""
    user_input_lower = user_input.lower()

    if "create" in user_input_lower and "test" in user_input_lower:
        return create_and_test_code(user_input)

    elif "check" in user_input_lower and "syntax" in user_input_lower:
        # Extract filename
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
        return chat(user_input)

if __name__ == "__main__":
    user_request = input("What would you like to create and test: ")
    print("\n" + testing_agent(user_request))