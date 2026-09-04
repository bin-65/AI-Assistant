import streamlit as st
import google.generativeai as genai
from PIL import Image
import urllib.parse
import pypdf
import docx
import pptx
from docx import Document
from pptx import Presentation
from fpdf import FPDF
import io

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
        "🎨 AI Image Generator 📸", 
        "⚡ Smart AI Workspace",
        "📚 Assignment Writer",
        "📑 Advanced Document Hub"
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

    # ---------------- TAB 2: TRANSLATOR ----------------
    with tab2:
        st.subheader("Multi-Language Translator")
        languages_50 = ["English", "Urdu", "Arabic", "Hindi", "Pashto", "Punjabi", "Sindhi", "Spanish", "French", "German", "Chinese"]
        target_language = st.selectbox("Select Target Language", languages_50)
        input_text = st.text_area("Source Text", placeholder="Write or paste your text here...", height=150)
        translate_btn = st.button("Translate Text")

        if translate_btn:
            if not input_text.strip():
                st.warning("Please enter some text to translate.")
            else:
                try:
                    translation_prompt = f"Automatically detect source language and translate to {target_language}:\n\n{input_text}"
                    with st.spinner("Translating..."):
                        response = model.generate_content(translation_prompt)
                    st.success("Translation Complete!")
                    st.markdown("---")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Error: {e}")

    # ---------------- TAB 3: AI IMAGE GENERATOR (ChatGPT Style Simple) ----------------
    with tab3:
        st.subheader("🎨 AI Image Generator")
        st.write("Write anything you want to create an image for (Education, Science, Art, Nature, Diagrams, 3D Models, etc.)")
        
        img_prompt = st.text_area(
            "What image do you want to create?", 
            placeholder="e.g., A detailed diagram of a human heart with labels for educational purpose", 
            height=120
        )

        generate_img_btn = st.button("✨ Create Image")

        if generate_img_btn:
            if not img_prompt.strip():
                st.warning("Please enter an image description.")
            else:
                try:
                    with st.spinner("Generating image..."):
                        encoded_prompt = urllib.parse.quote(img_prompt)
                        # Pollinations AI image URL
                        image_url = f"https://pollinations.ai/p/{encoded_prompt}?width=1024&height=1024&seed=42&model=flux"
                        
                        # Show Image directly like ChatGPT
                        st.image(image_url, caption=f"Prompt: {img_prompt}", use_container_width=True)
                        st.success("Image Created Successfully!")
                        
                        # Download Link/Button
                        st.markdown(f'''
                            <div style="margin-top: 15px;">
                                <a href="{image_url}" target="_blank" download="ai_image.jpg">
                                    <button style="background-color: #008CBA; color: white; border: none; padding: 10px 24px; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold;">
                                        📥 Download Image
                                    </button>
                                </a>
                            </div>
                        ''', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Error generating image: {e}")

    # ---------------- TAB 4: SMART AI WORKSPACE ----------------
    with tab4:
        st.subheader("⚡ Smart AI Workspace")
        user_prompt = st.text_area("Instructions / Prompt", placeholder="Type here...", height=100)
        uploaded_files = st.file_uploader("Upload Files", type=["png", "jpg", "jpeg", "txt"], accept_multiple_files=True)
        process_btn = st.button("Process")

        if process_btn:
            if not user_prompt.strip() and not uploaded_files: st.warning("Please enter input.")
            else:
                try:
                    with st.spinner("Processing..."):
                        contents = []
                        if uploaded_files:
                            for file in uploaded_files:
                                if "image" in file.type: contents.append(Image.open(file))
                                elif "text" in file.type: contents.append(file.read().decode('utf-8'))
                        if user_prompt.strip(): contents.append(user_prompt)
                        response = model.generate_content(contents)
                    st.success("Done!")
                    st.markdown(response.text)
                except Exception as e: st.error(f"Error: {e}")

    # ---------------- TAB 5: ASSIGNMENT WRITER ----------------
    with tab5:
        st.subheader("📚 Assignment Writer")
        with st.form("assignment_form"):
            subject_topic = st.text_input("Topic", placeholder="e.g., Quantum Computing")
            academic_level = st.selectbox("Level", ["School", "College", "Undergraduate", "Postgraduate"])
            assign_submit = st.form_submit_button("Generate")

        if assign_submit:
            if not subject_topic.strip(): st.warning("Enter topic.")
            else:
                try:
                    prompt = f"Write detailed assignment on {subject_topic} for level {academic_level}."
                    with st.spinner("Writing..."): response = model.generate_content(prompt)
                    st.markdown(response.text)
                except Exception as e: st.error(f"Error: {e}")

    # ---------------- TAB 6: ADVANCED DOCUMENT HUB ----------------
    with tab6:
        st.subheader("📑 Advanced Document Hub")
        
        doc_sub_tab1, doc_sub_tab2 = st.tabs(["📝 1. Create New Document / File", "📤 2. Upload Document & Extract MCQs"])

        # ------------ PROCEDURE 1: CREATE FILE & EXPORT ------------
        with doc_sub_tab1:
            st.markdown("### 📝 Create Document & Export to MS Office / PDF")
            
            doc_topic = st.text_input("Document Subject / Topic", placeholder="e.g., Fundamentals of Artificial Intelligence")
            export_format = st.selectbox("Select Output File Format", ["MS Word (.docx)", "PowerPoint Presentation (.pptx)", "PDF Document (.pdf)"])
            doc_length = st.selectbox("Content Length", ["Detailed Notes (~500 words)", "Full Chapter (~1500 words)", "Comprehensive Manual (~3000+ words)"])
            custom_prompt = st.text_area("Specific Outline / Instructions (Optional)", placeholder="e.g., Add 5 slides outline with headings...")

            create_doc_btn = st.button("✨ Generate Document Content")

            if create_doc_btn:
                if not doc_topic.strip():
                    st.warning("Please enter a topic.")
                else:
                    try:
                        with st.spinner("Generating document content..."):
                            gen_prompt = (
                                f"Create a comprehensive academic document on '{doc_topic}'.\n"
                                f"Format target: {export_format}\n"
                                f"Length: {doc_length}\n"
                                f"Instructions: {custom_prompt if custom_prompt else 'Include clear headings and structure.'}"
                            )
                            response = model.generate_content(gen_prompt)
                            generated_text = response.text

                        st.success("Document Generated Successfully!")
                        st.markdown("---")
                        
                        st.markdown("#### 📄 Document Preview (Copy Text Below):")
                        st.code(generated_text, language="markdown")

                        st.markdown("#### 💾 Download Exported File:")
                        
                        if export_format == "MS Word (.docx)":
                            doc = Document()
                            doc.add_heading(doc_topic, 0)
                            for paragraph in generated_text.split("\n\n"):
                                doc.add_paragraph(paragraph)
                            bio = io.BytesIO()
                            doc.save(bio)
                            st.download_button("📥 Download MS Word File (.docx)", data=bio.getvalue(), file_name=f"{doc_topic}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

                        elif export_format == "PowerPoint Presentation (.pptx)":
                            prs = Presentation()
                            slides_content = generated_text.split("\n\n")
                            for slide_text in slides_content[:10]:
                                slide = prs.slides.add_slide(prs.slide_layouts[1])
                                title = slide.shapes.title
                                body = slide.placeholders[1]
                                title.text = doc_topic
                                body.text = slide_text
                            bio = io.BytesIO()
                            prs.save(bio)
                            st.download_button("📥 Download PowerPoint File (.pptx)", data=bio.getvalue(), file_name=f"{doc_topic}.pptx", mime="application/vnd.openxmlformats-officedocument.presentationml.presentation")

                        elif export_format == "PDF Document (.pdf)":
                            pdf = FPDF()
                            pdf.add_page()
                            pdf.set_font("Arial", size=11)
                            clean_text = generated_text.encode('latin-1', 'replace').decode('latin-1')
                            pdf.multi_cell(0, 10, clean_text)
                            pdf_output = pdf.output(dest='S').encode('latin-1')
                            st.download_button("📥 Download PDF File (.pdf)", data=pdf_output, file_name=f"{doc_topic}.pdf", mime="application/pdf")

                    except Exception as e:
                        st.error(f"Error generating document: {e}")

        # ------------ PROCEDURE 2: UPLOAD & MCQs EXTRACTION ------------
        with doc_sub_tab2:
            st.markdown("### 📤 Upload Files & Unlimited MCQs / Summary Generator")
            
            uploaded_docs = st.file_uploader(
                "Upload Files (PDF, Word, PPT, TXT)", 
                type=["pdf", "docx", "pptx", "txt"], 
                accept_multiple_files=True
            )

            mcq_count = st.selectbox("Number of Questions to Extract", ["10 MCQs", "20 MCQs", "30 MCQs", "50 MCQs", "100 MCQs"])
            task_type = st.selectbox("Task Type", ["Generate Multiple Choice Questions (MCQs) with Answer Key", "Summarize Documents", "Extract Formulas & Definitions"])

            process_upload_btn = st.button("🚀 Process Uploaded Files")

            if process_upload_btn:
                if not uploaded_docs:
                    st.warning("Please upload at least one file.")
                else:
                    try:
                        with st.spinner("Extracting content from files..."):
                            extracted_full_text = ""
                            for file in uploaded_docs:
                                extracted_full_text += f"\n--- FILE: {file.name} ---\n"
                                if file.name.endswith(".pdf"):
                                    pdf_reader = pypdf.PdfReader(file)
                                    for page in pdf_reader.pages: extracted_full_text += page.extract_text() or ""
                                elif file.name.endswith(".docx"):
                                    doc = docx.Document(file)
                                    for p in doc.paragraphs: extracted_full_text += p.text + "\n"
                                elif file.name.endswith(".pptx"):
                                    prs = pptx.Presentation(file)
                                    for slide in prs.slides:
                                        for shape in slide.shapes:
                                            if hasattr(shape, "text"): extracted_full_text += shape.text + "\n"
                                elif file.name.endswith(".txt"):
                                    extracted_full_text += file.read().decode("utf-8")

                            mcq_prompt = (
                                f"Task: {task_type}\n"
                                f"Quantity: {mcq_count}\n"
                                f"Instructions: Create clear multiple choice questions with options (A, B, C, D) and Answer Key.\n\n"
                                f"=== SOURCE FILE TEXT ===\n"
                                f"{extracted_full_text}"
                            )

                            response = model.generate_content(mcq_prompt)
                            output_text = response.text

                        st.success("Extraction Complete!")
                        st.markdown("---")
                        st.markdown("#### 📋 Extracted Result (Copy Code/Text Box):")
                        st.code(output_text, language="markdown")

                        st.markdown("#### 💾 Download Output File:")
                        doc_mcq = Document()
                        doc_mcq.add_heading("Extracted MCQs & Analysis", 0)
                        for p in output_text.split("\n\n"): doc_mcq.add_paragraph(p)
                        bio_mcq = io.BytesIO()
                        doc_mcq.save(bio_mcq)
                        
                        st.download_button("📥 Download Result as Word (.docx)", data=bio_mcq.getvalue(), file_name="Extracted_MCQs.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

                    except Exception as e:
                        st.error(f"Error processing upload: {e}")
