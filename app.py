import streamlit as st
import openai

# Page configuration
st.set_page_config(
    page_title="TxT-S",
    page_icon="⚡",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom High-End Dark Mode Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #0B0B0E;
        color: #F1F1F3;
    }
    
    .main {
        background-color: #0B0B0E;
        padding: 2rem 1rem;
    }
    
    h1 {
        font-weight: 700;
        letter-spacing: -0.03em;
        color: #FFFFFF;
        font-size: 2.5rem !important;
        margin-bottom: 0.2rem;
    }
    
    .subtitle {
        color: #8A8A93;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    
    .stTextArea textarea {
        background-color: #141419 !important;
        color: #FFFFFF !important;
        border: 1px solid #23232C !important;
        border-radius: 12px !important;
        padding: 1rem !important;
        font-size: 0.95rem !important;
    }
    
    .stTextArea textarea:focus {
        border-color: #6366F1 !important;
        box-shadow: 0 0 0 1px #6366F1 !important;
    }
    
    .stButton button {
        background: linear-gradient(135deg, #6366F1 0%, #4F46E5 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton button:hover {
        opacity: 0.9;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
    }
    
    .result-box {
        background-color: #141419;
        border: 1px solid #23232C;
        border-radius: 12px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        color: #E2E2E7;
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.markdown("<h1>TxT-S</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Elite AI Text Summarization Engine</p>", unsafe_allow_html=True)

# API Key input in sidebar or hidden for privacy/user config
api_key = st.sidebar.text_input("OpenAI API Key", type="password")

# Input text area
text_input = st.text_area("Paste your text or article here:", height=200, placeholder="Drop your long text here to distill into core insights...")

summary_type = st.selectbox(
    "Summary Format",
    ["Bullet Points (Concise)", "Executive Paragraph", "Key Takeaways"]
)

if st.button("Generate Summary"):
    if not api_key:
        st.error("Please enter your OpenAI API Key in the sidebar first.")
    elif not text_input.strip():
        st.warning("Please provide some text to summarize.")
    else:
        with st.spinner("Distilling text..."):
            try:
                client = openai.OpenAI(api_key=api_key)
                prompt = f"Summarize the following text based on this format: {summary_type}\n\nText:\n{text_input}"
                
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "You are a professional, high-precision summarization AI assistant."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3
                )
                
                result = response.choices[0].message.content
                
                st.markdown("### Summary Result")
                st.markdown(f"<div class='result-box'>{result}</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
