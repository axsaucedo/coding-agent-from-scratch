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

def setup_test_file():
    """Create a test Python file"""
    with open('hello.py', 'w') as f:
        f.write('print("Hello, World!")\n')

def cleanup_test_file():
    """Remove test file"""
    if os.path.exists('hello.py'):
        os.remove('hello.py')

def test_read_file():
    """Test file reading functionality"""
    setup_test_file()
    try:
        result = subprocess.run(['python', 'main.py'],
                              input='read file hello.py\n',
                              capture_output=True, text=True, cwd='.')
        assert judge_response(result.stdout, "Shows content of hello.py file with print statement")
    finally:
        cleanup_test_file()

def test_list_python_files():
    """Test listing Python files"""
    result = subprocess.run(['python', 'main.py'],
                          input='list python files\n',
                          capture_output=True, text=True, cwd='.')
    assert judge_response(result.stdout, "Lists .py files found in directory")

def test_file_content_query():
    """Test asking about file content"""
    setup_test_file()
    try:
        result = subprocess.run(['python', 'main.py'],
                              input="what's in hello.py\n",
                              capture_output=True, text=True, cwd='.')
        assert judge_response(result.stdout, "Shows content description of hello.py")
    finally:
        cleanup_test_file()