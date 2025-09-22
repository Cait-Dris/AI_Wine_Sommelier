"""Simple working version without complex validation."""
import ollama

class SimpleLLMClient:
    def __init__(self, model="llama3.2"):
        self.model = model
    
    def chat(self, prompt):
        response = ollama.chat(
            model=self.model,
            messages=[{'role': 'user', 'content': prompt}]
        )
        return response['message']['content']

# Test it immediately
if __name__ == "__main__":
    client = SimpleLLMClient()
    print(client.chat("Say hello"))
