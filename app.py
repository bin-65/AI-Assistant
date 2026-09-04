import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
import pypdf
import docx
import pptx

# Page configuration
st.set_page_config(page_title="AI Multi-Tool Assistant", page_icon="⚡", layout="wide")

st.title("⚡ AI Multi-Tool Assistant")

# Check API Key from Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key nahi mili! Streamlit Secrets mein GEMINI_API_KEY add karein.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.6-flash")

    # Creating Six Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "✍️ Content Assistant", 
        "🌐 Translator", 
        "🎨 Image Generator", 
        "⚡ Smart AI Workspace",
        "📚 Assignment Writer",
        "📑 Document Hub (Create/Upload/MCQs)"
    ])

    # ---------------- TAB 1: CONTENT ASSISTANT ----------------
    with tab1:
        st.subheader("Generate Social Media Posts")
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
        languages_50 = [
            "English", "Urdu", "Arabic", "Hindi", "Pashto", "Punjabi", "Sindhi", "Balochi", "Spanish", "French", 
            "German", "Chinese", "Japanese", "Korean", "Russian", "Turkish", "Italian", "Portuguese", "Persian (Farsi)", "Bengali",
            "Dutch", "Greek", "Hebrew", "Indonesian", "Malay", "Thai", "Vietnamese", "Polish", "Swedish", "Norwegian",
            "Danish", "Finnish", "Czech", "Hungarian", "Romanian", "Ukrainian", "Filipino (Tagalog)", "Swahili", "Tamil", "Telugu"
        ]
        
        target_language = st.selectbox("Select Target Language", languages_50)
        input_text = st.text_area("Source Text", placeholder="Write or paste your text here...", height=150)
        translate_btn = st.button("Translate Text")

        if translate_btn:
            if not input_text.strip():
                st.warning("Please enter some text to translate.")
            else:
                try:
                    translation_prompt = f"Automatically detect the source language and translate to natural {target_language}:\n\n{input_text}"
                    with st.spinner("Translating..."):
                        response = model.generate_content(translation_prompt)
                    st.success("Translation Complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ---------------- TAB 3: AI IMAGE GENERATOR ----------------
    with tab3:
        st.subheader("AI Image Generator")
        img_prompt = st.text_area("Image Description / Prompt", placeholder="e.g., A futuristic city in HD digital art", height=100)
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
                        width, height = (1024, 1024) if aspect_ratio == "Square (1:1)" else ((1280, 720) if aspect_ratio == "Landscape (16:9)" else (720, 1280))
                        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width={width}&height={height}&seed=42&model=flux"
                        st.image(image_url, caption=f"Generated Image: {img_prompt}", use_container_width=True)
                        st.success("Image Generated Successfully!")
                except Exception as e:
                    st.error(f"Error generating image: {e}")

    # ---------------- TAB 4: SMART AI WORKSPACE ----------------
    with tab4:
        st.subheader("⚡ Smart AI Workspace (Multi-File & Voice)")
        user_prompt = st.text_area("Your Instructions / Speech Text", placeholder="Type or paste prompt here...", height=100)
        uploaded_files = st.file_uploader("➕ Upload Files (Unlimited Images/Text)", type=["png", "jpg", "jpeg", "txt"], accept_multiple_files=True)
        process_btn = st.button("Analyze & Process Files")

        if process_btn:
            if not user_prompt.strip() and not uploaded_files:
                st.warning("Please enter instructions or upload files.")
            else:
                try:
                    with st.spinner("Processing..."):
                        contents = []
                        if uploaded_files:
                            for file in uploaded_files:
                                if "image" in file.type:
                                    contents.append(Image.open(file))
                                elif "text" in file.type:
                                    contents.append(f"\n[File: {file.name}]\n{file.read().decode('utf-8')}")
                        if user_prompt.strip():
                            contents.append(user_prompt)
                        response = model.generate_content(contents)
                    st.success("Complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ---------------- TAB 5: ASSIGNMENT WRITER ----------------
    with tab5:
        st.subheader("📚 Assignment & Homework Writer")
        with st.form("assignment_form"):
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                academic_level = st.selectbox("Academic Level", ["School", "College", "Undergraduate", "Postgraduate"])
                doc_type = st.selectbox("Document Type", ["Full Assignment", "Multiple Choice Questions (MCQs)", "Essay", "Research Paper", "Case Study"])
            with col_a2:
                word_count = st.selectbox("Word Count", ["Short (~300 words)", "Medium (~700 words)", "Long (~1500 words)", "Unlimited / Comprehensive (~3000+ words)"])
                formatting_style = st.selectbox("Formatting", ["Standard Headings", "APA Style", "MLA Style", "Harvard Style"])

            subject_topic = st.text_input("Topic", placeholder="e.g., Artificial Intelligence in Healthcare")
            additional_instructions = st.text_area("Specific Guidelines", placeholder="Paste instructions here...")
            assign_submit = st.form_submit_button("Generate Document")

        if assign_submit:
            if not subject_topic.strip():
                st.warning("Please enter a topic.")
            else:
                try:
                    assignment_prompt = f"Write {doc_type} for level: {academic_level}, length: {word_count}, style: {formatting_style}, topic: {subject_topic}. Instructions: {additional_instructions}"
                    with st.spinner("Writing..."):
                        response = model.generate_content(assignment_prompt)
                    st.success("Complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ---------------- TAB 6: ADVANCED DOCUMENT HUB (CREATE / UPLOAD / MCQs) ----------------
    with tab6:
        st.subheader("📑 Advanced Document Hub: Create, Upload & Process")
        st.write("Create custom documents/MCQs or upload PDF, Word (.docx), PPT (.pptx), and Text (.txt) files with **no word limits**.")

        col_create, col_upload = st.columns(2)

        # 2.1 Document Creation (Manual Text / MCQs Editor)
        with col_create:
            st.markdown("#### 📝 Create / Write Document")
            doc_title = st.text_input("Document Title", placeholder="e.g., Computer Networks Quiz")
            created_content = st.text_area("Create Content / Paste Raw Text / Type MCQs Draft", height=200, placeholder="Type your text or questions here...")

        # 2.2 Unlimited Multi-Format File Upload (.pdf, .docx, .pptx, .txt)
        with col_upload:
            st.markdown("#### 📁 Upload Existing Documents")
            doc_files = st.file_uploader(
                "Upload Unlimited Files (PDF, Word, PPT, TXT)", 
                type=["pdf", "docx", "pptx", "txt"], 
                accept_multiple_files=True
            )

        st.markdown("---")
        st.markdown("#### ⚙️ Process & Action Options")

        col_act1, col_act2 = st.columns(2)
        with col_act1:
            hub_action = st.selectbox(
                "Select Action to Perform", 
                [
                    "Generate Multiple Choice Questions (MCQs) with Answer Key",
                    "Summarize Entire Document",
                    "Extract Key Concepts & Explanations",
                    "Reformat & Clean Up Document",
                    "Generate Presentation Slide Outline"
                ]
            )
        with col_act2:
            num_mcqs = st.selectbox("Number of Questions (If MCQs chosen)", ["10 MCQs", "20 MCQs", "30 MCQs", "50 MCQs"])

        custom_doc_instructions = st.text_area("Specific Instructions (Optional)", placeholder="e.g., Include difficult questions with detailed explanations for correct options.")
        
        execute_hub_btn = st.button("🚀 Process & Execute Document Task")

        if execute_hub_btn:
            if not created_content.strip() and not doc_files:
                st.warning("Please create text or upload at least one file.")
            else:
                try:
                    with st.spinner("Extracting multi-format text & generating output..."):
                        extracted_text = ""

                        # Process Created Text
                        if created_content.strip():
                            extracted_text += f"\n--- CREATED CONTENT ({doc_title}) ---\n{created_content}\n"

                        # Process Uploaded Files (PDF, DOCX, PPTX, TXT)
                        if doc_files:
                            for file in doc_files:
                                extracted_text += f"\n--- FILE: {file.name} ---\n"
                                
                                # PDF Extract
                                if file.name.endswith(".pdf"):
                                    pdf_reader = pypdf.PdfReader(file)
                                    for page in pdf_reader.pages:
                                        extracted_text += page.extract_text() or ""

                                # DOCX Extract
                                elif file.name.endswith(".docx"):
                                    doc = docx.Document(file)
                                    for para in doc.paragraphs:
                                        extracted_text += para.text + "\n"

                                # PPTX Extract
                                elif file.name.endswith(".pptx"):
                                    prs = pptx.Presentation(file)
                                    for slide in prs.slides:
                                        for shape in slide.shapes:
                                            if hasattr(shape, "text"):
                                                extracted_text += shape.text + "\n"

                                # TXT Extract
                                elif file.name.endswith(".txt"):
                                    extracted_text += file.read().decode("utf-8")

                        # Build Master Prompt
                        master_prompt = (
                            f"Action Required: {hub_action}\n"
                            f"Target Quantity/Detail: {num_mcqs}\n"
                            f"Additional Instructions: {custom_doc_instructions}\n\n"
                            f"=== SOURCE DOCUMENT DATA ===\n"
                            f"{extracted_text}"
                        )

                        response = model.generate_content(master_prompt)

                    st.success("Task Completed Successfully!")
                    st.markdown("---")
                    st.markdown("### 📊 AI Generated Output:")
                    st.write(response.text)

                except Exception as e:
                    st.error(f"Error processing documents: {e}")
