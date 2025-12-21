import subprocess
import requests
import sys
import os

# Get the Python executable from the current environment
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

def test_hello_world():
    """Test basic hello world generation"""
    result = subprocess.run([PYTHON_BIN, 'main.py'],
                          input='Create hello world in Python\n',
                          capture_output=True, text=True, cwd='1-phase-basic-llm')
    assert judge_response(result.stdout, "Contains Python print statement with hello world")

def test_function_creation():
    """Test function definition generation"""
    result = subprocess.run([PYTHON_BIN, 'main.py'],
                          input='Write function to add two numbers\n',
                          capture_output=True, text=True, cwd='1-phase-basic-llm')
    assert judge_response(result.stdout, "Contains function definition that adds two numbers")

def test_python_explanation():
    """Test coherent explanation"""
    result = subprocess.run([PYTHON_BIN, 'main.py'],
                          input='Explain what Python is\n',
                          capture_output=True, text=True, cwd='1-phase-basic-llm')
    assert judge_response(result.stdout, "Coherent explanation about Python programming language")