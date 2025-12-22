import os
import requests
from main import testing_agent

def judge_response(response, expected_behavior):
    prompt = f"""Judge this response: "{response}"
    Expected: {expected_behavior}
    Answer only: PASS or FAIL"""

    result = requests.post('http://localhost:11434/api/generate',
                          json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': False})
    return 'PASS' in result.json()['response'].upper()

def cleanup_test_files():
    files_to_remove = ['hello_test.py', 'calc_test.py', 'generated_test.py']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)

def test_create_and_validate():
    cleanup_test_files()

    response = testing_agent("Create hello world and test it")

    success = judge_response(response, "Created working Python code and validated it runs successfully")
    cleanup_test_files()
    assert success

def test_function_with_tests():
    cleanup_test_files()

    response = testing_agent("Create function with unit tests and run them")

    success = judge_response(response, "Created Python function with tests and verified they work")
    cleanup_test_files()
    assert success
