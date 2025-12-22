import requests

from phase_4.main import planning_agent


def judge_response(response, expected_behavior):
    print("[JUDGE - VALIDATING REPSPONSE]")
    prompt = f"""Judge this response: "{response}"
    Expected: {expected_behavior}
    Answer: PASS or FAIL (upper case). Followed by an explanation of why pass or fail."""

    result = requests.post('http://localhost:11434/api/generate',
                          json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': False}).json()['response']
    print(f"[JUDGE] Result: {result}")
    return 'PASS' in result


def test_planning_agent_creates_plan():
    response = planning_agent("Create a step-by-step plan to build a calculator")
    assert judge_response(response, "Validate that the provided response is a step by step plan to develop a calculator.")

def test_planning_agent_detailed_plan():
    response = planning_agent("Plan the development of a file analyzer tool")
    assert judge_response(response, "Validate that the provided response is a step by step plan to develop a file analyzer tool.")
