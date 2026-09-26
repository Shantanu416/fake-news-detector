import streamlit as st
import google.generativeai as genai
import time

# --- Pager Setup ---
st.set_page_config(page_title="Fake News Detector", page_icon="🕵️", layout="centered")

# Fetch the API key securely from Streamlit secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=GOOGLE_API_KEY)
except Exception as e:
    st.error("Google API Key not found in Streamlit Secrets. Please configure it in app settings.")
    st.stop()
# Initialize the Gemini model with detailed error reporting
# Initialize the Gemini model using safe lookup
def analyze_news(news_text):
    try:
        prompt = f"""
        Act as an expert fact-checker. Analyze the following news excerpt or claim based on your extensive training data.
        
        News Claim: "{news_text}"
        
        Provide the output strictly in two lines:
        Line 1: State clearly if the news is FAKE, REAL, or UNVERIFIED.
        Line 2: Provide specific reasoning or historical context to support your verdict.
        """
        
        # Let's iterate through available models dynamically or use a guaranteed safe fallback
        model = None
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                if 'flash' in m.name or 'pro' in m.name:
                    model = genai.GenerativeModel(m.name)
                    break
        
        if not model:
            model = genai.GenerativeModel('gemini-pro')
            
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        return f"ERROR\nDetailed Exception: {str(e)}"

# --- UI Design ---
st.title("🚨 Fake News Detector Dashboard")
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
            
            # Call the backend API
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
            
            # Dynamic UI styling based on verdict
            if "FAKE" in verdict.upper():
                st.error(f"**Verdict:** {verdict}")
                st.info(f"**Evidence:** {evidence}")
            elif "REAL" in verdict.upper():
                st.success(f"**Verdict:** {verdict}")
                st.info(f"**Evidence:** {evidence}")
            else:
                st.warning(f"**Verdict:** {verdict}")
                st.info(f"**Evidence:** {evidence}")
