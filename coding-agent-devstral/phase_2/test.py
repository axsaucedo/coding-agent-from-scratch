import os
from phase_2.main import agent_with_tools


def test_read_python_file_reads_content():
    with open('test_read.py', 'w') as f:
        f.write('print("hello world")\n')

    content = agent_with_tools('read the file test_read.py and return the contents')
    assert 'print' in content
    assert 'hello world' in content

    os.remove('test_read.py')

def test_list_python_files_finds_files():
    """Test that list_python_files finds Python files."""
    with open('test_list1.py', 'w') as f:
        f.write('x = 1')
    with open('test_list2.py', 'w') as f:
        f.write('y = 2')

    files = agent_with_tools("list all the python files in this directory")
    assert 'test_list1.py' in files
    assert 'test_list2.py' in files

    os.remove('test_list1.py')
    os.remove('test_list2.py')
