import os
from main import agent_with_tools, read_python_file, list_python_files

def test_read_file_tool():
    with open('test_file.py', 'w') as f:
        f.write('print("test")\n')

    response = agent_with_tools("read the file test_file.py")

    assert 'print' in response.lower() and 'test' in response.lower()

    os.remove('test_file.py')

def test_list_files_tool():
    with open('example1.py', 'w') as f:
        f.write('x = 1\n')
    with open('example2.py', 'w') as f:
        f.write('y = 2\n')

    response = agent_with_tools("list all python files")

    assert '.py' in response.lower()

    os.remove('example1.py')
    os.remove('example2.py')
