# test_groq.py
# tests/test_groq.py
import streamlit as st
from groq import Groq

st.title("🧪 Groq API Test")

# Show configuration
st.sidebar.write("**Configuration:**")
st.sidebar.write(f"API Key Present: {'GROQ_API_KEY' in st.secrets}")
st.sidebar.write(f"Streamlit Cloud: {'STREAMLIT_CLOUD' in st.secrets}")

if st.button("Test Groq Connection"):
    try:
        # Initialize client
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        st.success("✅ Client initialized")
        
        # Test API call
        with st.spinner("Testing API..."):
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": "Say 'Wine test successful!' in 5 words or less"}],
                max_tokens=50
            )
        
        # Show response
        st.success("✅ API call successful!")
        st.write("**Response:**", response.choices[0].message.content)
        
        # Show available models
        st.write("**Available for your app:**")
        st.code("""
Models you can use:
- llama3-8b-8192 (recommended)
- llama3-70b-8192
- mixtral-8x7b-32768
- gemma-7b-it
        """)
        
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.write("**Debug info:**")
        st.code(str(e))