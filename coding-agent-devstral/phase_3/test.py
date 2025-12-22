import requests
from main import context_aware_agent

def judge_response(response, expected_behavior):
    prompt = f"""Judge this response: "{response}"
    Expected: {expected_behavior}
    Answer only: PASS or FAIL"""

    result = requests.post('http://localhost:11434/api/generate',
                          json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': False})
    return 'PASS' in result.json()['response'].upper()

def test_analyze_project():
    response = context_aware_agent("analyze this python project")
    assert judge_response(response, "identifies main components and project structure")

def test_list_functions():
    response = context_aware_agent("find all functions")
    assert "def" in response or "functions" in response.lower()
