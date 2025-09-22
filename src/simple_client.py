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
                # Map Ollama models to Groq models
                self.model_map = {
                    "llama3.2": "llama-3.2-90b-text-preview",
                    "llama3": "llama3-70b-8192",
                    "gemma": "gemma-7b-it",
                    "qwen": "mixtral-8x7b-32768"  # Closest alternative
                }
                self.groq_model = self.model_map.get(model, "mixtral-8x7b-32768")
            except:
                st.error("Please configure GROQ_API_KEY in Streamlit secrets")
                st.stop()
        else:
            import ollama
            self.ollama = ollama
    
    def chat(self, prompt):
        if self.is_cloud:
            # Use Groq API
            response = self.client.chat.completions.create(
                model=self.groq_model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        else:
            # Use local Ollama
            response = self.ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']
