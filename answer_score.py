import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import json

def show_answer_score():
    load_dotenv()
    
    # Page configuration
    st.set_page_config(page_title="Precision Scorer - Deep Cosmos", page_icon="🎯", layout="wide")

    # Load external CSS
    try:
        with open("styles.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

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
                    <span class="material-symbols-rounded" style="font-size: 2.5rem; background: linear-gradient(to right, #6B2E9E, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">track_changes</span>
                    <span class="cosmic-gradient-text">Precision Scorer</span>
                </div>
                <div style="font-size: 0.9rem; color: var(--text-nebula); font-weight: 500; letter-spacing: 0.1em; display: flex; align-items: center; gap: 5px;">
                     <span class="material-symbols-rounded" style="font-size: 1.2rem;">analytics</span> PERFORMANCE ANALYTICS
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
    
    st.markdown('### <span class="material-symbols-rounded" style="vertical-align: middle; margin-right: 8px; color: var(--aurora-cyan);">analytics</span> Analyze Performance', unsafe_allow_html=True)

    # Custom CSS for label visibility
    st.markdown("""
    <style>
    /* Force input labels to be bright white */
    [data-testid="stSelectbox"] label {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    [data-testid="stTextArea"] label {
        color: #FFFFFF !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
    }
    
    /* Ensure input text itself is readable */
    [data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        color: black !important;
    }
    textarea {
        font-size: 1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    role = st.selectbox(
        "Target Role",
        ["Software Developer", "Data Analyst", "ML Engineer", "HR Interview", "Product Manager", "General"]
    )

    answer = st.text_area("Provide your answer for analysis:", height=250, placeholder="Type or paste the answer you gave during practice...")

    if st.button("GENERATE SCORED FEEDBACK", use_container_width=True):
        if not client:
            st.error("Groq API Key not found! Please check .env file.")
        elif not answer.strip():
            st.warning("Input required for analysis.")
        else:
            with st.spinner("AI Evaluating..."):
                try:
                    completion = client.chat.completions.create(
                        messages=[
                            {
                                "role": "system", 
                                "content": f"You are an expert Interview Coach for {role} roles. Evaluate the candidate's answer. Return valid JSON only with keys: 'score' (0-100 integer), 'feedback' (string), 'better_answer' (string)."
                            },
                            {
                                "role": "user", 
                                "content": f"Candidate Answer: {answer}"
                            }
                        ],
                        model="llama-3.1-8b-instant",
                        response_format={"type": "json_object"}
                    )
                    
                    result = json.loads(completion.choices[0].message.content)
                    score = result.get('score', 0)
                    feedback = result.get('feedback', "No feedback provided.")
                    better_answer = result.get('better_answer', "")

                    st.success("Analysis Optimized")
                    
                    # Display Score
                    score_color = "#22C55E" if score >= 80 else "#EAB308" if score >= 60 else "#EF4444"
                    
                    st.markdown(f"""
                        <div style="border-left: 4px solid var(--primary-glow); padding-left: 1rem; margin-top: 1rem;">
                            <h4 style="color: {score_color};">Confidence Score: {score}%</h4>
                            <p style="color: #E2E8F0; font-size: 1.05rem;">{feedback}</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    if better_answer:
                        with st.expander("✨ View Suggested Answer"):
                            st.write(better_answer)

                except Exception as e:
                    st.error(f"Error Analyzing answer: {str(e)}")

    st.markdown("</div>", unsafe_allow_html=True)
