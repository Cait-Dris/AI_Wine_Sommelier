"""Ollama client wrapper for LLM interactions."""
import ollama

class LLMClient:
    """Wrapper for Ollama API interactions."""
    
    def __init__(self, model: str = "llama3.2"):
        self.model = model
        self._validate_model()
    
    def _validate_model(self):
        """Check if model is available in Ollama."""
        try:
            models = ollama.list()
            # Handle the response structure correctly
            available_models = [m.model for m in models.models]
            # Also check for model:tag format
            model_base = self.model.split(':')[0]
            if not any(model_base in m for m in available_models):
                print(f"Warning: Model {self.model} may not be available")
                print(f"Available models: {available_models}")
        except Exception as e:
            print(f"Warning: Could not validate model: {e}")
    
    def chat(self, prompt: str, temperature: float = 0.7) -> str:
        """Send chat request to LLM."""
        try:
            response = ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}],
                options={'temperature': temperature}
            )
            return response['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"
