import requests, httpx, json

def chat(prompt):
    print(f"Received prompt: {prompt}")
    response = requests.post('http://localhost:11434/api/generate',
                           json={
                               'model': 'devstral-small-2',
                               'prompt': prompt,
                               'stream': False
                           })
    val = response.json()['response']
    print(f"Result: {val}")
    return val


def chat_stream(prompt):
    full = ""
    with httpx.stream("POST", "http://localhost:11434/api/generate",
                           json={
                               'model': 'devstral-small-2',
                               'prompt': prompt,
                               'stream': True
                           }) as r:
        for line in r.iter_lines():
            if line and (token := json.loads(line).get('response', '')):
                print(token, end='', flush=True)
                full += token
    return full

if __name__ == "__main__":
    print(chat(input("Ask: ")))
    print(chat_stream(input("Ask: ")))
