import httpx
import json

def chat_stream(prompt):
    full = ""
    with httpx.stream("POST", "http://localhost:11434/api/generate",
                     json={'model': 'devstral-small-2', 'prompt': prompt, 'stream': True}) as r:
        for line in r.iter_lines():
            if line and (token := json.loads(line).get('response', '')):
                print(token, end='', flush=True)
                full += token
    return full

def create_plan(task):
    prompt = f"""Create a detailed step-by-step plan for: {task}

Format your response as numbered steps:
1. Step one
2. Step two
etc.

Be specific and actionable."""

    response = chat_stream(prompt)
    steps = []
    for line in response.split('\n'):
        line = line.strip()
        if line and (line[0].isdigit() or line.startswith('-')):
            steps.append(line)
    return steps

def planning_agent(user_input):
    user_input_lower = user_input.lower()

    if any(keyword in user_input_lower for keyword in [
        "create", "build", "develop", "implement", "add", "make"
    ]):
        plan = create_plan(user_input)
        if plan:
            result = f"Plan for: {user_input}\n\n"
            result += "\n".join(plan)
            return result
        else:
            return chat_stream(f"Create a plan for: {user_input}")

    elif "debug" in user_input_lower or "fix" in user_input_lower:
        debug_plan = create_plan(f"Debug and fix: {user_input}")
        if debug_plan:
            result = f"Debugging plan for: {user_input}\n\n"
            result += "\n".join(debug_plan)
            return result
        else:
            return chat_stream(f"Create a debugging plan for: {user_input}")

    else:
        return chat_stream(user_input)

if __name__ == "__main__":
    user_request = input("Describe your task: ")
    print("\n" + planning_agent(user_request))