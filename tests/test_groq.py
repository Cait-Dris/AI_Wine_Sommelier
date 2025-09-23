# tests/test_groq.py
import streamlit as st
from groq import Groq

st.title("🧪 Groq API Test")

# Show configuration
st.sidebar.write("**Configuration:**")
st.sidebar.write(f"API Key Present: {'GROQ_API_KEY' in st.secrets}")
st.sidebar.write(f"Streamlit Cloud: {'STREAMLIT_CLOUD' in st.secrets}")

# List of models to try
models_to_test = [
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant", 
    "llama3-groq-70b-8192-tool-use-preview",
    "llama3-groq-8b-8192-tool-use-preview",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
    "gemma-7b-it"
]

if st.button("Test Groq Connection"):
    try:
        # Initialize client
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        st.success("✅ Client initialized")
        
        # Test each model
        st.write("**Testing models:**")
        working_models = []
        
        for model in models_to_test:
            try:
                with st.spinner(f"Testing {model}..."):
                    response = client.chat.completions.create(
                        model=model,
                        messages=[{"role": "user", "content": "Say 'hello' in one word"}],
                        max_tokens=10
                    )
                st.success(f"✅ {model} - WORKS")
                working_models.append(model)
            except Exception as e:
                if "does not exist" in str(e) or "decommissioned" in str(e):
                    st.error(f"❌ {model} - Not available")
                else:
                    st.warning(f"⚠️ {model} - Error: {str(e)[:100]}")
        
        if working_models:
            st.success(f"**Found {len(working_models)} working models!**")
            st.code("\n".join(working_models))
        else:
            st.error("No working models found!")
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")