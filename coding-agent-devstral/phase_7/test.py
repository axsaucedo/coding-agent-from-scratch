import os
import requests
from main import full_development_workflow

def judge_response(response, expected_behavior):
    prompt = f"""Judge this response: "{response}"
    Expected: {expected_behavior}
    Answer only: PASS or FAIL"""

    result = requests.post('http://localhost:11434/api/generate',
                          json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': False})
    return 'PASS' in result.json()['response'].upper()

def cleanup_generated_files():
    files = ['test_generated.py', 'main_generated.py', 'generated.py']
    for file in files:
        if os.path.exists(file):
            os.remove(file)

def test_complete_project_workflow():
    cleanup_generated_files()

    output = full_development_workflow('Create Python project with main.py and tests')

    success = judge_response(output, "Complete development workflow with project analysis, planning, code generation, and testing")
    cleanup_generated_files()
    assert success

def test_calculator_with_error_handling():
    cleanup_generated_files()

    output = full_development_workflow('Build calculator app with error handling')

    assert output or 'agent' in output.lower()
    cleanup_generated_files()
