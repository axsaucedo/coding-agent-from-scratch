import subprocess
import requests
import os
import sys

PYTHON_BIN = sys.executable

def judge_response(response, expected_behavior):
    """Use LLM to judge if response meets expected behavior"""
    prompt = f"""Judge this response: "{response}"
    Expected: {expected_behavior}
    Answer only: PASS or FAIL"""

    try:
        result = requests.post('http://localhost:11434/api/generate',
                              json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': False})
        return 'PASS' in result.json()['response'].upper()
    except:
        return False

def setup_test_project():
    """Create test Python files for project analysis"""
    test_dir = '3-phase-context-aware/testproject'
    os.makedirs(test_dir, exist_ok=True)

    with open(f'{test_dir}/calc.py', 'w') as f:
        f.write('''def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

if __name__ == "__main__":
    print("Calculator module")
''')

    with open(f'{test_dir}/main.py', 'w') as f:
        f.write('''from calc import add, multiply

def main():
    result = add(5, 3)
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
''')

def cleanup_test_project():
    """Remove test project files"""
    import shutil
    test_dir = '3-phase-context-aware/testproject'
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

def test_project_analysis():
    """Test project structure analysis"""
    setup_test_project()
    try:
        result = subprocess.run([PYTHON_BIN, 'main.py'],
                              input='analyze this python project\n',
                              capture_output=True, text=True, cwd='3-phase-context-aware')
        assert judge_response(result.stdout, "Identifies Python files and describes project components")
    finally:
        cleanup_test_project()

def test_codebase_summary():
    """Test codebase summary generation"""
    setup_test_project()
    try:
        result = subprocess.run([PYTHON_BIN, 'main.py'],
                              input='what does this codebase do\n',
                              capture_output=True, text=True, cwd='3-phase-context-aware')
        assert judge_response(result.stdout, "Provides accurate description of what the code does")
    finally:
        cleanup_test_project()

def test_function_discovery():
    """Test function finding capability"""
    setup_test_project()
    try:
        result = subprocess.run([PYTHON_BIN, 'main.py'],
                              input='find all functions\n',
                              capture_output=True, text=True, cwd='3-phase-context-aware')
        assert judge_response(result.stdout, "Lists Python functions found in the project files")
    finally:
        cleanup_test_project()