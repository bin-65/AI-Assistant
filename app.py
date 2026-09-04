import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="AI Content Assistant", page_icon="✍️", layout="centered")

st.title("✍️ AI Content Assistant")
st.write("Generate customized posts powered by Gemini.")

api_key = st.secrets.get("GEMINI_API_KEY")

with st.form("content_form"):
    col1, col2 = st.columns(2)
    with col1:
        platform = st.selectbox("Platform", ["LinkedIn", "Instagram", "Twitter / X", "Facebook"])
        content_type = st.selectbox("Content Type", ["Informational Post", "Promotional / Ad", "Storytelling"])
    with col2:
        tone = st.selectbox("Tone", ["Professional", "Casual & Friendly", "Persuasive", "Inspirational"])
        target_audience = st.text_input("Target Audience", placeholder="e.g., Students, Entrepreneurs")
    
    topic = st.text_area("Topic / Core Message", placeholder="What do you want to talk about?")
    submit_btn = st.form_submit_button("Generate Content")

if submit_btn:
    if not api_key:
        st.error("API Key nahi mili! Streamlit Secrets mein GEMINI_API_KEY add karein.")
    elif not topic or not target_audience:
        st.warning("Please fill in all fields.")
    else:
        try:
            genai.configure(api_key=api_key)
            
            # Use exact stable model endpoint
            model = genai.GenerativeModel("gemini-2.0-flash")
            
            prompt = f"Platform: {platform}\nType: {content_type}\nTone: {tone}\nAudience: {target_audience}\nTopic: {topic}"
            
            with st.spinner("Generating..."):
                response = model.generate_content(prompt)
                
            st.success("Done!")
            st.markdown("---")
            st.markdown(response.text)
        except Exception as e:
            st.error(f"Error: {e}")
