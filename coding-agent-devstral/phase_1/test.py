import requests
from main import chat_stream

def judge_response(response, expected_behavior):
    prompt = f"""Judge this response: "{response}"
    Expected: {expected_behavior}
    Answer only: PASS or FAIL"""

    result = requests.post('http://localhost:11434/api/generate',
                          json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': False})
    return 'PASS' in result.json()['response'].upper()

def test_hello_world():
    response = chat_stream("Create hello world in Python")
    assert judge_response(response, "Contains Python print statement with hello world")

def test_function_creation():
    response = chat_stream("Write function to add two numbers")
    assert judge_response(response, "Contains function definition that adds two numbers")
