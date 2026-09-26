import streamlit as st
import google.generativeai as genai
import time

# --- Pager Setup ---
st.set_page_config(page_title="Fake News Detector", page_icon="🕵️", layout="centered")

# --- Gemini API Configuration ---
# ⚠️ REPLACE 'YOUR_API_KEY_HERE' with your actual Google Gemini API Key
# Fetch the API key securely from Streamlit secrets
try:
    GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]
except KeyError:
    st.error("API Key not found. Please configure Streamlit secrets.")
    st.stop()
    
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the Gemini model with search grounding enabled
def analyze_news(news_text):
    try:
        # Use gemini-1.5-flash which is fast and supports search grounding
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt engineered for specific output format
        prompt = f"""
        Analyze the following news excerpt or claim. Use Google Search to cross-reference facts with reliable global news sources.
        
        News Claim: "{news_text}"
        
        Provide the output strictly in two lines:
        Line 1: State clearly if the news is FAKE, REAL, or UNVERIFIED based on current search results.
        Line 2: Provide specific evidence, citing the sources you cross-referenced (e.g., "BBC and Reuters confirm this event" or "No reliable news outlet has reported this").
        """
        
        # Adding tools to enable Google Search
        response = model.generate_content(
            prompt,
            tools='google_search_retrieval'
        )
        return response.text
    except Exception as e:
        return f"ERROR\nCould not process the request. Error details: {e}"

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