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

if __name__ == "__main__":
    print(chat(input("Ask: ")))