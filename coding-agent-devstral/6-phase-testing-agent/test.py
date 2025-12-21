import subprocess
import requests
import os

def judge_response(response, expected_behavior):
    """Use LLM to judge if response meets expected behavior"""
    prompt = f"""Judge this response: "{response}"
    Expected: {expected_behavior}
    Answer only: PASS or FAIL"""

    try:
        result = requests.post('http://localhost:11434/api/generate',
                              json={'model': 'devstral-2-small', 'prompt': prompt, 'stream': False})
        return 'PASS' in result.json()['response'].upper()
    except:
        return False

def cleanup_test_files():
    """Remove generated test files"""
    files_to_remove = ['hello_test.py', 'calc_test.py', 'generated_test.py', 'broken_test.py']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)

def test_create_and_validate():
    """Test creating hello world and validating it works"""
    cleanup_test_files()

    result = subprocess.run(['python', 'main.py'],
                          input='Create hello world and test it\n',
                          capture_output=True, text=True, cwd='.')

    success = judge_response(result.stdout, "Created working Python code and validated it runs successfully")
    cleanup_test_files()
    assert success

def test_function_with_tests():
    """Test creating function with unit tests"""
    cleanup_test_files()

    result = subprocess.run(['python', 'main.py'],
                          input='Create function with unit tests and run them\n',
                          capture_output=True, text=True, cwd='.')

    success = judge_response(result.stdout, "Created Python function with tests and verified they work")
    cleanup_test_files()
    assert success

def test_syntax_error_detection():
    """Test syntax error detection"""
    cleanup_test_files()

    # Create a file with syntax error for testing
    with open('broken_test.py', 'w') as f:
        f.write('def broken_function(\n    print("missing colon and parenthesis")')

    result = subprocess.run(['python', 'main.py'],
                          input='check syntax errors in broken_test.py\n',
                          capture_output=True, text=True, cwd='.')

    success = judge_response(result.stdout, "Detects and reports syntax errors in Python file")
    cleanup_test_files()
    assert success