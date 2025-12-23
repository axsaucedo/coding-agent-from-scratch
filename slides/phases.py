import marimo

__generated_with = "0.18.4"
app = marimo.App()


@app.cell
def _():
    import httpx
    import json
    import requests
    import glob
    import re
    import ast
    import subprocess
    import os

    print("✓ Imports loaded")
    return ast, glob, httpx, json, os, re, requests, subprocess


@app.cell
def _(httpx):
    try:
        _response = httpx.get('http://localhost:11434/api/tags', timeout=2)
        if _response.status_code == 200:
            print('✓ Ollama running on localhost:11434')
    except Exception as e:
        print(f'✗ Ollama not available: {e}')
    return


@app.cell
def _(httpx, json, requests):
    print('\n' + '=' * 60)
    print('PHASE 1: Basic LLM Chat')
    print('=' * 60)

    def chat(prompt, system_prompt=''):
        _response, full_prompt = ('', f'System prompt: {system_prompt}\nUser: {prompt}')
        _response = requests.post('http://localhost:11434/api/generate', json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': False})
        val = _response.json()['response']
        return val

    def chat_stream(prompt, system_prompt=''):
        _response, full_prompt = ('', f'System prompt: {system_prompt}\nUser: {prompt}')
        with httpx.stream('POST', 'http://localhost:11434/api/generate', json={'model': 'devstral-small-2', 'prompt': full_prompt, 'stream': True}, timeout=None) as r:
            for line in r.iter_lines():
                if line and (token := json.loads(line).get('response', '')):
                    print(token, end='', flush=True)
                    _response += token
        print()
        return _response
    print("Running: What is 2+2? (should answer '4')")
    _response = chat_stream('What is 2+2? Respond with a number only e.g. (1,2,3,4,etc).')
    # Execute Phase 1 example
    print(f'Result: {_response.strip()}')
    return (chat_stream,)


@app.cell
def _(ast, chat_stream, glob, os, re):
    print('\n' + '=' * 60)
    print('PHASE 2: Tool-Enabled Agent')
    print('=' * 60)

    def read_python_file(filepath):
        """Read and return the contents of a Python file."""
        with open(filepath, 'r') as _f:
            return _f.read()

    def list_python_files():
        """List all Python files in the current directory."""
        return glob.glob('*.py')
    TOOLS_PHASE2 = [read_python_file, list_python_files]

    def agent_with_tools(user_input, tools=TOOLS_PHASE2, system_prompt=''):
        tool_map = {fn.__name__: fn for fn in tools}
        tools_desc = '\n'.join([f'- {fn.__name__}: {fn.__doc__}' for fn in tools])
        system = f'You are a helpful assistant with access to tools.\n\nAvailable tools:\n{tools_desc}\n\nWhen you need to use a tool, call it using TOOL:<tool_name>(params).\n\nExamples:\n- TOOL:read_python_file("hello.py")\n- TOOL:list_python_files()\n\nWhen done using tools or if no tools required, respond with TOOL:NONE.\n\nAfter using a tool, the output will be provided as context.'
        prompt = f'{system}\n\nUser: {user_input}'
        for iteration in range(3):
            _response = chat_stream(prompt, system_prompt=system_prompt)
            tool_match = re.search('TOOL:(\\w+)\\((.*?)\\)', _response, re.DOTALL)
            if not tool_match:
                return _response
            tool_name = tool_match.group(1)
            params_str = tool_match.group(2).strip()
            if tool_name == 'NONE':
                return _response
            if tool_name in tool_map:
                if params_str:
                    try:
                        params = ast.literal_eval(f'[{params_str}]')
                    except (SyntaxError, ValueError):
                        params = [params_str]
                else:
                    params = []
                result = tool_map[tool_name](*params)
                prompt = f'{system}\n\nTool executed: {tool_name}({params_str})\nResult:\n{result}\n\nInclude the tool result in your response. Provide the information the user requested:'
            else:
                return _response
        return _response
    print('Creating test files...')
    with open('test_read.py', 'w') as _f:
        _f.write('print("hello world")\n')
    print('Agent task: read the file test_read.py and return the contents')
    content = agent_with_tools('read the file test_read.py and return the contents')
    assert 'print' in content and 'hello world' in content
    print(f'✓ Successfully read file and found: print, hello world')
    # Execute Phase 2 example
    os.remove('test_read.py')
    return agent_with_tools, list_python_files, read_python_file


@app.cell
def _(agent_with_tools, glob, list_python_files, os, read_python_file):
    print('\n' + '=' * 60)
    print('PHASE 3: Context-Aware Agent')
    print('=' * 60)

    def analyze_project():
        """Analyze Python project structure and summarize contents."""
        files = glob.glob('**/*.py', recursive=True)
        context = 'Project structure:\n'
        for _f in files[:5]:
            with open(_f, 'r') as file:
                content = file.read()[:150]
                context += f'\n{_f}:\n{content}...\n'
        return context

    def find_functions():
        """Find all function definitions in Python files."""
        files = glob.glob('**/*.py', recursive=True)
        functions = []
        for _f in files:
            with open(_f, 'r') as file:
                lines = file.readlines()
                for line_num, line in enumerate(lines, 1):
                    if line.strip().startswith('def '):
                        func_name = line.strip().split('(')[0].replace('def ', '')
                        functions.append(f'{_f}:{line_num} - {func_name}')
        return functions
    TOOLS_PHASE3 = [read_python_file, list_python_files, analyze_project, find_functions]

    def context_aware_agent(user_input):
        return agent_with_tools(user_input, tools=TOOLS_PHASE3)
    print('Creating test file with functions...')
    with open('funcs.py', 'w') as _f:
    # Execute Phase 3 example
        _f.write('def hello():\n    pass\ndef world():\n    pass\n')
    print('Agent task: Find all the functions in this project')
    _response = context_aware_agent('Find all the functions in this project')
    assert 'hello' in _response or 'world' in _response or 'function' in _response.lower()
    print(f'✓ Successfully found functions')
    os.remove('funcs.py')
    return analyze_project, find_functions


@app.cell
def _(
    agent_with_tools,
    analyze_project,
    chat_stream,
    find_functions,
    list_python_files,
    read_python_file,
):
    print('\n' + '=' * 60)
    print('PHASE 4: Planning Agent')
    print('=' * 60)

    def create_plan():
        """Create a detailed step by step plan for simple and complex applications."""
        guiding_prompt = f'Create a detailed step-by-step plan for the text provided by the user.\n\nFormat your response as numbered steps:\n1. Step one\n2. Step two\netc.\n\nBe specific and actionable. Keep it to only a few simple steps and keep it simple and basic unless specified otherwise.\n\nOnly reply with the plan and do not reply with anything else.'
        return guiding_prompt
    TOOLS_PHASE4 = [read_python_file, list_python_files, analyze_project, find_functions]

    def planning_agent(user_input):
        return agent_with_tools(user_input, tools=TOOLS_PHASE4)

    def judge_response(response, expected_behavior):
        print(f'[JUDGE] Validating: {expected_behavior[:50]}...')
        prompt = f'You are a Judge LLM which evaluates the EXPECTED_TASK of a large language model against the ANSWER_PROVIDED as outlined below.\n\nAnswer specifically with PASS or FAIL (upper case). Followed by an explanation of why pass or fail.\n\nEXPECTED_TASK:\n    """{expected_behavior}"""\n\nANSWER_PROVIDED:\n    """{response}"""\n'
        result = chat_stream(prompt)
        print(f'[JUDGE] Result: {result[:100]}...')
        return 'PASS' in result
    print('Agent task: Plan the development of a file analyzer tool in python')
    _response = planning_agent('Plan the development of a file analyzer tool in python')
    _judge_result = judge_response(_response, 'Validate that the provided response is a step by step plan to develop a file analyzer tool.')
    # Execute Phase 4 example with judge
    print(f'✓ Plan validated: {('PASS' if _judge_result else 'FAIL')}')
    return create_plan, judge_response


@app.cell
def _(chat_stream):
    print('\n' + '=' * 60)
    print('PHASE 5: Code Generation')
    print('=' * 60)

    def generate_code(description):
        """Generate Python code from a description."""
        code_prompt = f"Write Python code for: {description}\n\nRequirements:\n- Complete, working Python code\n- Include proper function definitions\n- Add basic error handling where appropriate\n- Include a main section if it's a script\n- Make it simple and functional\n\nOnly return the Python code, nothing else (e.g. no text, explanations, etc)."
        code = chat_stream(code_prompt)
        if '```python' in code:
            code = code.split('```python')[1].split('```')[0].strip()
        elif '```' in code:
            code = code.split('```')[1].split('```')[0].strip()
        return code

    def create_python_file(description, filename='generated.py'):
        """Create and save a Python file from description."""
        code = generate_code(description)
        with open(filename, 'w') as _f:
            _f.write(code)
        return filename
    print('Generating code for: add_numbers function')
    _response = generate_code("A function named 'add_numbers' that takes two parameters and returns their sum")
    lines = _response.split('\n')
    func_lines = []
    in_function = False
    for line in lines:
        if 'def add_numbers' in line:
            in_function = True
        if in_function:
            if line.strip().startswith('if __name__'):
                break
            func_lines.append(line)
    code = '\n'.join(func_lines).strip()
    # Execute Phase 5 example
    namespace = {}
    exec(code, namespace)
    add_numbers = namespace['add_numbers']
    # Extract and execute function
    result1 = add_numbers(2, 3)
    result2 = add_numbers(10, 20)
    result3 = add_numbers(-5, 10)
    print(f'✓ Generated and tested add_numbers():')
    print(f'  add_numbers(2, 3) = {result1} (expected 5)')
    print(f'  add_numbers(10, 20) = {result2} (expected 30)')
    print(f'  add_numbers(-5, 10) = {result3} (expected 5)')
    assert result1 == 5 and result2 == 30 and (result3 == 5)
    # Test the function
    print(f'✓ All tests passed!')
    return create_python_file, generate_code


@app.cell
def _(
    agent_with_tools,
    analyze_project,
    create_plan,
    create_python_file,
    find_functions,
    generate_code,
    judge_response,
    list_python_files,
    os,
    read_python_file,
    subprocess,
):
    print('\n' + '=' * 60)
    print('PHASE 6: Testing Agent (Full Development Cycle)')
    print('=' * 60)

    def run_python_file(filepath):
        """Run a Python file and check if it executes without errors."""
        if not os.path.exists(filepath):
            return f'File {filepath} not found'
        with open(filepath, 'r') as _f:
            code = _f.read()
        try:
            compile(code, filepath, 'exec')
        except SyntaxError as e:
            return f'Syntax error in {filepath}: {e}'
        try:
            result = subprocess.run(['python', filepath], capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                return f'✓ {filepath} runs successfully\nOutput:\n{result.stdout}'
            else:
                return f'✗ {filepath} failed:\n{result.stderr}'
        except subprocess.TimeoutExpired:
            return f'✗ {filepath} timed out (>10 seconds)'
        except Exception as e:
            return f'✗ Error running {filepath}: {e}'
    TOOLS_PHASE6 = [read_python_file, list_python_files, analyze_project, find_functions, create_plan, generate_code, create_python_file, run_python_file]

    def code_testing_agent(user_input):
        return agent_with_tools(user_input, tools=TOOLS_PHASE6)
    print('Creating file with runtime error (division by zero)...')
    with open('test_error.py', 'w') as _f:
        _f.write('x = 1 / 0')
    print('Agent task: Run test_error.py and tell me what happens')
    _response = code_testing_agent('Run test_error.py and tell me what happens')
    _judge_result = judge_response(_response, 'expect error division by zero')
    print(f'✓ Error detection validated: {('PASS' if _judge_result else 'FAIL')}')
    # Execute Phase 6 example - detect runtime errors
    os.remove('test_error.py')
    return


@app.cell
def _():
    print("\n" + "="*60)
    print("COMPLETE: All 6 Phases Executed Successfully")
    print("="*60)
    print("""
    Phase 1: ✓ Basic LLM Chat
    Phase 2: ✓ Tool-Enabled Agent (file operations)
    Phase 3: ✓ Context-Aware Agent (project analysis)
    Phase 4: ✓ Planning Agent (with validation)
    Phase 5: ✓ Code Generation (with execution)
    Phase 6: ✓ Testing Agent (error detection)

    Key patterns learned:
    - Tool pattern: Functions as auto-discovered tools
    - Agent loop: LLM → Parse → Execute → Feedback
    - Progressive enhancement: Each phase builds on previous
    """)
    return


if __name__ == "__main__":
    app.run()
