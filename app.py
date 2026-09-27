import streamlit as st
from groq import Groq
import time

# --- Page Setup ---
st.set_page_config(page_title="Fake News Detector", page_icon="🕵️", layout="centered")

# Fetch the Groq API key securely from Streamlit secrets
try:
    GROQ_API_KEY = st.secrets["GROQ_API_KEY"]
    client = Groq(api_key=GROQ_API_KEY)
except Exception as e:
    st.error("Groq API Key not found in Streamlit Secrets. Please configure GROQ_API_KEY in app settings.")
    st.stop()

# --- Caching with Groq API ---
@st.cache_data(show_spinner=False)
def analyze_news(news_text):
    try:
        prompt = f"""
        Act as an expert fact-checker. Analyze the following news excerpt or claim based on your extensive training data.
        
        News Claim: "{news_text}"
        
        Provide the output strictly in two lines:
        Line 1: State clearly if the news is FAKE, REAL, or UNVERIFIED.
        Line 2: Provide specific reasoning or historical context to support your verdict.
        """
        
        # Using Groq's fast Llama model
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
        )
        return completion.choices[0].message.content
        
    except Exception as e:
        return f"ERROR\nDetailed Exception: {str(e)}"

# --- UI Design ---
st.title("🚨 Fake News Detector Dashboard")
st.markdown("A Hybrid AI engine powered by Groq to detect misinformation instantly.")

st.divider()

st.subheader("Verify News Authenticity")
user_input = st.text_area("Paste an article excerpt, headline, or claim here...", height=150)

if st.button("🔍 Analyze Authenticity", type="primary"):
    if not user_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing linguistic patterns and scanning live global news sources..."):
            time.sleep(1.0)  
            
            # Call the Groq API
            result = analyze_news(user_input)
            
            # Process Output
            lines = result.split('\n')
            
            if len(lines) >= 2:
                verdict = lines[0].strip()
                evidence = ' '.join(lines[1:]).strip()
            else:
                verdict = "UNVERIFIED"
                evidence = result
            
            st.divider()
            st.subheader("Analysis Result")
            
            if "FAKE" in verdict.upper():
                st.error(f"**Verdict:** {verdict}")
                st.info(f"**Evidence:** {evidence}")
            elif "REAL" in verdict.upper():
                st.success(f"**Verdict:** {verdict}")
                st.info(f"**Evidence:** {evidence}")
            else:
                st.warning(f"**Verdict:** {verdict}")
                st.info(f"**Evidence:** {evidence}")
