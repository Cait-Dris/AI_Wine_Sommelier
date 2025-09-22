import ollama

# List available models
models = ollama.list()
print("Available models:")
for model in models['models']:
    print(f"  - {model['name']}")

# Test a simple prompt
response = ollama.chat(
    model='llama3.2',
    messages=[{'role': 'user', 'content': 'Say hello!'}]
)
print(f"\nResponse: {response['message']['content']}")
