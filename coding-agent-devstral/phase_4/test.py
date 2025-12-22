from phase_4.main import planning_agent

def test_planning_agent_creates_plan():
    response = planning_agent("Create a step-by-step plan to build a calculator")
    assert any(keyword in response.lower() for keyword in ['step', 'plan', 'build', 'calculator', 'approach'])

def test_planning_agent_detailed_plan():
    response = planning_agent("Plan the development of a file analyzer tool")
    assert any(keyword in response.lower() for keyword in ['step', 'plan', 'approach', 'first', 'create'])
