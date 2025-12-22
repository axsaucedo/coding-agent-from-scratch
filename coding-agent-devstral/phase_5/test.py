import os
from main import code_creator_agent

def cleanup_generated_files():
    files_to_remove = ['hello.py', 'calculator.py', 'test_calculator.py']
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)

def test_hello_world_creation():
    cleanup_generated_files()

    response = code_creator_agent("Create hello world program")

    if os.path.exists('hello.py'):
        os.remove('hello.py')
        assert True
    else:
        cleanup_generated_files()
        assert False, "hello.py was not created"

def test_calculator_creation():
    cleanup_generated_files()

    response = code_creator_agent("Create calculator with add and subtract")

    assert 'calculator' in response.lower() or 'code' in response.lower()
    cleanup_generated_files()
