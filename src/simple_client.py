# src/simple_client.py
import os
import streamlit as st

class SimpleLLMClient:
    def __init__(self, model="llama3.2"):
        self.model = model
        self.is_cloud = os.getenv("STREAMLIT_CLOUD") == "true"
        
        if self.is_cloud:
            try:
                from groq import Groq
                self.client = Groq(api_key=st.secrets["GROQ_API_KEY"])
                
                # Only use WORKING Groq models (tested and confirmed)
                self.model_map = {
                    "llama3.2": "llama-3.1-8b-instant",   # Fast model
                    "llama3": "gemma2-9b-it",             # Alternative model
                    "llama2": "llama-3.1-8b-instant",     # Default to working model
                    "gemma": "gemma2-9b-it",              # Gemma 2
                    "mixtral": "gemma2-9b-it",            # Use Gemma as fallback
                    "qwen": "llama-3.1-8b-instant"        # Default to Llama
                }
                self.groq_model = self.model_map.get(model, "llama-3.1-8b-instant")
                st.sidebar.info(f"Using Groq model: {self.groq_model}")
            except Exception as e:
                st.error(f"Failed to initialize Groq: {str(e)}")
                st.stop()
        else:
            import ollama
            self.ollama = ollama
    
    def chat(self, prompt):
        if self.is_cloud:
            try:
                # Use Groq API with working model
                response = self.client.chat.completions.create(
                    model=self.groq_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content
            except Exception as e:
                st.error(f"Groq API error: {str(e)}")
                return "Sorry, I'm having trouble connecting. Please try again."
        else:
            # Use local Ollama
            response = self.ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']