import subprocess
import requests
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

def test_calculator_app_plan():
    """Test planning for calculator app development"""
    result = subprocess.run([PYTHON_BIN, 'main.py'],
                          input='Create Python calculator app\n',
                          capture_output=True, text=True, cwd='4-phase-planning-agent')
    assert judge_response(result.stdout, "Contains logical development steps for building a calculator application")

def test_testing_strategy_plan():
    """Test planning for adding tests"""
    result = subprocess.run([PYTHON_BIN, 'main.py'],
                          input='Add tests to existing code\n',
                          capture_output=True, text=True, cwd='4-phase-planning-agent')
    assert judge_response(result.stdout, "Contains testing strategy with step-by-step approach")

def test_debugging_plan():
    """Test planning for debugging approach"""
    result = subprocess.run([PYTHON_BIN, 'main.py'],
                          input='Debug Python error in my code\n',
                          capture_output=True, text=True, cwd='4-phase-planning-agent')
    assert judge_response(result.stdout, "Contains systematic debugging approach with logical steps")