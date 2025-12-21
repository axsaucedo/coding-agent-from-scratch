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

def setup_test_file():
    """Create a test Python file"""
    filepath = '2-phase-tool-calling/hello.py'
    with open(filepath, 'w') as f:
        f.write('print("Hello, World!")\n')

def cleanup_test_file():
    """Remove test file"""
    filepath = '2-phase-tool-calling/hello.py'
    if os.path.exists(filepath):
        os.remove(filepath)

def test_read_file():
    """Test file reading functionality"""
    setup_test_file()
    try:
        result = subprocess.run([PYTHON_BIN, 'main.py'],
                              input='read file hello.py\n',
                              capture_output=True, text=True, cwd='2-phase-tool-calling')
        # Check that the file content was printed
        assert "print" in result.stdout.lower() and "Hello" in result.stdout
    finally:
        cleanup_test_file()

def test_list_python_files():
    """Test listing Python files"""
    result = subprocess.run([PYTHON_BIN, 'main.py'],
                          input='list python files\n',
                          capture_output=True, text=True, cwd='2-phase-tool-calling')
    assert judge_response(result.stdout, "Lists .py files found in directory")

def test_file_content_query():
    """Test asking about file content"""
    setup_test_file()
    try:
        result = subprocess.run([PYTHON_BIN, 'main.py'],
                              input="what's in hello.py\n",
                              capture_output=True, text=True, cwd='2-phase-tool-calling')
        assert judge_response(result.stdout, "Shows content description of hello.py")
    finally:
        cleanup_test_file()