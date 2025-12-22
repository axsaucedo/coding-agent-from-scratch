import os
from phase_6.main import code_testing_agent
from phase_4.test import judge_response

def test_code_testing_detects_runtime_errors():
    """Test that code_testing_agent detects runtime errors."""
    with open('test_error.py', 'w') as f:
        f.write('x = 1 / 0')  # Division by zero

    prompt = "Run test_error.py and tell me what happens"
    response = code_testing_agent(prompt)
    assert judge_response(response, "expect error divsion by zero")

    os.remove('test_error.py')
