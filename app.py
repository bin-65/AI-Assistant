import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(page_title="AI Multi-Tool Assistant", page_icon="⚡", layout="centered")

st.title("⚡ AI Multi-Tool Assistant")

# Check API Key from Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key nahi mili! Streamlit Secrets mein GEMINI_API_KEY add karein.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.6-flash")

    # Creating Two Tabs
    tab1, tab2 = st.tabs(["✍️ Content Assistant", "🌐 Language Translator"])

    # ---------------- TAB 1: CONTENT ASSISTANT ----------------
    with tab1:
        st.subheader("Generate Social Media Posts")
        st.write("Generate customized posts powered by Gemini.")
        
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
            if not topic or not target_audience:
                st.warning("Please fill in all fields.")
            else:
                try:
                    prompt = f"Platform: {platform}\nType: {content_type}\nTone: {tone}\nAudience: {target_audience}\nTopic: {topic}"
                    with st.spinner("Generating..."):
                        response = model.generate_content(prompt)
                    st.success("Done!")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ---------------- TAB 2: TRANSLATOR TO ENGLISH ----------------
    with tab2:
        st.subheader("Translate Any Language to English")
        st.write("Enter text in any language (Urdu, Spanish, Arabic, French, etc.) and translate it accurately into English.")
        
        input_text = st.text_area("Source Text", placeholder="Write or paste your text here...", height=150)
        translate_btn = st.button("Translate to English")

        if translate_btn:
            if not input_text.strip():
                st.warning("Please enter some text to translate.")
            else:
                try:
                    translation_prompt = (
                        "You are a professional translator. Automatically detect the source language of the following text "
                        "and accurately translate it into fluent, natural English. Provide only the translated English text:\n\n"
                        f"{input_text}"
                    )
                    with st.spinner("Translating..."):
                        response = model.generate_content(translation_prompt)
                    st.success("Translation Complete!")
                    st.markdown("---")
                    st.markdown("### English Translation:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")
