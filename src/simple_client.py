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
                
                # UPDATED model map with currently active Groq models
                self.model_map = {
                    "llama3.2": "llama-3.2-11b-text-preview",  # Updated to active model
                    "llama3": "llama3-70b-8192",
                    "llama2": "llama2-70b-4096", 
                    "gemma": "gemma2-9b-it",  # Updated to gemma2
                    "mixtral": "mixtral-8x7b-32768",
                    "qwen": "llama-3.2-11b-text-preview"  # Use llama as fallback
                }
                self.groq_model = self.model_map.get(model, "llama-3.2-11b-text-preview")
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
                # Use Groq API with updated model
                response = self.client.chat.completions.create(
                    model=self.groq_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7,
                    max_tokens=1000
                )
                return response.choices[0].message.content
            except Exception as e:
                # If model fails, try with a known good model
                if "model" in str(e).lower():
                    st.warning(f"Model {self.groq_model} failed, trying fallback...")
                    response = self.client.chat.completions.create(
                        model="llama-3.2-11b-text-preview",  # Fallback model
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    return response.choices[0].message.content
                else:
                    st.error(f"Groq API error: {str(e)}")
                    return "Sorry, I'm having trouble connecting. Please try again."
        else:
            # Use local Ollama
            response = self.ollama.chat(
                model=self.model,
                messages=[{'role': 'user', 'content': prompt}]
            )
            return response['message']['content']