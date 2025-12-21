import requests

def chat(prompt):
    """Send prompt to ollama, return response"""
    try:
        response = requests.post('http://localhost:11434/api/generate',
                               json={
                                   'model': 'devstral-2-small',
                                   'prompt': prompt,
                                   'stream': False
                               })
        return response.json()['response']
    except Exception as e:
        return f"Error: {e}"

def create_plan(task):
    """Create step-by-step plan for a task"""
    prompt = f"""Create a detailed step-by-step plan for: {task}

Format your response as numbered steps:
1. Step one
2. Step two
etc.

Be specific and actionable."""

    response = chat(prompt)
    # Parse response into list of steps
    steps = []
    for line in response.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            steps.append(line)

    return steps

def planning_agent(user_input):
    """Agent that creates plans for development tasks"""
    user_input_lower = user_input.lower()

    if any(keyword in user_input_lower for keyword in [
        "create", "build", "develop", "implement", "add", "make"
    ]):
        # This looks like a task that needs planning
        plan = create_plan(user_input)
        if plan:
            result = f"Plan for: {user_input}\n\n"
            result += "\n".join(plan)
            return result
        else:
            return chat(f"Create a plan for: {user_input}")

    elif "debug" in user_input_lower or "fix" in user_input_lower:
        debug_plan = create_plan(f"Debug and fix: {user_input}")
        if debug_plan:
            result = f"Debugging plan for: {user_input}\n\n"
            result += "\n".join(debug_plan)
            return result
        else:
            return chat(f"Create a debugging plan for: {user_input}")

    else:
        # Regular chat for non-planning requests
        return chat(user_input)

if __name__ == "__main__":
    user_request = input("Describe your task: ")
    print("\n" + planning_agent(user_request))