import os
from phase_3.main import context_aware_agent

def test_analyze_project_with_agent():
    with open('test_module.py', 'w') as f:
        f.write('x = 1\ny = 2\n')

    response = context_aware_agent('Analyze the project structure')
    assert 'test_module' in response or 'Project' in response

    os.remove('test_module.py')

def test_find_functions_with_agent():
    with open('funcs.py', 'w') as f:
        f.write('def hello():\n    pass\ndef world():\n    pass\n')

    response = context_aware_agent('Find all the functions in this project')
    assert 'hello' in response or 'world' in response or 'function' in response.lower()

    os.remove('funcs.py')
