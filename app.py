import streamlit as st
import google.generativeai as genai
import urllib.parse

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

    # Creating Three Tabs
    tab1, tab2, tab3 = st.tabs(["✍️ Content Assistant", "🌐 Multi-Language Translator", "🎨 AI Image Generator"])

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

    # ---------------- TAB 2: MULTI-LANGUAGE TRANSLATOR (50 LANGUAGES) ----------------
    with tab2:
        st.subheader("Multi-Language Translator")
        st.write("Select a target language from the top 50 global languages.")
        
        languages_50 = [
            "English", "Urdu", "Arabic", "Hindi", "Pashto", "Punjabi", "Sindhi", "Balochi", "Spanish", "French", 
            "German", "Chinese", "Japanese", "Korean", "Russian", "Turkish", "Italian", "Portuguese", "Persian (Farsi)", "Bengali",
            "Dutch", "Greek", "Hebrew", "Indonesian", "Malay", "Thai", "Vietnamese", "Polish", "Swedish", "Norwegian",
            "Danish", "Finnish", "Czech", "Hungarian", "Romanian", "Ukrainian", "Filipino (Tagalog)", "Swahili", "Tamil", "Telugu",
            "Marathi", "Gujarati", "Kannada", "Malayalam", "Somali", "Kurdish", "Uzbek", "Kazakh", "Amharic", "Nepali"
        ]
        
        target_language = st.selectbox("Select Target Language", languages_50)
        input_text = st.text_area("Source Text", placeholder="Write or paste your text here in any language...", height=150)
        translate_btn = st.button("Translate Text")

        if translate_btn:
            if not input_text.strip():
                st.warning("Please enter some text to translate.")
            else:
                try:
                    translation_prompt = (
                        f"You are a professional translator. Automatically detect the source language of the given text "
                        f"and translate it accurately into natural, fluent {target_language}. Provide only the translated text:\n\n"
                        f"{input_text}"
                    )
                    with st.spinner(f"Translating to {target_language}..."):
                        response = model.generate_content(translation_prompt)
                    st.success("Translation Complete!")
                    st.markdown("---")
                    st.markdown(f"### Output ({target_language}):")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ---------------- TAB 3: AI IMAGE GENERATOR ----------------
    with tab3:
        st.subheader("AI Image Generator")
        st.write("Type any positive concept, title, or visual description to create an image.")
        
        img_prompt = st.text_area(
            "Image Description / Prompt", 
            placeholder="e.g., A futuristic smart city with green parks and flying cars, HD digital art", 
            height=100
        )
        
        col_style, col_ratio = st.columns(2)
        with col_style:
            image_style = st.selectbox("Style", ["Photorealistic", "Digital Art", "3D Render", "Anime / Cartoon", "Cinematic"])
        with col_ratio:
            aspect_ratio = st.selectbox("Aspect Ratio", ["Square (1:1)", "Landscape (16:9)", "Portrait (9:16)"])

        generate_img_btn = st.button("Generate Image")

        if generate_img_btn:
            if not img_prompt.strip():
                st.warning("Please enter an image description.")
            else:
                try:
                    with st.spinner("Creating image..."):
                        # Build detailed prompt
                        full_prompt = f"{img_prompt}, positive vibes, high quality, {image_style} style"
                        encoded_prompt = urllib.parse.quote(full_prompt)
                        
                        # Set dimensions based on ratio
                        width, height = 1024, 1024
                        if aspect_ratio == "Landscape (16:9)":
                            width, height = 1280, 720
                        elif aspect_ratio == "Portrait (9:16)":
                            width, height = 720, 1280
                        
                        # Generate Image URL via Pollinations AI
                        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&seed=42&model=flux"
                        
                        st.image(image_url, caption=f"Generated Image: {img_prompt}", use_container_width=True)
                        st.success("Image Generated Successfully!")
                except Exception as e:
                    st.error(f"Error generating image: {e}")
