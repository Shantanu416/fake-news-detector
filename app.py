import streamlit as st
import google.generativeai as genai
import time

# --- Page Setup ---
st.set_page_config(page_title="Fake News Detector", page_icon="🕵️", layout="centered")

# Fetch the API key securely from Streamlit secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error("Google API Key not found in Streamlit Secrets. Please configure it in app settings.")
    st.stop()

# --- Caching added here to save API Quota ---
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
        # Wapas gemini-3.8-flash par set kar rahe hain jo Google recommend kar raha hai
        model = genai.GenerativeModel("gemini-3.8-flash")
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ERROR\nDetailed Exception: {str(e)}"

# --- UI Design ---
st.title("🚨 Fake News Detector ")
st.markdown("A Hybrid AI engine that analyzes text and cross-references live global sources to detect misinformation.")

st.divider()

st.subheader("Verify News Authenticity")
user_input = st.text_area("Paste an article excerpt, headline, or claim here...", height=150)

if st.button("🔍 Analyze Authenticity", type="primary"):
    if not user_input.strip():
        st.warning("Please enter some text to analyze.")
    else:
        with st.spinner("Analyzing linguistic patterns and scanning live global news sources..."):
            # Add a slight delay for dramatic effect in presentation
            time.sleep(1.5)  
            
            # Call the backend API (Cached)
            result = analyze_news(user_input)
            
            # Process Output
            lines = result.split('\n')
            
            # Fallback if the API returns unexpected formatting
            if len(lines) >= 2:
                verdict = lines[0].strip()
                evidence = ' '.join(lines[1:]).strip() # Combine rest as evidence
            else:
                verdict = "UNVERIFIED"
                evidence = result
            
            st.divider()
            st.subheader("Analysis Result")
            
            # FIXED & COMPLETED: Dynamic UI styling based on verdict with proper rendering blocks
            if "FAKE" in verdict.upper():
                st.error(f"**Verdict:** {verdict}")
                st.info(f"**Evidence:** {evidence}")
            elif "REAL" in verdict.upper():
                st.success(f"**Verdict:** {verdict}")
                st.info(f"**Evidence:** {evidence}")
            else:
                st.warning(f"**Verdict:** {verdict}")
                st.info(f"**Evidence:** {evidence}")
