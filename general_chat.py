import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
import speech_recognition as sr

def show_chat():
    load_dotenv()
    
    # Page configuration
    st.set_page_config(page_title="AI Interview Coach", page_icon="💫", layout="wide")

    # Load external CSS
    try:
        with open("styles.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except:
        pass

    # ---------------- COSMIC HEADER ----------------
    col_head1, col_head2 = st.columns([8, 2])
    with col_head1:
        st.markdown('<div style="margin-bottom: 2rem;"><div style="font-size: 2rem; font-weight: 800; font-family: Orbitron, sans-serif;"><span class="cosmic-gradient-text">AI chat bot</span></div></div>', unsafe_allow_html=True)
    
    with col_head2:
        st.markdown('<div style="margin-top: 0.5rem;"></div>', unsafe_allow_html=True)  # Push button down
        if st.button("⬅ BACK TO HOME", use_container_width=True):
            st.session_state.page = "landing"
            st.rerun()

    # ---------------- SESSION STATE ----------------
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "voice_text" not in st.session_state:
        st.session_state.voice_text = ""

    # Initialize Groq client
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = "llama-3.1-8b-instant"
    
    try:
        client = Groq(api_key=GROQ_API_KEY)
    except Exception as e:
        st.error(f"Error initializing Groq client: {e}")
        return

    # ---------------- CHAT DISPLAY ----------------
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin-bottom: 1.5rem;">
                        <div class="glass-card" style="padding: 1.5rem 2rem; border-radius: 20px 20px 4px 20px; max-width: 75%; background: linear-gradient(135deg, #6B2E9E, #8B42C4); border: 2px solid rgba(139, 66, 196, 0.6); box-shadow: 0 8px 32px rgba(107, 46, 158, 0.4);">
                            <div style="color: #FFFFFF; font-size: 1.05rem; line-height: 1.6; font-weight: 500; text-shadow: 0 1px 2px rgba(0,0,0,0.2);">{msg["content"]}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin-bottom: 1.5rem;">
                        <div class="glass-card" style="padding: 1.5rem 2rem; border-radius: 20px 20px 20px 4px; max-width: 75%; border: 2px solid rgba(6, 182, 212, 0.4); box-shadow: 0 8px 32px rgba(6, 182, 212, 0.2);">
                            <div style="color: #FFFFFF; font-size: 1.05rem; line-height: 1.7; font-weight: 400;">{msg["content"]}</div>
                        </div>
                    </div>
                """, unsafe_allow_html=True)

    # ---------------- INPUT AREA ----------------
    st.markdown("""<div style="height: 100px;"></div>""", unsafe_allow_html=True) # Spacer
    
    input_cols = st.columns([1, 10, 1])
    
    with input_cols[0]:
        mic = st.button("🎙️", help="Start Voice Input", use_container_width=True)
    
    with input_cols[1]:
        typed = st.chat_input("Message your AI Coach...")
    
    with input_cols[2]:
        if st.button("✨", help="Enhance Answer", use_container_width=True):
            pass

    # ---------------- CHAT LOGIC ----------------
    if mic:
        r = sr.Recognizer()
        with sr.Microphone() as source:
            with st.spinner("🎙️ AI Listening..."):
                try:
                    audio = r.listen(source, timeout=5)
                    st.session_state.voice_text = r.recognize_google(audio)
                except:
                    st.error("Audio not captured. Please try again.")

    prompt = typed or st.session_state.voice_text
    
    if prompt:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.voice_text = ""
        
        # Get AI response
        try:
            with st.spinner("🌌 Cosmic AI thinking..."):
                chat_completion = client.chat.completions.create(
                    messages=[
                        {"role": "system", "content": "You are an expert AI interview coach. Help users prepare for technical interviews with detailed, accurate, and encouraging responses."},
                        *st.session_state.messages
                    ],
                    model=MODEL,
                    temperature=0.7,
                    max_tokens=1024
                )
                
                ai_response = chat_completion.choices[0].message.content
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
                
        except Exception as e:
            st.error(f"Error getting AI response: {e}")
        
        st.rerun()
