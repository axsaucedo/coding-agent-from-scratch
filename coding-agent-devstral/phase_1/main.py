import httpx, json, requests


def chat(prompt, system_prompt=""):
    response, full_prompt = "", f"System prompt: {system_prompt}\nUser: {prompt}"
    print(f"Received: {full_prompt}")
    response = requests.post('http://localhost:11434/api/generate',
                           json={
                               'model': 'devstral-small-2',
                               'prompt': prompt,
                               'stream': False
                           })
    val = response.json()['response']
    print(f"Result: {val}")
    return val


def chat_stream(prompt, system_prompt=""):
    response, full_prompt = "", f"System prompt: {system_prompt}\nUser: {prompt}"
    print(f"Received: {full_prompt}")
    with httpx.stream("POST", "http://localhost:11434/api/generate",
                     json={'model': 'devstral-small-2', 'prompt': full_prompt, 'stream': True},
                     timeout=None) as r:
        for line in r.iter_lines():
            if line and (token := json.loads(line).get('response', '')):
                print(token, end='', flush=True)
                response += token
    print()
    return response

if __name__ == "__main__":
    print(chat(input("Ask (Sync): ")))
    print(chat_stream(input("Ask (Stream): ")))
