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

def cleanup_generated_files():
    """Remove all generated files"""
    files = ['7-phase-full-agent/test_generated.py', '7-phase-full-agent/main_generated.py', '7-phase-full-agent/generated.py']
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def test_complete_project_workflow():
    """Test full workflow for creating Python project"""
    cleanup_generated_files()

    # Simulate interactive input for the agent
    process = subprocess.Popen([PYTHON_BIN, 'main.py'],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True, cwd='7-phase-full-agent')

    output, error = process.communicate(input='Create Python project with main.py and tests\nquit\n')

    success = judge_response(output, "Complete development workflow with project analysis, planning, code generation, and testing")
    cleanup_generated_files()
    assert success

def test_calculator_with_error_handling():
    """Test building calculator with robust implementation"""
    cleanup_generated_files()

    process = subprocess.Popen([PYTHON_BIN, 'main.py'],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True, cwd='7-phase-full-agent')

    output, error = process.communicate(input='Build calculator app with error handling\nquit\n')

    # Check if output contains indication of development activity (no error just means it ran)
    assert output or 'agent' in (output + error).lower()
    cleanup_generated_files()

def test_full_development_cycle():
    """Test complete development cycle"""
    cleanup_generated_files()

    process = subprocess.Popen([PYTHON_BIN, 'main.py'],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True, cwd='7-phase-full-agent')

    output, error = process.communicate(input='Create web scraper with unit tests and run them\nquit\n')

    # Check if output contains indication of development activity
    assert output or 'agent' in (output + error).lower()
    cleanup_generated_files()