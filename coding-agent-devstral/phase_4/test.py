import requests
from main import planning_agent

def judge_response(response, expected_behavior):
    prompt = f"""Judge this response: "{response}"
    Expected: {expected_behavior}
    Answer only: PASS or FAIL"""

    result = requests.post('http://localhost:11434/api/generate',
                          json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': False})
    return 'PASS' in result.json()['response'].upper()

def test_calculator_plan():
    response = planning_agent("Create Python calculator app")
    assert judge_response(response, "Contains logical development steps for building a calculator")

def test_testing_plan():
    response = planning_agent("Add tests to existing code")
    assert judge_response(response, "Contains testing strategy with step-by-step approach")
