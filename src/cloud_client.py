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
        
        # Only use WORKING Groq models
        self.model_map = {
            "llama3.2": "llama-3.1-8b-instant",   
            "llama3": "gemma2-9b-it",             
            "llama2": "llama-3.1-8b-instant",     
            "gemma": "gemma2-9b-it",              
            "mixtral": "gemma2-9b-it",            
            "qwen": "llama-3.1-8b-instant"        
        }
        
        self.model = self.model_map.get(model, "llama-3.1-8b-instant")
    
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