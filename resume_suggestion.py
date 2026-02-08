import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from io import BytesIO

try:
    import PyPDF2
except ImportError:
    st.error("PyPDF2 library not found. Please run `pip install PyPDF2`")
    PyPDF2 = None

def show_resume_suggestion():
    load_dotenv()
    
    # Page configuration
    st.set_page_config(page_title="Resume Optimizer - Deep Cosmos", page_icon="📝", layout="wide")

    # Load external CSS
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    # Initialize Session State
    if "resume_chat_history" not in st.session_state:
        st.session_state.resume_chat_history = []
    
    # Initialize Groq Client
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    client = None
    if GROQ_API_KEY:
        try:
            client = Groq(api_key=GROQ_API_KEY)
        except Exception as e:
            st.error(f"Error initializing Groq client: {e}")

    # ---------------- HEADER ----------------
    col_head1, col_head2 = st.columns([8, 2])
    with col_head1:
        st.markdown("""
            <div style="display: flex; flex-direction: column; gap: 0.5rem; margin-bottom: 2rem;">
                <div style="font-size: 2rem; font-weight: 800; font-family: 'Orbitron'; display: flex; align-items: center; gap: 10px;">
                    <span class="material-symbols-rounded" style="font-size: 2.5rem; background: linear-gradient(135deg, #FF6B6B, #4ECDC4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">contact_page</span>
                    <span class="cosmic-gradient-text">Resume Architect</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-nebula); font-weight: 500; letter-spacing: 0.1em; display: flex; align-items: center; gap: 5px;">
                     <span class="material-symbols-rounded" style="font-size: 1.2rem;">stars</span> STELLAR CAREER BUILDER
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_head2:
        st.markdown('<div style="margin-top: 0.5rem;"></div>', unsafe_allow_html=True)
        if st.button("⬅ BACK TO HOME", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

    # ---------------- MAIN CONTENT ----------------
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    
    st.markdown('### <span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: var(--electric-blue);">screen_search_desktop</span> Analyze Document', unsafe_allow_html=True)
    
    # Enhanced File Uploader Styling
    st.markdown("""
    <style>
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.03);
        border: 2px dashed var(--aurora-cyan);
        border-radius: 12px;
        padding: 1.5rem;
    }
    [data-testid="stFileUploader"] label {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stFileUploader"] small {
        color: #E2E8F0 !important;
        font-size: 0.9rem !important;
    }
    [data-testid="stFileUploader"] button {
        background: var(--electric-violet) !important;
        color: white !important;
        border: none !important;
        padding: 0.5rem 1rem !important;
        border-radius: 8px !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf", "docx", "doc", "txt"],
        help="Supported formats: PDF, DOCX, DOC, TXT",
        accept_multiple_files=False
    )

    if uploaded_file is not None:
        if st.button("GENERATE AUDIT REPORT", use_container_width=True):
                if not client:
                     st.error("Groq API Key not found!")
                else:
                    with st.spinner("AI Auditor at work..."):
                        try:
                            resume_text = ""
                            file_type = uploaded_file.name.split('.')[-1].lower()
                            
                            # Extract text based on file type
                            if file_type == "pdf":
                                if not PyPDF2:
                                    st.error("PyPDF2 library is missing. Run: `pip install PyPDF2`")
                                else:
                                    pdf_reader = PyPDF2.PdfReader(uploaded_file)
                                    for page in pdf_reader.pages:
                                        resume_text += page.extract_text()
                            
                            elif file_type == "txt":
                                # Read text file directly
                                resume_text = uploaded_file.read().decode("utf-8")
                            
                            elif file_type in ["docx", "doc"]:
                                try:
                                    import docx
                                    doc = docx.Document(uploaded_file)
                                    for para in doc.paragraphs:
                                        resume_text += para.text + "\n"
                                except ImportError:
                                    st.error("python-docx library is missing. Run: `pip install python-docx`")
                                except Exception as e:
                                    st.error(f"Error reading DOCX file: {str(e)}")
                            
                            if resume_text.strip():
                                st.session_state.resume_text = resume_text
                                
                                # AI Analysis
                                completion = client.chat.completions.create(
                                    messages=[
                                        {"role": "system", "content": "You are an expert Resume Reviewer and Career Coach. Audit the following resume text. Provide a score out of 100, list top strengths, list weaknesses, and provide 3 concrete improvement suggestions. Format output in clean Markdown."},
                                        {"role": "user", "content": resume_text}
                                    ],
                                    model="llama-3.1-8b-instant",
                                )
                            st.session_state.resume_analysis = completion.choices[0].message.content
                            st.success("Report Generated")
                        except Exception as e:
                            st.error(f"Error processing resume: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- ANALYSIS RESULTS ----------------
    if st.session_state.get("resume_analysis"):
        st.markdown('<div class="glass-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
        st.markdown('### <span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: var(--stellar-gold);">assessment</span> Architecture Report', unsafe_allow_html=True)
        
        # High-Contrast CSS for Report
        st.markdown("""
            <style>
            .resume-report-card {
                background: rgba(16, 20, 45, 0.95);
                padding: 2rem;
                border-radius: 16px;
                border: 1px solid var(--aurora-cyan);
                box-shadow: 0 0 20px rgba(0, 255, 255, 0.1);
                margin-top: 1rem;
                color: #E2E8F0;
            }
            .resume-report-card h1, .resume-report-card h2, .resume-report-card h3 {
                color: #F8FAFC !important;
                font-family: 'Orbitron', sans-serif;
                margin-top: 1.5rem;
                margin-bottom: 0.8rem;
                text-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
            }
            .resume-report-card strong {
                color: var(--stellar-gold) !important;
            }
            .resume-report-card ul, .resume-report-card ol {
                margin-left: 1.5rem;
            }
            .resume-report-card li {
                color: #CBD5E1 !important;
                font-size: 1.05rem;
                margin-bottom: 0.5rem;
                line-height: 1.6;
            }
            .resume-report-card p {
                color: #E2E8F0 !important;
                line-height: 1.6;
                font-size: 1.05rem;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="resume-report-card">
                {st.session_state.resume_analysis}
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

    # ---------------- CHAT WITH RESUME AI ----------------
    if st.session_state.get("resume_text"):
        # Custom CSS for Premium Pill-Styled Input
        st.markdown("""
        <style>
        /* Chat Container Styling */
        .chat-glass-card {
            background: rgba(16, 20, 45, 0.8);
            border: 1px solid rgba(0, 255, 255, 0.2);
            border-radius: 20px;
            padding: 2rem;
            margin-top: 2rem;
            box-shadow: 0 8px 32px rgba(0, 255, 255, 0.1);
        }
        
        /* Pill-Styled Text Input */
        div[data-testid="stTextInput"] input {
            background: rgba(255, 255, 255, 0.05) !important;
            border: 2px solid var(--aurora-cyan) !important;
            border-radius: 50px !important;
            color: white !important;
            padding: 1rem 1.5rem !important;
            font-size: 1rem !important;
            caret-color: white !important;
            box-shadow: 0 0 20px rgba(0, 255, 255, 0.2) !important;
            transition: all 0.3s ease !important;
        }
        
        div[data-testid="stTextInput"] input:focus {
            border-color: var(--electric-violet) !important;
            box-shadow: 0 0 30px rgba(139, 66, 196, 0.4) !important;
            outline: none !important;
        }
        
        div[data-testid="stTextInput"] input::placeholder {
            color: rgba(255, 255, 255, 0.4) !important;
        }
        
        /* Chat Message Bubbles */
        .chat-message {
            margin: 1rem 0;
            animation: fadeIn 0.3s ease;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
        """, unsafe_allow_html=True)

        st.markdown('<div class="glass-card" style="margin-top: 2rem;">', unsafe_allow_html=True)
        st.markdown('### <span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: var(--nebula-violet);">forum</span> Chat with Resume AI', unsafe_allow_html=True)
        st.markdown("<div style='margin-bottom: 1.5rem; color: #C7D2FE; font-size: 0.95rem;'>💬 Ask questions to improve your resume sections, rephrase bullets, or get career advice.</div>", unsafe_allow_html=True)
        
        # Display chat history
        for msg in st.session_state.resume_chat_history:
            role_color = "#8B42C4" if msg["role"] == "user" else "#06B6D4"
            align = "flex-end" if msg["role"] == "user" else "flex-start"
            
            st.markdown(f"""
                <div class="chat-message" style="display: flex; justify-content: {align};">
                    <div style="background: {role_color}30; padding: 1rem 1.25rem; border-radius: 18px; max-width: 75%; border: 1px solid {role_color}50; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.2);">
                        {msg["content"]}
                    </div>
                </div>
            """, unsafe_allow_html=True)

        # Chat Input Handler
        def handle_chat():
            user_input = st.session_state.get("resume_chat_input", "").strip()
            if user_input and client:
                st.session_state.resume_chat_history.append({"role": "user", "content": user_input})
                
                try:
                    context_messages = [
                        {"role": "system", "content": f"You are an expert Resume Coach. Here is the user's resume:\n\n{st.session_state.resume_text}\n\nProvide specific, actionable advice."},
                        *st.session_state.resume_chat_history
                    ]
                    
                    completion = client.chat.completions.create(
                        messages=context_messages,
                        model="llama-3.1-8b-instant",
                    )
                    
                    response = completion.choices[0].message.content
                    st.session_state.resume_chat_history.append({"role": "assistant", "content": response})
                    st.session_state.resume_chat_input = ""  # Clear input
                    st.rerun()
                except Exception as e:
                    st.error(f"Chat Error: {str(e)}")

        # Premium Pill Input
        st.text_input(
            "Chat Input",
            key="resume_chat_input",
            on_change=handle_chat,
            label_visibility="collapsed",
            placeholder="✨ Type your question and press Enter..."
        )
        
        st.markdown("</div>", unsafe_allow_html=True)
