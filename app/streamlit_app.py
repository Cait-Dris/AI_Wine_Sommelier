"""Wine Sommelier AI - Interactive Web Application"""
import streamlit as st
import os
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from src.sommelier import WineSommelier
from src.personas import PERSONAS

# Page config
st.set_page_config(
    page_title="AI Wine Sommelier",
    page_icon="🍷",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if os.getenv("STREAMLIT_CLOUD"):  # Set this in Streamlit Cloud secrets
    # Use cloud API (OpenAI, Anthropic, etc.)
    from src.cloud_client import CloudLLMClient
    llm_client = CloudLLMClient(api_key=st.secrets["OPENAI_API_KEY"])
else:
    # Use local Ollama
    from src.simple_client import SimpleLLMClient
    llm_client = SimpleLLMClient()


# Custom CSS for elegant styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Open+Sans:wght@300;400;600&display=swap');
    
    /* Main theme colors */
    :root {
        --wine-red: #8B0000;
        --wine-burgundy: #722f37;
        --gold: #DAA520;
        --light-gold: #F4E4C1;
        --cream: #FFF8DC;
        --off-white: #FAF6F0;
        --charcoal: #36454F;
        --soft-gray: #8B8680;
    }
    
    /* Clean background */
    .stApp {
        background-color: var(--off-white);
    }
    
    /* Main title styling */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: var(--wine-burgundy) !important;
        text-align: center;
        font-size: 3.5rem !important;
        font-weight: 700 !important;
        margin-bottom: 0 !important;
        padding: 1rem 0;
    }
    
    /* Subtitle */
    .subtitle {
        text-align: center;
        color: var(--soft-gray);
        font-family: 'Open Sans', sans-serif;
        font-weight: 300;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-style: italic;
    }
    
    /* Card styling */
    .main-card {
        background: white;
        border-radius: 15px;
        padding: 2rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        margin: 1rem 0;
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Section headers */
    h2 {
        font-family: 'Playfair Display', serif !important;
        color: var(--wine-burgundy) !important;
        font-size: 1.8rem !important;
        margin-bottom: 1rem !important;
    }
    
    h3 {
        font-family: 'Playfair Display', serif !important;
        color: var(--charcoal) !important;
        font-size: 1.3rem !important;
    }
    
    /* Persona cards */
    .persona-card {
        background: linear-gradient(135deg, var(--wine-burgundy), var(--wine-red));
        color: white;
        padding: 1.2rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 3px 10px rgba(114, 47, 55, 0.2);
    }
    
    .persona-card h4 {
        font-family: 'Playfair Display', serif;
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
    }
    
    .persona-card p {
        margin: 0;
        font-family: 'Open Sans', sans-serif;
        font-size: 0.95rem;
        opacity: 0.95;
    }
    
    /* Button styling */
    .stButton > button {
        background: var(--gold);
        color: var(--charcoal);
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        border-radius: 25px;
        transition: all 0.3s ease;
        font-family: 'Open Sans', sans-serif;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: var(--wine-burgundy);
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(114, 47, 55, 0.3);
    }
    
    /* Text input styling */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 8px;
        border: 2px solid #E0D5C7;
        font-family: 'Open Sans', sans-serif;
        background-color: white;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: var(--gold);
        box-shadow: 0 0 0 2px rgba(218, 165, 32, 0.1);
    }
    
    /* Radio button styling */
    .stRadio > div {
        background-color: transparent;
    }
    
    /* Recommendation box */
    .recommendation-box {
        background: linear-gradient(to right, var(--cream), white);
        border-left: 4px solid var(--gold);
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
        font-family: 'Open Sans', sans-serif;
    }
    
    /* Info box styling */
    .stAlert {
        background-color: var(--light-gold);
        color: var(--charcoal);
        border-radius: 8px;
        border: 1px solid var(--gold);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-family: 'Open Sans', sans-serif;
        font-weight: 600;
        color: var(--wine-burgundy);
    }
    
    /* History item */
    .history-item {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 3px solid var(--wine-burgundy);
        transition: transform 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .history-item:hover {
        transform: translateX(5px);
        box-shadow: 0 3px 8px rgba(0,0,0,0.1);
    }
    
    /* Wine icon animation (subtle) */
    @keyframes gentle-sway {
        0%, 100% { transform: rotate(-3deg); }
        50% { transform: rotate(3deg); }
    }
    
    .wine-icon {
        display: inline-block;
        animation: gentle-sway 3s ease-in-out infinite;
    }
    
    /* Divider styling */
    hr {
        border: none;
        border-top: 1px solid #E0D5C7;
        margin: 2rem 0;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        color: var(--soft-gray);
        font-family: 'Open Sans', sans-serif;
        font-size: 0.9rem;
        padding: 2rem 0;
    }
    
    .footer a {
        color: var(--wine-burgundy);
        text-decoration: none;
        font-weight: 600;
    }
    
    .footer a:hover {
        color: var(--gold);
    }
</style>
""", unsafe_allow_html=True)

# Initialize
if 'sommelier' not in st.session_state:
    st.session_state.sommelier = WineSommelier()
if 'history' not in st.session_state:
    st.session_state.history = []
if 'show_comparison' not in st.session_state:
    st.session_state.show_comparison = False

# Header with subtle animation
st.markdown('<h1><span class="wine-icon">🍷</span> AI Wine Sommelier <span class="wine-icon">🍷</span></h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Discover the perfect wine pairing through the lens of unique AI personalities</p>', unsafe_allow_html=True)

# Main container
st.markdown('<div class="main-card">', unsafe_allow_html=True)

# Create columns with better spacing
col1, spacer, col2 = st.columns([5, 0.5, 5])

with col1:
    st.markdown("## 🍽️ Your Culinary Creation")
    
    name = st.text_input(
        "Your Name",
        placeholder="Enter your name...",
        help="We'll use this to personalize your recommendation"
    )
    
    dish = st.text_area(
        "Describe Your Dish",
        placeholder="Be descriptive! E.g., Pan-seared duck breast with cherry reduction, roasted root vegetables, and fresh thyme...",
        height=120,
        help="The more details you provide, the better the wine pairing!"
    )
    
    st.markdown("### 🎭 Choose Your Sommelier")
    
    # Create persona cards
    persona = st.radio(
        "Select a personality:",
        list(PERSONAS.keys()),
        format_func=lambda x: f"{PERSONAS[x].name}",
        horizontal=False,
        label_visibility="collapsed"
    )
    
    # Display persona info in a styled box
    st.markdown(f"""
    <div class="persona-card">
        <h4>{PERSONAS[persona].name}</h4>
        <p>{PERSONAS[persona].context}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Action buttons
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        recommend_btn = st.button(
            "🍷 Get Recommendation",
            type="primary",
            use_container_width=True,
            disabled=not (name and dish)
        )
    with col_btn2:
        compare_btn = st.button(
            "🔄 Compare All",
            use_container_width=True,
            disabled=not (name and dish)
        )

with col2:
    st.markdown("## 📜 Your Wine Recommendation")
    
    if recommend_btn and name and dish:
        with st.spinner("🍇 Consulting our sommelier..."):
            response = st.session_state.sommelier.recommend(
                customer_name=name,
                dish_description=dish,
                persona=persona
            )
            st.session_state.history.append({
                'name': name,
                'dish': dish,
                'persona': PERSONAS[persona].name,
                'response': response
            })
            st.session_state.show_comparison = False
    
    if compare_btn and name and dish:
        st.session_state.show_comparison = True
    
    # Display recommendation or comparison
    if st.session_state.show_comparison and name and dish:
        st.markdown("### 🎭 All Personalities")
        with st.spinner("Getting perspectives from all sommeliers..."):
            comparisons = st.session_state.sommelier.compare_personas(name, dish)
            tabs = st.tabs([f"🍷 {PERSONAS[p].name}" for p in PERSONAS.keys()])
            for tab, (persona_key, response) in zip(tabs, comparisons.items()):
                with tab:
                    st.markdown(f'<div class="recommendation-box">{response}</div>', unsafe_allow_html=True)
    elif st.session_state.history:
        latest = st.session_state.history[-1]
        st.markdown(f"""
        <div class="recommendation-box">
            <strong>For:</strong> {latest['name']}<br>
            <strong>Dish:</strong> {latest['dish']}<br>
            <strong>Sommelier:</strong> {latest['persona']}
        </div>
        """, unsafe_allow_html=True)
        st.markdown(latest['response'])
        
        # Export button
        if st.button("📥 Save Recommendation"):
            text = f"""
Wine Recommendation
==================
For: {latest['name']}
Dish: {latest['dish']}
Sommelier: {latest['persona']}

{latest['response']}
            """
            st.download_button(
                label="Download as TXT",
                data=text,
                file_name=f"wine_recommendation_{latest['name'].replace(' ', '_')}.txt",
                mime="text/plain"
            )
    else:
        st.info("👈 Enter your details and click 'Get Recommendation' to receive personalized wine pairing advice!")

st.markdown('</div>', unsafe_allow_html=True)

# History section
if st.session_state.history:
    st.markdown("---")
    with st.expander(f"📚 Recommendation History ({len(st.session_state.history)} entries)"):
        for i, entry in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"""
            <div class="history-item">
                <strong>{i}. {entry['name']}</strong> - {entry['dish'][:50]}...<br>
                <small>Sommelier: {entry['persona']}</small>
            </div>
            """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer">
    Made with ❤️ using Ollama and Streamlit | <a href="https://github.com/yourusername/wine-sommelier-ai">View on GitHub</a>
</div>
""", unsafe_allow_html=True)
