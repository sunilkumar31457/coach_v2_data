import streamlit as st
import pytesseract
from PIL import Image
import os
import json
from dotenv import load_dotenv
from groq import Groq

def show_jd_interview():
    load_dotenv()
    
    # ---------------- CONFIG ----------------
    # Page config is handled in app.py or implicitly. We don't set it here to avoid conflicts.
    
    # Load external CSS
    try:
        with open("styles.css") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

    # ---------------- SETTINGS & API KEY ----------------
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        with st.expander("API Settings", expanded=False):
            files_api_key = os.getenv("GROQ_API_KEY", "")
            user_api_key = st.text_input("Groq API Key", value=files_api_key, type="password", help="Enter a valid Groq API Key. Get one for free at console.groq.com")
            if user_api_key and user_api_key != files_api_key:
                os.environ["GROQ_API_KEY"] = user_api_key
                # Optional: Update .env file if possible, but runtime env var is enough for session
    
    # Initialize Groq Client
    GROQ_API_KEY = user_api_key or os.getenv("GROQ_API_KEY")
    client = None
    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
        except Exception as e:
            st.sidebar.error(f"Invalid Key: {e}")

    # ---------------- HEADER ----------------
    col_head1, col_head2 = st.columns([8, 2])
    with col_head1:
        st.markdown("""
            <div style="margin-bottom: 2rem;">
                <div style="font-size: 2rem; font-weight: 800; font-family: 'Orbitron'; display: flex; align-items: center; gap: 10px;">
                    <span class="material-symbols-rounded" style="font-size: 2.5rem; background: linear-gradient(135deg, #F59E0B, #D946EF); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">business_center</span>
                    <span class="cosmic-gradient-text">JD Mock Interview</span>
                </div>
                <div style="font-size: 0.9rem; color: #C7D2FE; font-weight: 500; letter-spacing: 0.1em; display: flex; align-items: center; gap: 5px;">
                     <span class="material-symbols-rounded" style="font-size: 1.2rem;">psychology</span> AI INTERVIEW SIMULATION
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_head2:
        st.markdown('<div style="margin-top: 0.5rem;"></div>', unsafe_allow_html=True)
        if st.button("⬅ BACK TO HOME", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

    # ---------------- SESSION STATE ----------------
    if "jd_text" not in st.session_state:
        st.session_state.jd_text = ""
    if "questions" not in st.session_state:
        st.session_state.questions = []
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "current_q" not in st.session_state:
        st.session_state.current_q = 0
    if "interview_active" not in st.session_state:
        st.session_state.interview_active = False
    if "jd_analysis" not in st.session_state:
        st.session_state.jd_analysis = ""

    # ---------------- FUNCTIONS ----------------
    # ---------------- FUNCTIONS ----------------
    import base64
    from io import BytesIO

    def configure_tesseract():
        """Attempt to find Tesseract executable in common Windows paths and user-provided directory."""
        # 1. Check specific user path first (Recursive search in case it's a build dir)
        user_path = r"C:\Users\B SUNIL KUMAR\Downloads\tesseract-main\tesseract-main"
        if os.path.exists(user_path):
            if os.path.isfile(user_path) and user_path.lower().endswith("tesseract.exe"):
                 pytesseract.pytesseract.tesseract_cmd = user_path
                 return True
            # Recursive search for tesseract.exe within the user directory
            for root, dirs, files in os.walk(user_path):
                if "tesseract.exe" in files:
                    found_path = os.path.join(root, "tesseract.exe")
                    pytesseract.pytesseract.tesseract_cmd = found_path
                    return True

        # 2. Check common installation paths
        common_paths = [
            r"C:\Program Files\Tesseract-OCR\tesseract.exe",
            r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
            r"C:\Users\B SUNIL KUMAR\AppData\Local\Tesseract-OCR\tesseract.exe",
            r"C:\Users\B SUNIL KUMAR\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"
        ]
        for path in common_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                return True
        return False

    def encode_image(image):
        if image.mode != 'RGB':
            image = image.convert('RGB')
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode('utf-8')

    def extract_text_with_groq(image, client_instance):
        """Use Groq Vision model to extract text. Supports 90b and 11b models."""
        if not client_instance:
             raise Exception("Groq API Key missing for Vision OCR.")
        
        base64_image = encode_image(image)
        
        # candidate models in order of preference (using exact IDs from user's access list)
        candidate_models = [
            "meta-llama/llama-4-scout-17b-16e-instruct",
            "meta-llama/llama-4-maverick-17b-128e-instruct",
            "llama-3.2-11b-vision-preview", # Keeping as fallback just in case
        ]

        last_exception = None
        for model in candidate_models:
            try:
                completion = client_instance.chat.completions.create(
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Extract all the text from this Job Description image exactly as it appears. Output ONLY the text content, no conversational filler."},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    temperature=0.0,
                    max_tokens=2048
                )
                return completion.choices[0].message.content
            except Exception as e:
                last_exception = e
                continue # Try next model
        
        # If all failed
        raise last_exception

    def extract_text_from_image(image):
        # 1. Try Groq Vision First (Serverless, No Install, High Accuracy)
        vision_key = os.getenv("GROQ_API_KEY")
        if vision_key:
             try:
                 temp_client = Groq(api_key=vision_key)
                 return extract_text_with_groq(image, temp_client)
             except Exception as vision_error:
                 if "401" in str(vision_error):
                     st.warning("⚠️ Vision OCR Failed: Invalid API Key. Please update it in the Sidebar Settings.")
                 else:
                     st.warning(f"Vision OCR failed (Switching to Tesseract): {vision_error}")
                 # Fall through to Tesseract
        
        # 2. Try Tesseract as Backup
        try:
            configure_tesseract()
            return pytesseract.image_to_string(image, lang="eng")
        except Exception:
            raise Exception("OCR Failed: Groq Vision Model ineffective AND Tesseract not installed.\n\n👉 ACTION: Update your API Key in the Sidebar Settings, or use 'Paste Text' mode.")
    
    def parse_questions_list(text):
        lines = text.split("\n")
        questions = []
        for line in lines:
            line = line.strip()
            if not line:
                continue
            # Capture numbered or bulleted questions
            if line[0].isdigit() or line.startswith("-"):
                clean = line.lstrip("0123456789.- ").strip()
                if clean:
                    questions.append(clean)
        return questions

    # ---------------- MAIN CONTENT ----------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    # Input Section
    st.markdown('### <span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: var(--nebula-pink);">upload_file</span> Job Description Input', unsafe_allow_html=True)
    
    input_mode = st.radio("Choose Input Type:", ["Upload Image", "Paste Text"], horizontal=True)
    
    # Force radio text color
    st.markdown("""
    <style>
    div[role="radiogroup"] label { color: white !important; font-weight: 600; }
    </style>
    """, unsafe_allow_html=True)

    if input_mode == "Upload Image":
        uploaded_file = st.file_uploader(
            "📎 Upload JD (Image, PDF, DOCX, JSON, TXT, etc.)",
            type=["png", "jpg", "jpeg", "pdf", "docx", "doc", "txt", "json", "csv", "md", "html"],
            help="Supported: Images, PDF, Word, JSON, Text, CSV, Markdown"
        )
        if uploaded_file:
            file_type = uploaded_file.name.split('.')[-1].lower()
            
            # Check if it's an image or document
            if file_type in ["png", "jpg", "jpeg"]:
                # Image processing with OCR
                img = Image.open(uploaded_file)
                st.image(img, caption="Target Document", use_container_width=True)
                if st.button("🔍 Extract & Analyze JD", use_container_width=True):
                    with st.spinner("Extracting text from image..."):
                        try:
                            extracted = extract_text_from_image(img)
                            st.session_state.jd_text = extracted
                            st.success("JD Extracted Successfully!")
                        except Exception as e:
                            if "Tesseract" in str(e) or "OCR Failed" in str(e):
                                st.warning("⚠️ Critical OCR Failure")
                                st.info("Both AI Vision and Local Tesseract failed. Please copy-paste your JD text using the 'Paste Text' option above.")
                            else:
                                st.error(f"Analysis Error: {e}")
            
            elif file_type in ["pdf", "docx", "doc", "txt", "json", "csv", "md", "html"]:
                # Document processing (direct text extraction or OCR fallback)
                st.info(f"📄 Document detected: {uploaded_file.name}")
                if st.button("📖 Extract Text from Document", use_container_width=True):
                    with st.spinner("Processing document..."):
                        try:
                            jd_text = ""
                            
                            # --- JSON Handling ---
                            if file_type == "json":
                                try:
                                    import json
                                    data = json.load(uploaded_file)
                                    # Convert JSON to a readable string format
                                    jd_text = json.dumps(data, indent=2)
                                except Exception as e:
                                    st.error(f"JSON Error: {e}")

                            # --- PDF Handling (Text + OCR Fallback) ---
                            elif file_type == "pdf":
                                try:
                                    import fitz  # PyMuPDF
                                    
                                    # Write bytes to temp file because fitz needs a filename or bytes stream
                                    # fitz.open(stream=..., filetype="pdf") works
                                    doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                                    
                                    for page_num, page in enumerate(doc):
                                        text = page.get_text()
                                        
                                        # Check if page is likely scanned (very little text)
                                        if len(text.strip()) < 50:
                                            st.info(f"Page {page_num+1} appears scanned. Applying OCR...")
                                            # Render page to image
                                            pix = page.get_pixmap(dpi=200)
                                            # Convert to PIL Image
                                            img_data = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                                            # Use existing extraction function
                                            text = extract_text_from_image(img_data)
                                            jd_text += f"\n--- Page {page_num+1} (OCR) ---\n" + text
                                        else:
                                            jd_text += text
                                            
                                except ImportError:
                                    st.error("PyMuPDF (fitz) is missing. Please ensure requirements.docx is installed.")
                                except Exception as e:
                                    st.error(f"PDF Error: {e}")

                            # --- Word Document ---
                            elif file_type in ["docx", "doc"]:
                                try:
                                    import docx
                                    doc = docx.Document(uploaded_file)
                                    for para in doc.paragraphs:
                                        jd_text += para.text + "\n"
                                except ImportError:
                                    st.error("python-docx library is missing.")

                            # --- Generic Text Handling (TXT, CSV, MD, HTML) ---
                            else:
                                try:
                                    # Reset pointer just in case
                                    uploaded_file.seek(0)
                                    jd_text = uploaded_file.read().decode("utf-8")
                                except Exception:
                                    st.warning("Could not decode as UTF-8. Trying fallback encoding...")
                                    uploaded_file.seek(0)
                                    jd_text = uploaded_file.read().decode("latin-1")
                            
                            # Final Check
                            if jd_text.strip():
                                st.session_state.jd_text = jd_text
                                st.success("✅ JD Text Extracted Successfully!")
                            else:
                                st.warning("No text extracted. The file might be empty or unreadable.")
                        except Exception as e:
                            st.error(f"Document extraction error: {str(e)}")
                        
    elif input_mode == "Paste Text":
        jd_input = st.text_area("Paste Job Description", height=200, value=st.session_state.jd_text)
        if st.button("Save JD", use_container_width=True):
            st.session_state.jd_text = jd_input
            st.success("JD Saved!")

    # Display Extracted Text (Optional but helpful)
    # Old expander removed to show text prominently in the next section
    pass
    
    st.markdown("</div>", unsafe_allow_html=True) # End Input Card
    
    # ---------------- REVIEW & INTERVIEW SETUP ----------------
    if st.session_state.jd_text and not st.session_state.interview_active:
        # Save to JSON whenever we have text
        from text_utils import save_extracted_text_to_json, chunk_text_meaningfully
        save_extracted_text_to_json(st.session_state.jd_text)
        
        # Create chunks
        chunks = chunk_text_meaningfully(st.session_state.jd_text)
        
        # Update jd_text to reflect the segmented format (visual improvement)
        # We join chunks with double newlines to separate them in the text area
        formatted_text = "\n\n".join(chunks)
        if formatted_text != st.session_state.jd_text:
             st.session_state.jd_text = formatted_text
             st.rerun() 
        
        st.markdown('<div class="glass-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
        
        # 1. Review Section
        st.markdown('### <span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: var(--electric-violet);">rate_review</span> Review & Edit Job Description', unsafe_allow_html=True)
        
        # Display Chunks
        if chunks:
             st.markdown("#### <span style='font-size: 0.9rem; color: #94A3B8;'>Processed Segments (Read-Only Preview)</span>", unsafe_allow_html=True)
             for i, chunk in enumerate(chunks):
                 st.markdown(f"""
                 <div style="background: rgba(255, 255, 255, 0.05); padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem; border-left: 3px solid var(--electric-violet); white-space: pre-wrap;">
                    <small style="color: #64748B; display: block; margin-bottom: 4px;">Segment {i+1}</small>
                    <span style="color: #E2E8F0;">{chunk}</span>
                 </div>
                 """, unsafe_allow_html=True)
                 
        st.info("👇 Please check the full extracted text below. Content can be edited if needed.")
        
        # Editable Text Area - Critical for User Verification
        # Custom CSS to force white caret
        st.markdown("""
        <style>
        textarea {
            caret-color: white !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        updated_jd = st.text_area(
            "Extracted Job Description",
            value=st.session_state.jd_text,
            height=300,
            key="jd_editor"
        )
        
        # Sync edits back to session state
        if updated_jd != st.session_state.jd_text:
            st.session_state.jd_text = updated_jd

        st.markdown("---")
        
        # 2. Analysis Section
        st.markdown('### <span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: var(--stellar-blue);">analytics</span> JD Analysis', unsafe_allow_html=True)
        
        if st.button("🔍 Analyze Job Description", use_container_width=True):
            if not client:
                st.error("Groq API Key missing.")
            else:
                with st.spinner("AI analyzing job requirements..."):
                    try:
                        analysis_prompt = f"""
                        Analyze the following Job Description and provide a structured summary in Markdown format.
                        Focus on:
                        1. Job Title & Role Summary
                        2. Key Responsibilities (Bullet points)
                        3. Required Skills & Technologies
                        4. Experience & Qualifications
                        5. Key Benefits/Perks (if mentioned)
                        
                        Job Description:
                        {st.session_state.jd_text}
                        """
                        
                        completion = client.chat.completions.create(
                            messages=[{"role": "system", "content": "You are an expert HR Analyst."}, {"role": "user", "content": analysis_prompt}],
                            model="llama-3.1-8b-instant"
                        )
                        st.session_state.jd_analysis = completion.choices[0].message.content
                        st.session_state.interview_active = False # Reset interview state
                            
                    except Exception as e:
                        st.error(f"Analysis Error: {e}")

        # Display Analysis Result
        if st.session_state.get("jd_analysis"):
            st.markdown("---")
            
            # Custom CSS for Analysis Card
            st.markdown("""
                <style>
                .jd-analysis-card {
                    background: rgba(16, 20, 45, 0.95);
                    padding: 2rem;
                    border-radius: 16px;
                    border: 1px solid var(--aurora-cyan);
                    box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
                    margin-top: 1rem;
                    color: #E2E8F0; /* Default text color: Light Gray */
                }
                .jd-analysis-card h1, .jd-analysis-card h2, .jd-analysis-card h3 {
                    color: #F8FAFC !important; /* Headers: White */
                    font-family: 'Orbitron', sans-serif;
                    margin-top: 1.5rem;
                    margin-bottom: 0.8rem;
                    text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
                }
                .jd-analysis-card strong {
                    color: var(--stellar-gold) !important; /* Bold text: Gold */
                }
                .jd-analysis-card ul, .jd-analysis-card ol {
                    margin-left: 1.5rem;
                }
                .jd-analysis-card li {
                    color: #CBD5E1 !important; /* List items: Light Blue-Gray */
                    font-size: 1.05rem;
                    margin-bottom: 0.5rem;
                    line-height: 1.6;
                }
                .jd-analysis-card p {
                    color: #E2E8F0 !important;
                    line-height: 1.6;
                    font-size: 1.05rem;
                }
                </style>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div class="jd-analysis-card">
                    {st.session_state.jd_analysis}
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # ---------------- INTERVIEW SETUP SECTION ----------------
            if not st.session_state.interview_active:
                st.markdown("---")
                
                # Custom CSS for Interview Setup
                st.markdown("""
                <style>
                .interview-setup-card {
                    background: linear-gradient(135deg, rgba(139, 66, 196, 0.1), rgba(67, 233, 178, 0.1));
                    border: 1px solid var(--nebula-violet);
                    border-radius: 20px;
                    padding: 2rem;
                    margin-top: 1rem;
                    text-align: center;
                }
                .setup-title {
                    font-size: 1.8rem;
                    font-weight: 700;
                    color: #FFFFFF !important;
                    margin-bottom: 1rem;
                    font-family: 'Orbitron', sans-serif;
                    text-shadow: 0 0 20px rgba(139, 66, 196, 0.6);
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.markdown('<div class="interview-setup-card">', unsafe_allow_html=True)
                st.markdown('<div class="setup-title">⚙️ Ready for Interview?</div>', unsafe_allow_html=True)
                
                # Slider for number of questions
                num_questions = st.slider(
                    "Number of Questions",
                    min_value=3,
                    max_value=10,
                    value=5,
                    key="interview_question_count",
                    help="Choose how many interview questions you want to practice"
                )
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                if st.button("🚀 START MOCK INTERVIEW", use_container_width=True, type="primary"):
                    if not client:
                        st.error("Groq API Client not initialized.")
                    else:
                        with st.spinner(f"🤖 AI is generating {num_questions} interview questions..."):
                            try:
                                # Generate Questions
                                question_prompt = f"""
                                Based on this job description, generate exactly {num_questions} interview questions:
                                {st.session_state.jd_text}
                                
                                Return only the questions, one per line, numbered 1-{num_questions}.
                                Focus on technical skills, behavioral scenarios, and role-specific expertise.
                                """
                                
                                completion = client.chat.completions.create(
                                    messages=[
                                        {"role": "system", "content": "You are an expert technical recruiter."},
                                        {"role": "user", "content": question_prompt}
                                    ],
                                    model="llama-3.1-8b-instant",
                                )
                                
                                raw_questions = completion.choices[0].message.content
                                # Parse questions (split by newline, clean up)
                                questions = [q.strip() for q in raw_questions.split('\n') if q.strip() and any(c.isalpha() for c in q)]
                                # Remove numbering if present
                                questions = [q.split('.', 1)[-1].strip() if q[0].isdigit() else q for q in questions]
                                
                                if len(questions) >= num_questions - 1:  # Allow slight variation
                                    st.session_state.questions = questions[:num_questions]
                                    st.session_state.answers = []
                                    st.session_state.current_q = 0
                                    st.session_state.interview_active = True
                                    st.rerun()
                                else:
                                    st.error("Failed to generate enough questions. Please try again.")
                                    
                            except Exception as e:
                                st.error(f"Question Generation Error: {str(e)}")
                
                st.markdown('</div>', unsafe_allow_html=True)
            
            
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- LIVE INTERVIEW MODE ----------------
    if st.session_state.interview_active and st.session_state.questions:
        st.markdown('<div class="glass-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
        
        total_qs = len(st.session_state.questions)
        q_idx = st.session_state.current_q
        
        if q_idx < total_qs:
            # Progress
            progress = (q_idx) / total_qs
            st.progress(progress)
            
            st.markdown(f"#### Question {q_idx + 1} of {total_qs}")
            st.markdown(f"""
                <div style="background: rgba(255,255,255,0.1); padding: 1.5rem; border-radius: 12px; border-left: 4px solid var(--aurora-cyan); margin-bottom: 1.5rem;">
                    <span style="font-size: 1.2rem; font-weight: 500; color: white;">{st.session_state.questions[q_idx]}</span>
                </div>
            """, unsafe_allow_html=True)
            
            user_ans = st.text_area("Your Answer", height=150, key=f"ans_{q_idx}")
            
            # Buttons in columns for Submit and Skip
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("✅ Submit Answer", use_container_width=True, type="primary"):
                    if not user_ans:
                        st.warning("Please type an answer.")
                    else:
                        st.session_state.answers.append(user_ans)
                        st.session_state.current_q += 1
                        st.rerun()
            
            with col2:
                if st.button("⏭️ Skip Question", use_container_width=True):
                    st.session_state.answers.append("")  # Record as skipped
                    st.session_state.current_q += 1
                    st.rerun()
        else:
            # ---------------- FEEDBACK GENERATION ----------------
            st.markdown('### <span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: var(--stellar-gold);">fact_check</span> Interview Evaluation', unsafe_allow_html=True)
            
            # High-Contrast Feedback CSS
            st.markdown("""
                <style>
                .feedback-card {
                    background: rgba(16, 20, 45, 0.95);
                    padding: 2rem;
                    border-radius: 16px;
                    border: 1px solid var(--stellar-gold);
                    box-shadow: 0 0 20px rgba(255, 215, 0, 0.15);
                    margin-top: 1rem;
                    color: #E2E8F0;
                }
                .feedback-card h1, .feedback-card h2, .feedback-card h3, .feedback-card h4 {
                    color: #F8FAFC !important;
                    font-family: 'Orbitron', sans-serif;
                    margin-top: 1.5rem;
                    margin-bottom: 0.8rem;
                    text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
                }
                .feedback-card strong {
                    color: var(--stellar-gold) !important;
                }
                .feedback-card ul, .feedback-card ol {
                    margin-left: 1.5rem;
                }
                .feedback-card li {
                    color: #CBD5E1 !important;
                    font-size: 1.05rem;
                    margin-bottom: 0.5rem;
                    line-height: 1.6;
                }
                .feedback-card p {
                    color: #E2E8F0 !important;
                    line-height: 1.6;
                    font-size: 1.05rem;
                }
                </style>
            """, unsafe_allow_html=True)
            
            if "feedback" not in st.session_state:
                 with st.spinner("AI evaluating your performance..."):
                    try:
                        qa_pairs = list(zip(st.session_state.questions, st.session_state.answers))
                        feedback_prompt = f"""
                        You are a Hard-Nosed Interview Evaluator. 
                        
                        🎯 OBJECTIVE: Evaluate the candidate's performance based ONLY on the User's Answers.
                        
                        User's Actual Answers (The ONLY Source of Truth):
                        {qa_pairs}
                        
                        EVALUATION RULES:
                        1. SCORING SYSTEM (2 Marks Per Question): 
                           - Each individual question carries exactly 2 marks.
                           - Every SKIPPED or EMPTY answer MUST result in exactly 0/2 marks.
                           - Every ATTENDED answer must be scored from 0 to 2 (e.g., 0.5, 1.25, 2.0) based on how well it satisfies the requirement.
                           - MAX POSSIBLE SCORE = (Number of Questions * 2).
                        2. WEAKNESSES & GAPS: 
                           - Explicitly list every SKIPPED question as a major weakness/gap (0/2 marks).
                           - Explain that skipping critical questions significantly impacts the hiring decision.
                        3. DEMONSTRATED STRENGTHS: 
                           - Only extract strengths from questions the user actually ATTENDED.
                           - Show the mark awarded (e.g., 1.8/2) for each strength found.
                        4. NO ASSUMPTIONS: Do not grant marks for skills listed in the JD unless explicitly proved in an attended answer.
                        
                        Evaluation Format (Markdown):
                        ### **Overall performance Score**: [Total Marks Obtained] / [Max Possible Marks]
                        
                        #### **Score Breakdown**:
                        - Q1: [Score]/2
                        - Q2: [Score]/2
                        ... (for all questions)
                        
                        #### **Demonstrated Strengths (Attended Questions)**:
                        - [Strength description] (Evidence: [citation])
                        
                        #### **Gaps & Weaknesses (Skipped & Poor Answers)**:
                        - **Skipped Question [N]**: Major Gap - No evidence provided (0/2 Marks)
                        - [Other weaknesses]
                        
                        #### **Final Verdict**:
                        [Strict hiring decision based ONLY on the total marks and evidence]
                        """
                        
                        completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "You are a strictly objective auditor. You categorize skips as weaknesses and attended answers as potential strengths. You judge only what is written."},
                                {"role": "user", "content": feedback_prompt}
                            ],
                            model="llama-3.1-8b-instant",
                        )
                        
                        st.session_state.feedback = completion.choices[0].message.content
                    except Exception as e:
                        st.error(f"Feedback Error: {str(e)}")
            
            if "feedback" in st.session_state:
                 st.markdown(f"""
                     <div class="feedback-card">
                         {st.session_state.feedback}
                     </div>
                 """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🔄 Start New Interview"):
                 st.session_state.interview_active = False
                 st.session_state.questions = []
                 st.session_state.answers = []
                 st.session_state.current_q = 0
                 if "feedback" in st.session_state:
                     del st.session_state.feedback
                 st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
