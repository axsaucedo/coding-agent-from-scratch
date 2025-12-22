from phase_5.main import generate_code

def test_code_creator_with_functions():
    """Test that code_creator_agent creates, executes, and validates functions."""
    # Call generate_code directly to get the function definition
    response = generate_code("A function named 'add_numbers' that takes two parameters and returns their sum")
    assert response is not None
    assert len(response) > 0

    # Extract the function definition from the generated code
    # The response might include markdown or the if __name__ block, so extract just the function
    lines = response.split('\n')
    func_lines = []
    in_function = False

    for line in lines:
        if 'def add_numbers' in line:
            in_function = True

        if in_function:
            # Stop at if __name__
            if line.strip().startswith('if __name__'):
                break
            func_lines.append(line)

    code = '\n'.join(func_lines).strip()

    # Execute the code to define the function
    namespace = {}
    exec(code, namespace)

    # Verify the function exists
    assert 'add_numbers' in namespace, f"Function 'add_numbers' not found. Extracted code was:\n{code}\n\nNamespace: {list(namespace.keys())}"

    # Get the function
    add_numbers = namespace['add_numbers']

    # Test the function with multiple inputs
    result1 = add_numbers(2, 3)
    assert result1 == 5, f"Expected add_numbers(2, 3) to return 5, got {result1}"

    result2 = add_numbers(10, 20)
    assert result2 == 30, f"Expected add_numbers(10, 20) to return 30, got {result2}"

    result3 = add_numbers(-5, 10)
    assert result3 == 5, f"Expected add_numbers(-5, 10) to return 5, got {result3}"

