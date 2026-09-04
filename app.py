import streamlit as st
import google.generativeai as genai
from PIL import Image
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

    # Creating Five Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "✍️ Content Assistant", 
        "🌐 Translator", 
        "🎨 Image Generator", 
        "⚡ Smart AI Workspace",
        "📚 Assignment & Essay Writer"
    ])

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

    # ---------------- TAB 2: MULTI-LANGUAGE TRANSLATOR ----------------
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
                        full_prompt = f"{img_prompt}, positive vibes, high quality, {image_style} style"
                        encoded_prompt = urllib.parse.quote(full_prompt)
                        
                        width, height = 1024, 1024
                        if aspect_ratio == "Landscape (16:9)":
                            width, height = 1280, 720
                        elif aspect_ratio == "Portrait (9:16)":
                            width, height = 720, 1280
                        
                        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&seed=42&model=flux"
                        st.image(image_url, caption=f"Generated Image: {img_prompt}", use_container_width=True)
                        st.success("Image Generated Successfully!")
                except Exception as e:
                    st.error(f"Error generating image: {e}")

    # ---------------- TAB 4: SMART AI WORKSPACE (UNLIMITED MULTI-FILES + VOICE) ----------------
    with tab4:
        st.subheader("⚡ Smart AI Workspace (Multi-File & Voice)")
        st.write("Upload multiple images/text files with no limit and ask questions via text or voice.")

        # Voice Input UI
        st.markdown("""
        <div style="background-color: #f0f2f6; padding: 15px; border-radius: 10px; margin-bottom: 15px;">
            <p style="margin: 0 0 10px 0; font-weight: bold; color: #1E1E1E;">🎤 Voice Input (Microphone):</p>
            <button id="start-btn" onclick="startConverting()" style="background-color: #ff4b4b; color: white; border: none; padding: 8px 16px; border-radius: 5px; cursor: pointer; font-weight: bold;">
                🔴 Start Speaking
            </button>
            <p id="voice-status" style="margin-top: 10px; font-size: 14px; color: #555;">Click button to convert voice to text...</p>
        </div>

        <script>
            function startConverting() {
                var status = document.getElementById('voice-status');
                if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
                    var SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                    var recognition = new SpeechRecognition();
                    recognition.continuous = false;
                    recognition.interimResults = false;
                    recognition.lang = 'en-US';

                    recognition.onstart = function() { status.innerHTML = '🎙️ Listening... Speak now!'; };
                    recognition.onspeechend = function() { status.innerHTML = '✅ Processing complete!'; recognition.stop(); };
                    recognition.onresult = function(event) {
                        status.innerHTML = '<strong>Recognized Text:</strong> ' + event.results[0][0].transcript;
                    };
                    recognition.onerror = function(event) { status.innerHTML = '❌ Voice Error: ' + event.error; };
                    recognition.start();
                } else {
                    status.innerHTML = '⚠️ Voice recognition requires Google Chrome browser.';
                }
            }
        </script>
        """, unsafe_allow_html=True)

        user_prompt = st.text_area("Your Instructions / Prompt / Speech Text", placeholder="Type or paste your prompt here...", height=100)

        # Unlimited Multi-File Upload Option (`accept_multiple_files=True`)
        uploaded_files = st.file_uploader(
            "➕ Upload Files (Unlimited PNG, JPG, JPEG, TXT files)", 
            type=["png", "jpg", "jpeg", "txt"], 
            accept_multiple_files=True
        )

        process_btn = st.button("Analyze & Process Files")

        if process_btn:
            if not user_prompt.strip() and not uploaded_files:
                st.warning("Please enter instructions or upload files.")
            else:
                try:
                    with st.spinner("Processing files and response..."):
                        contents = []
                        
                        if uploaded_files:
                            for file in uploaded_files:
                                if "image" in file.type:
                                    img = Image.open(file)
                                    contents.append(img)
                                elif "text" in file.type:
                                    txt = file.read().decode("utf-8")
                                    contents.append(f"\n[File: {file.name}]\n{txt}")

                        if user_prompt.strip():
                            contents.append(user_prompt)

                        response = model.generate_content(contents)
                        
                    st.success("Analysis Complete!")
                    st.markdown("---")
                    st.markdown("### 🤖 AI Response:")
                    st.write(response.text)
                except Exception as e:
                    st.error(f"Error processing request: {e}")

    # ---------------- TAB 5: ASSIGNMENT & ESSAY WRITER ----------------
    with tab5:
        st.subheader("📚 Assignment & Homework Writer")
        st.write("Generate high-quality assignments, essays, research outlines, and coursework.")

        with st.form("assignment_form"):
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                academic_level = st.selectbox("Academic Level", ["School", "College / High School", "Undergraduate (University)", "Postgraduate / Master's"])
                doc_type = st.selectbox("Document Type", ["Full Assignment", "Essay", "Research Paper Outline", "Case Study Solution", "Question Answers"])
            with col_a2:
                word_count = st.selectbox("Approximate Word Count", ["Short (~300 words)", "Medium (~700 words)", "Long (~1500 words)", "Comprehensive (~2500+ words)"])
                formatting_style = st.selectbox("Formatting Style", ["Standard Headings & Bullets", "APA Style", "MLA Style", "Harvard Style"])

            subject_topic = st.text_input("Subject & Assignment Topic", placeholder="e.g., Computer Science: Artificial Intelligence in Modern Healthcare")
            additional_instructions = st.text_area("Specific Questions or Guidelines (Optional)", placeholder="Paste assignment questions or specific guidelines here...")

            assign_submit = st.form_submit_button("Generate Assignment")

        if assign_submit:
            if not subject_topic.strip():
                st.warning("Please enter a subject and topic.")
            else:
                try:
                    assignment_prompt = (
                        f"You are an expert academic tutor. Write a high-quality, well-researched {doc_type}.\n\n"
                        f"- Level: {academic_level}\n"
                        f"- Length: {word_count}\n"
                        f"- Formatting Style: {formatting_style}\n"
                        f"- Subject & Topic: {subject_topic}\n"
                        f"- Specific Guidelines: {additional_instructions if additional_instructions else 'None'}\n\n"
                        f"Ensure clear subheadings, structured paragraphs, logical flow, and academic tone."
                    )
                    with st.spinner("Writing assignment..."):
                        response = model.generate_content(assignment_prompt)
                    
                    st.success("Assignment Generated Successfully!")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error generating assignment: {e}")
