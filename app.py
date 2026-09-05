import streamlit as st
import google.generativeai as genai
from PIL import Image
import pypdf
import docx
import pptx
from docx import Document
from pptx import Presentation
from fpdf import FPDF
import io

# Page configuration
st.set_page_config(page_title="AI Multi-Tool Assistant", page_icon="⚡", layout="wide")

st.title("⚡ AI Multi-Tool Assistant (Unlimited Edition)")

# Helper function to generate PDF bytes safely
def generate_pdf_bytes(title, text_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, title.encode('latin-1', 'replace').decode('latin-1'), ln=True)
    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    clean_text = text_content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, clean_text)
    return pdf.output()

# Helper function to generate Word bytes safely
def generate_docx_bytes(title, text_content):
    doc = Document()
    doc.add_heading(title, 0)
    for paragraph in text_content.split("\n\n"):
        doc.add_paragraph(paragraph)
    bio = io.BytesIO()
    doc.save(bio)
    return bio.getvalue()

# Check API Key from Secrets
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("API Key nahi mili! Streamlit Secrets mein GEMINI_API_KEY add karein.")
else:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-3.6-flash")

    # Sidebar Information
    st.sidebar.markdown("### ♾️ App Access Status")
    st.sidebar.success("✅ **Unlimited Access Enabled**\nAap tamam features bina kisi limit ke kitni bhi baar use kar sakte hain!")

    # Five Active Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "✍️ Content Assistant", 
        "🌐 Translator", 
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
                    res_text = response.text
                    
                    st.success("Done!")
                    st.markdown("---")
                    
                    st.markdown("#### 📋 Copy Generated Document:")
                    st.code(res_text, language="markdown")
                    
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.download_button("📥 Download PDF", data=generate_pdf_bytes(f"{platform} Post", res_text), file_name="Social_Media_Post.pdf", mime="application/pdf")
                    with col_d2:
                        st.download_button("📥 Download Word (.docx)", data=generate_docx_bytes(f"{platform} Post", res_text), file_name="Social_Media_Post.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
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
                    res_text = response.text
                    
                    st.success("Translation Complete!")
                    st.markdown("---")
                    
                    st.markdown("#### 📋 Copy Translated Text:")
                    st.code(res_text, language="markdown")
                    
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.download_button("📥 Download PDF", data=generate_pdf_bytes(f"Translation ({target_language})", res_text), file_name="Translation.pdf", mime="application/pdf")
                    with col_d2:
                        st.download_button("📥 Download Word (.docx)", data=generate_docx_bytes(f"Translation ({target_language})", res_text), file_name="Translation.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                except Exception as e:
                    st.error(f"Error: {e}")

    # ---------------- TAB 3: SMART AI WORKSPACE ----------------
    with tab3:
        st.subheader("⚡ Smart AI Workspace")
        st.write("Upload Images or Documents (PDF, Word, PPT, TXT) with Unlimited File Size!")
        
        user_prompt = st.text_area("Instructions / Prompt", placeholder="e.g., Summarize these files or extract key information...", height=100)
        uploaded_files = st.file_uploader(
            "Upload Files (PDF, DOCX, PPTX, TXT, Images)", 
            type=["png", "jpg", "jpeg", "pdf", "docx", "pptx", "txt"], 
            accept_multiple_files=True
        )
        process_btn = st.button("Process Workspace Request")

        if process_btn:
            if not user_prompt.strip() and not uploaded_files:
                st.warning("Please enter instructions or upload at least one file.")
            else:
                try:
                    with st.spinner("Processing workspace files..."):
                        contents = []
                        extracted_text_from_docs = ""

                        if uploaded_files:
                            for file in uploaded_files:
                                file_type = file.type or ""
                                filename = file.name.lower()

                                if "image" in file_type or filename.endswith((".png", ".jpg", ".jpeg")):
                                    contents.append(Image.open(file))
                                elif filename.endswith(".pdf"):
                                    pdf_reader = pypdf.PdfReader(file)
                                    pdf_text = "\n".join([page.extract_text() or "" for page in pdf_reader.pages])
                                    extracted_text_from_docs += f"\n--- [PDF: {file.name}] ---\n{pdf_text}\n"
                                elif filename.endswith(".docx"):
                                    doc_file = docx.Document(file)
                                    docx_text = "\n".join([p.text for p in doc_file.paragraphs])
                                    extracted_text_from_docs += f"\n--- [Word: {file.name}] ---\n{docx_text}\n"
                                elif filename.endswith(".pptx"):
                                    prs_file = pptx.Presentation(file)
                                    pptx_text = ""
                                    for slide in prs_file.slides:
                                        for shape in slide.shapes:
                                            if hasattr(shape, "text"): pptx_text += shape.text + "\n"
                                    extracted_text_from_docs += f"\n--- [PPT: {file.name}] ---\n{pptx_text}\n"
                                elif filename.endswith(".txt"):
                                    extracted_text_from_docs += f"\n--- [TXT: {file.name}] ---\n{file.read().decode('utf-8', errors='ignore')}\n"

                        final_instruction = ""
                        if extracted_text_from_docs:
                            final_instruction += f"=== EXTRACTED DOCUMENTS CONTENT ===\n{extracted_text_from_docs}\n"
                        if user_prompt.strip():
                            final_instruction += f"=== USER INSTRUCTION ===\n{user_prompt}"

                        if final_instruction: contents.append(final_instruction)
                        response = model.generate_content(contents)
                        res_text = response.text

                    st.success("Processing Complete!")
                    st.markdown("---")
                    
                    st.markdown("#### 📋 Copy Workspace Output:")
                    st.code(res_text, language="markdown")
                    
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.download_button("📥 Download PDF", data=generate_pdf_bytes("Workspace Output", res_text), file_name="Smart_Workspace_Output.pdf", mime="application/pdf")
                    with col_d2:
                        st.download_button("📥 Download Word (.docx)", data=generate_docx_bytes("Workspace Output", res_text), file_name="Smart_Workspace_Output.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                except Exception as e:
                    st.error(f"Error processing request: {e}")

    # ---------------- TAB 4: ASSIGNMENT WRITER ----------------
    with tab4:
        st.subheader("📚 Assignment Writer")
        with st.form("assignment_form"):
            subject_topic = st.text_input("Topic", placeholder="e.g., Quantum Computing")
            academic_level = st.selectbox("Level", ["School", "College", "Undergraduate", "Postgraduate"])
            assign_submit = st.form_submit_button("Generate Assignment")

        if assign_submit:
            if not subject_topic.strip():
                st.warning("Enter topic.")
            else:
                try:
                    prompt = f"Write detailed assignment on {subject_topic} for level {academic_level}."
                    with st.spinner("Writing assignment..."):
                        response = model.generate_content(prompt)
                    res_text = response.text
                    
                    st.success("Assignment Generated!")
                    st.markdown("---")
                    
                    st.markdown("#### 📋 Copy Full Assignment Text:")
                    st.code(res_text, language="markdown")
                    
                    col_d1, col_d2 = st.columns(2)
                    with col_d1:
                        st.download_button("📥 Download PDF", data=generate_pdf_bytes(f"Assignment: {subject_topic}", res_text), file_name=f"{subject_topic}_Assignment.pdf", mime="application/pdf")
                    with col_d2:
                        st.download_button("📥 Download Word (.docx)", data=generate_docx_bytes(f"Assignment: {subject_topic}", res_text), file_name=f"{subject_topic}_Assignment.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
                except Exception as e:
                    st.error(f"Error: {e}")

    # ---------------- TAB 5: ADVANCED DOCUMENT HUB ----------------
    with tab5:
        st.subheader("📑 Advanced Document Hub")
        
        doc_sub_tab1, doc_sub_tab2 = st.tabs(["📝 1. Create New Document / File", "📤 2. Upload Document & Extract MCQs (PDF Export)"])

        # PROCEDURE 1: CREATE FILE & EXPORT
        with doc_sub_tab1:
            st.markdown("### 📝 Create Document & Export")
            
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
                        
                        st.markdown("#### 📋 Copy Document Text:")
                        st.code(generated_text, language="markdown")

                        st.markdown("#### 💾 Download Exported File:")
                        
                        if export_format == "MS Word (.docx)":
                            st.download_button("📥 Download MS Word File (.docx)", data=generate_docx_bytes(doc_topic, generated_text), file_name=f"{doc_topic}.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

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
                            st.download_button("📥 Download PDF File (.pdf)", data=generate_pdf_bytes(doc_topic, generated_text), file_name=f"{doc_topic}.pdf", mime="application/pdf")

                    except Exception as e:
                        st.error(f"Error generating document: {e}")

        # PROCEDURE 2: UPLOAD & MCQs EXTRACTION
        with doc_sub_tab2:
            st.markdown("### 📤 Upload Files & Extract MCQs / Summary (Download as PDF)")
            
            uploaded_docs = st.file_uploader(
                "Upload Files (PDF, Word, PPT, TXT) - Unlimited Size Supported", 
                type=["pdf", "docx", "pptx", "txt"], 
                accept_multiple_files=True
            )

            mcq_count = st.selectbox("Number of Questions to Extract", ["10 MCQs", "20 MCQs", "30 MCQs", "50 MCQs", "100 MCQs (Comprehensive)"])
            task_type = st.selectbox("Task Type", ["Generate Multiple Choice Questions (MCQs) with Answer Key", "Summarize Documents", "Extract Formulas & Definitions"])

            process_upload_btn = st.button("🚀 Process Uploaded Files")

            if process_upload_btn:
                if not uploaded_docs:
                    st.warning("Please upload at least one file.")
                else:
                    try:
                        with st.spinner("Extracting content and generating MCQs..."):
                            extracted_full_text = ""
                            for file in uploaded_docs:
                                extracted_full_text += f"\n--- FILE: {file.name} ---\n"
                                if file.name.endswith(".pdf"):
                                    pdf_reader = pypdf.PdfReader(file)
                                    for page in pdf_reader.pages: extracted_full_text += (page.extract_text() or "") + "\n"
                                elif file.name.endswith(".docx"):
                                    doc = docx.Document(file)
                                    for p in doc.paragraphs: extracted_full_text += p.text + "\n"
                                elif file.name.endswith(".pptx"):
                                    prs = pptx.Presentation(file)
                                    for slide in prs.slides:
                                        for shape in slide.shapes:
                                            if hasattr(shape, "text"): extracted_full_text += shape.text + "\n"
                                elif file.name.endswith(".txt"):
                                    extracted_full_text += file.read().decode("utf-8", errors="ignore")

                            mcq_prompt = (
                                f"Task: {task_type}\n"
                                f"Quantity: {mcq_count}\n"
                                f"Instructions: Create clear multiple choice questions with options (A, B, C, D) and an Answer Key with explanations at the bottom.\n\n"
                                f"=== SOURCE FILE TEXT ===\n"
                                f"{extracted_full_text}"
                            )

                            response = model.generate_content(mcq_prompt)
                            output_text = response.text

                        st.success("MCQs Extraction Complete!")
                        st.markdown("---")
                        
                        st.markdown("#### 📋 Copy All MCQs / Extracted Output:")
                        st.code(output_text, language="markdown")

                        st.markdown("#### 💾 Download MCQs File:")
                        col_mcq1, col_mcq2 = st.columns(2)
                        
                        with col_mcq1:
                            st.download_button("📥 Download MCQs as PDF (.pdf)", data=generate_pdf_bytes("Extracted MCQs & Answer Key", output_text), file_name="Extracted_MCQs.pdf", mime="application/pdf")
                        
                        with col_mcq2:
                            st.download_button("📥 Download MCQs as Word (.docx)", data=generate_docx_bytes("Extracted MCQs & Answer Key", output_text), file_name="Extracted_MCQs.docx", mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")

                    except Exception as e:
                        st.error(f"Error processing upload: {e}")
