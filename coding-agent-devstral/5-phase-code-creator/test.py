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

def cleanup_generated_files():
    """Remove generated test files"""
    files_to_remove = ['hello.py', 'calculator.py', 'test_calculator.py']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)

def test_hello_world_creation():
    """Test creating hello world program"""
    cleanup_generated_files()

    result = subprocess.run(['python', 'main.py'],
                          input='Create hello world program\n',
                          capture_output=True, text=True, cwd='.')

    # Check if hello.py was created and works
    if os.path.exists('hello.py'):
        run_result = subprocess.run(['python', 'hello.py'],
                                  capture_output=True, text=True, cwd='.')
        success = run_result.returncode == 0
        cleanup_generated_files()
        assert success and judge_response(result.stdout, "Created working Python hello world program")
    else:
        cleanup_generated_files()
        assert False, "hello.py was not created"

def test_calculator_creation():
    """Test creating calculator with functions"""
    cleanup_generated_files()

    result = subprocess.run(['python', 'main.py'],
                          input='Create calculator with add and subtract\n',
                          capture_output=True, text=True, cwd='.')

    success = judge_response(result.stdout, "Created Python calculator with add and subtract functions")
    cleanup_generated_files()
    assert success

def test_unit_tests_creation():
    """Test creating unit tests"""
    cleanup_generated_files()

    result = subprocess.run(['python', 'main.py'],
                          input='Create unit tests for calculator\n',
                          capture_output=True, text=True, cwd='.')

    success = judge_response(result.stdout, "Created Python unit tests that can be run with pytest")
    cleanup_generated_files()
    assert success