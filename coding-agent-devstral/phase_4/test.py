import requests

from phase_1.main import chat_stream
from phase_4.main import planning_agent


def judge_response(response, expected_behavior):
    print("[JUDGE - VALIDATING REPSPONSE]")
    prompt = f"""You are a Judge LLM which evaluates the EXPECTED_TASK of a large language model against the ANSWER_PROVIDED as outlined below.

    Answer specifically with PASS or FAIL (upper case). Followed by an explanation of why pass or fail.

    EXPECTED_TASK:
        \"\"\"{expected_behavior}\"\"\"

    ANSWER_PROVIDED: 
        \"\"\"{response}\"\"\"
    """

    result = chat_stream(prompt)
    print(f"[JUDGE] Result: {result}")
    return 'PASS' in result


def test_planning_agent_detailed_plan():
    response = planning_agent("Plan the development of a file analyzer tool in python")
    assert judge_response(response, "Validate that the provided response is a step by step plan to develop a file analyzer tool.")
