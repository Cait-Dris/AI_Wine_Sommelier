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
        
        # Use ONLY currently active Groq models
        self.model_map = {
            "llama3.2": "llama3-8b-8192",     # Use llama3 8B
            "llama3": "llama3-70b-8192",      # Llama 3 70B  
            "llama2": "llama2-70b-4096",      # Llama 2 70B
            "gemma": "gemma-7b-it",           # Gemma 7B
            "mixtral": "mixtral-8x7b-32768",  # Mixtral
            "qwen": "llama3-8b-8192"          # Default to llama3
        }
        
        self.model = self.model_map.get(model, "llama3-8b-8192")
    
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
            if "model" in str(e).lower() or "decommissioned" in str(e).lower():
                # Try fallback model
                try:
                    response = self.client.chat.completions.create(
                        model="llama3-8b-8192",  # Most stable model
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=1000
                    )
                    return response.choices[0].message.content
                except:
                    st.error(f"Error calling Groq API: {str(e)}")
                    return "I'm having trouble connecting. Please try again!"
            else:
                st.error(f"Error calling Groq API: {str(e)}")
                return "I'm having trouble connecting to my wine knowledge base. Please try again!"