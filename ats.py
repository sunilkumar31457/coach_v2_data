import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import json
from io import BytesIO

# Fallback for PyPDF2
try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

def show_ats_score():
    load_dotenv()
    
    # Page configuration
    st.set_page_config(page_title="ATS Cosmic Scanner - Deep Cosmos", page_icon="🔍", layout="wide")

    # Load external CSS
    with open("styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

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
                    <span class="material-symbols-rounded" style="font-size: 2.5rem; background: -webkit-linear-gradient(45deg, #6B2E9E, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">rule_settings</span>
                    <span class="cosmic-gradient-text">ATS Scanner</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-nebula); font-weight: 500; letter-spacing: 0.1em; display: flex; align-items: center; gap: 5px;">
                    <span class="material-symbols-rounded" style="font-size: 1.2rem;">compare_arrows</span> COMPATIBILITY ANALYZER
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col_head2:
        st.markdown('<div style="margin-top: 0.5rem;"></div>', unsafe_allow_html=True)
        if st.button("⬅ BACK TO HOME", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

    # ---------------- MAIN CONTENT ----------------
    col_left, col_right = st.columns([6, 4])

    with col_left:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown('### <span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: var(--nebula-pink);">fact_check</span> Compatibility Check', unsafe_allow_html=True)
        
        # Custom CSS for file uploader visibility
        st.markdown("""
        <style>
        /* Text Area Label */
        [data-testid="stTextArea"] label {
            color: #FFFFFF !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.05em !important;
            text-shadow: 0 0 10px rgba(139, 66, 196, 0.3);
        }
        
        /* File Uploader Label */
        [data-testid="stFileUploader"] label {
            color: #FFFFFF !important;
            font-size: 1.1rem !important;
            font-weight: 700 !important;
        }
        
        /* File Uploader Content (Uploaded filename) */
        [data-testid="stFileUploader"] section {
            background: rgba(255, 255, 255, 0.05);
            border: 1px dashed rgba(255, 255, 255, 0.2);
            border-radius: 12px;
        }

        /* The Small text inside uploader "Drag and drop..." */
        [data-testid="stFileUploader"] small {
            color: #E2E8F0 !important;
            opacity: 0.8 !important;
        }

        /* The uploaded file name text - specific targeting */
        [data-testid="stFileUploader"] .uploadedFile {
            color: #FFFFFF !important;
            font-weight: 600 !important;
            background: rgba(10, 14, 39, 0.6) !important;
            border: 1px solid rgba(139, 66, 196, 0.3) !important;
            border-radius: 8px !important;
        }
        
        /* General text visibility in this block */
        .uploadedFileName, .stMarkdown p {
            color: #E2E8F0 !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Upload Document", type=["pdf"])
        job_role = st.text_area("Target Job Description", height=200, placeholder="Paste JD here to calibrate scores...")
        
        if st.button("EXECUTE ATS AUDIT", use_container_width=True):
            if not client:
                st.error("Groq API Key not found!")
            elif not PyPDF2:
                 st.error("PyPDF2 library is missing. Cannot process PDF. Please install PyPDF2.")
            elif not uploaded_file:
                st.warning("Please upload a resume first.")
            elif not job_role:
                st.warning("Please paste a Job Description.")
            else:
                with st.spinner("Analyzing Compatibility..."):
                    try:
                        # Extract Text from PDF
                        pdf_reader = PyPDF2.PdfReader(uploaded_file)
                        resume_text = ""
                        for page in pdf_reader.pages:
                            resume_text += page.extract_text()
                        


                        # Compare Resume vs JD using Groq
                        completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "You are an expert ATS System. Compare the candidate's resume with the provided Job Description. Return valid JSON only with keys: 'match_score' (0-100 integer) and 'analysis' (markdown string)."},
                                {"role": "user", "content": f"RESUME:\n{resume_text}\n\nJOB DESCRIPTION:\n{job_role}"}
                            ],
                            model="llama-3.1-8b-instant",
                            response_format={"type": "json_object"}
                        )
                        result_text = completion.choices[0].message.content
                        
                        # Extract Score and Analysis
                        try:
                            result_json = json.loads(result_text)
                            score = result_json.get("match_score", 0)
                            analysis_content = result_json.get("analysis", "No analysis provided.")
                                
                            st.session_state.ats_score = score
                            st.session_state.ats_analysis = analysis_content
                            st.success("ATS Scan Complete")
                            
                        except Exception as e:
                            st.error(f"Error parsing score: {e}")
                            st.session_state.ats_score = 0
                            st.session_state.ats_analysis = result_text
                            
                    except Exception as e:
                        st.error(f"Error during scan: {str(e)}")

        st.markdown("</div>", unsafe_allow_html=True)

    with col_right:
        st.markdown('<div class="glass-card" style="text-align: center; height: 100%;">', unsafe_allow_html=True)
        st.markdown('### <span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: var(--stellar-blue);">hub</span> Live Score', unsafe_allow_html=True)
        
        display_score = st.session_state.get("ats_score", 0)
        
        # Determine Color based on score
        if display_score >= 80:
             score_color = "#22C55E" # Green
             verdict = "OPTIMIZED FOR TIER 1"
        elif display_score >= 60:
             score_color = "#EAB308" # Yellow
             verdict = "MODERATE MATCH"
        else:
             score_color = "#EF4444" # Red
             verdict = "NEEDS IMPROVEMENT"
            
        # Circular Score Visualization
        st.markdown(f"""
            <div style="width: 200px; height: 200px; border-radius: 50%; border: 12px solid rgba(255,255,255,0.05); margin: 2rem auto; display: flex; align-items: center; justify-content: center; position: relative;">
                <div style="position: absolute; width: 100%; height: 100%; border-radius: 50%; border: 12px solid {score_color}; border-top-color: transparent; transform: rotate({3.6 * display_score}deg); transition: transform 1s ease-out;"></div>
                <div style="font-size: 3rem; font-weight: 800; color: #FFFFFF;">{display_score}%</div>
            </div>
            <div style="font-weight: 600; color: {score_color}; margin-bottom: 2rem; font-size: 1.2rem;">{verdict}</div>
        """, unsafe_allow_html=True)
        
        if st.session_state.get("ats_analysis"):
             st.markdown('<div style="text-align: left; margin-top: 1rem; padding: 1.5rem; border-top: 1px solid rgba(255,255,255,0.1); background: rgba(0,0,0,0.2); border-radius: 16px;">', unsafe_allow_html=True)
             st.markdown(f'<div style="color: #E0E7FF; font-size: 0.95rem; line-height: 1.6;">{st.session_state.ats_analysis}</div>', unsafe_allow_html=True)
             st.markdown("</div>", unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
