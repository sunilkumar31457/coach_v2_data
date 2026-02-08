import streamlit as st
from landing_page import show_landing
from general_chat import show_chat
from ocr_jd import show_jd_interview
from resume_suggestion import show_resume_suggestion
from ats import show_ats_score
from answer_score import show_answer_score



# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "landing"

# Sync with URL query params
params = st.query_params
if "page" in params:
    st.session_state.page = params["page"]

# Navigation Logic
if st.session_state.page == "chat":
    show_chat()

elif st.session_state.page == "landing":
    show_landing()

elif st.session_state.page == "jd":
    show_jd_interview()

elif st.session_state.page == "resume":
    show_resume_suggestion()

elif st.session_state.page == "ats":
    show_ats_score()

elif st.session_state.page == "score":
    show_answer_score()

else:
    st.write(f"Page {st.session_state.page} is coming soon!")
    if st.button("Back to Home"):
        st.session_state.page = "landing"
        st.rerun()
