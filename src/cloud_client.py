# src/cloud_client.py
import streamlit as st
from groq import Groq

class CloudLLMClient:
    def __init__(self, model="llama3.2"):
        """Initialize cloud LLM client using Groq API"""
        try:
            self.client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        except:
            st.error("Please configure GROQ_API_KEY in Streamlit secrets")
            st.stop()
        
        # Map local model names to Groq models
        self.model_map = {
            "llama3.2": "llama-3.2-90b-text-preview",
            "llama3": "llama3-70b-8192", 
            "llama2": "llama2-70b-4096",
            "gemma": "gemma-7b-it",
            "mixtral": "mixtral-8x7b-32768",
            "qwen": "mixtral-8x7b-32768"  # Use mixtral as alternative
        }
        
        # Get the Groq model name, default to mixtral if not found
        self.model = self.model_map.get(model, "mixtral-8x7b-32768")
    
    def chat(self, prompt):
        """Send chat request to Groq API"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            st.error(f"Error calling Groq API: {str(e)}")
            return "I'm having trouble connecting to my wine knowledge base. Please try again!"