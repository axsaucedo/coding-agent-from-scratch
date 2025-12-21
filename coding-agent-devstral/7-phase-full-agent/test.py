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
    """Remove all generated files"""
    files = ['test_generated.py', 'main_generated.py', 'generated.py']
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def test_complete_project_workflow():
    """Test full workflow for creating Python project"""
    cleanup_generated_files()

    # Simulate interactive input for the agent
    process = subprocess.Popen(['python', 'main.py'],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True, cwd='.')

    output, error = process.communicate(input='Create Python project with main.py and tests\nquit\n')

    success = judge_response(output, "Complete development workflow with project analysis, planning, code generation, and testing")
    cleanup_generated_files()
    assert success

def test_calculator_with_error_handling():
    """Test building calculator with robust implementation"""
    cleanup_generated_files()

    process = subprocess.Popen(['python', 'main.py'],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True, cwd='.')

    output, error = process.communicate(input='Build calculator app with error handling\nquit\n')

    success = judge_response(output, "Robust calculator implementation with error handling and validation")
    cleanup_generated_files()
    assert success

def test_full_development_cycle():
    """Test complete development cycle"""
    cleanup_generated_files()

    process = subprocess.Popen(['python', 'main.py'],
                              stdin=subprocess.PIPE,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              text=True, cwd='.')

    output, error = process.communicate(input='Create web scraper with unit tests and run them\nquit\n')

    success = judge_response(output, "Complete development cycle from planning to testing with working code")
    cleanup_generated_files()
    assert success