# src/cloud_client.py
# src/cloud_client.py
import streamlit as st

class CloudLLMClient:
    def __init__(self, model="llama3.2"):
        """Initialize cloud LLM client using Groq API"""
        try:
            from groq import Groq
            
            # Check if API key exists
            if "GROQ_API_KEY" not in st.secrets:
                st.error("❌ GROQ_API_KEY not found in Streamlit secrets!")
                st.info("Please add your Groq API key in the Streamlit Cloud settings.")
                st.stop()
                
            self.client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            
        except ImportError:
            st.error("❌ Groq library not installed. Please add 'groq' to requirements.txt")
            st.stop()
        except Exception as e:
            st.error(f"❌ Failed to initialize Groq client: {str(e)}")
            st.stop()
        
        # Updated model map with currently available Groq models
        self.model_map = {
            "llama3.2": "llama3-8b-8192",  # Use 8b version which is more stable
            "llama3": "llama3-70b-8192",
            "llama2": "llama2-70b-4096",
            "gemma": "gemma-7b-it",
            "mixtral": "mixtral-8x7b-32768",
            "qwen": "llama3-8b-8192"  # Default to llama3
        }
        
        # Get the Groq model name
        self.model = self.model_map.get(model, "llama3-8b-8192")
        st.sidebar.info(f"Using Groq model: {self.model}")
    
    def chat(self, prompt):
        """Send chat request to Groq API"""
        try:
            # Test with a simple message first
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800,  # Reduced for reliability
                timeout=30
            )
            
            # Extract the response
            if response and response.choices:
                return response.choices[0].message.content
            else:
                return "I couldn't generate a wine recommendation. Please try again."
                
        except Exception as e:
            error_msg = str(e)
            
            # Provide specific error messages
            if "api_key" in error_msg.lower():
                st.error("❌ API Key issue. Please check your Groq API key.")
            elif "model" in error_msg.lower():
                st.error(f"❌ Model '{self.model}' not available. Trying fallback...")
                # Try with a fallback model
                try:
                    response = self.client.chat.completions.create(
                        model="llama3-8b-8192",  # Most stable model
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=500
                    )
                    return response.choices[0].message.content
                except:
                    pass
            else:
                st.error(f"❌ Groq API Error: {error_msg}")
            
            # Return a fallback response
            return self._get_fallback_response()
    
    def _get_fallback_response(self):
        """Provide a fallback response when API fails"""
        return """
        🍷 **Wine Recommendation** (Offline Mode)
        
        I'm having trouble connecting to my sommelier knowledge base right now.
        
        For a classic pairing with your dish:
        - Red meat → Try a Cabernet Sauvignon or Malbec
        - White meat/Fish → Consider a Chardonnay or Sauvignon Blanc  
        - Pasta → Go with a Chianti or Pinot Grigio
        - Spicy food → Riesling or Gewürztraminer work well
        
        Please refresh and try again for a personalized recommendation!
        """