import streamlit as st

def show_landing():
    # Page configuration
    st.set_page_config(
        page_title="AI Interview Coach - Ultra Cosmos",
        page_icon="🌌",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Load CSS
    try:
        with open("styles.css", "r", encoding="utf-8") as f:
            css_content = f.read()
            st.markdown(f"<style>{css_content}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"CSS Error: {e}")

    # Header using columns
    col_h1, col_h2 = st.columns([3, 1])
    with col_h1:
        st.markdown('<div style="font-size: 2.4rem; font-weight: 900; font-family: Orbitron, sans-serif; letter-spacing: 0.12em; display: flex; align-items: center; gap: 15px;"><span class="material-symbols-rounded" style="font-size: 3rem; color: #D946EF;">rocket_launch</span> <span class="cosmic-gradient-text">AI INTERVIEW COACH</span></div>', unsafe_allow_html=True)
    with col_h2:
        st.markdown('<div style="text-align: right;"><div style="display: inline-block; font-size: 0.9rem; color: #22D3EE; font-weight: 700; margin-right: 1rem; display: inline-flex; align-items: center; gap: 5px;"><span class="material-symbols-rounded" style="font-size: 1.2rem; color: #F59E0B;">verified_user</span> ULTRA ACCESS</div><div style="display: inline-block; width: 48px; height: 48px; background: linear-gradient(135deg, #6B2E9E, #3B82F6); border-radius: 50%; box-shadow: 0 0 35px rgba(107, 46, 158, 0.9); vertical-align: middle;"></div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Hero Section - Opening
    st.markdown("""
<div class="glass-card" style="margin-bottom: 3.5rem; text-align: center; position: relative; overflow: hidden; padding: 5rem 3rem 2rem 3rem;">
<div style="position: absolute; top: -40%; right: -15%; width: 500px; height: 500px; background: radial-gradient(circle, rgba(107, 46, 158, 0.35) 0%, transparent 65%); filter: blur(70px);"></div>
<div style="position: absolute; bottom: -40%; left: -15%; width: 450px; height: 450px; background: radial-gradient(circle, rgba(59, 130, 246, 0.3) 0%, transparent 65%); filter: blur(60px);"></div>
<div style="position: relative; z-index: 2;">
<h1 style="font-size: 4.5rem; line-height: 1.1; margin-bottom: 1.8rem; font-family: Orbitron, sans-serif; font-weight: 900;">Master Interviews<br/><span class="cosmic-gradient-text" style="font-size: 5rem;">Among the Stars</span></h1>
<p style="font-size: 1.35rem; color: #C7D2FE; max-width: 750px; margin: 0 auto 2.5rem auto; line-height: 1.8;">Elevate your interview preparation with AI-powered simulations</p>
</div>
    """, unsafe_allow_html=True)

    # Navigation Buttons INSIDE Hero
    btn_cols = st.columns(5)
    pages = ["chat", "jd", "resume", "ats", "score"]
    labels = ["LIVE CHAT", "JD ANALYZER", "RESUME AI", "ATS AUDIT", "SCORER"]
    
    for i, col in enumerate(btn_cols):
        with col:
            if st.button(labels[i], key=f"nav_{pages[i]}", use_container_width=True):
                st.session_state.page = pages[i]
                st.rerun()
    
    # Close Hero Section - AFTER buttons
    st.markdown("</div>", unsafe_allow_html=True)


    # Section Header
    st.markdown('<div style="margin: 1.5rem 0; text-align: center;"><h2 style="font-size: 2rem; margin-bottom: 0.8rem; font-family: Orbitron, sans-serif; font-weight: 800;"><span class="cosmic-gradient-text">ELITE COMPANY TRAINING</span></h2><p style="color: #C7D2FE; font-size: 1rem;">Tailored interview simulations for tier-1 tech positions</p></div>', unsafe_allow_html=True)

    # Role Cards
    col1, col2 = st.columns(2, gap="medium")

    with col1:
        st.markdown("""
<div class="glass-card" style="padding: 2rem; position: relative;">
<div style="position: absolute; top: 20px; right: 20px;"><div style="background: rgba(107, 46, 158, 0.35); color: #C7D2FE; padding: 6px 16px; border-radius: 999px; font-size: 0.75rem; font-weight: 800; border: 2px solid rgba(139, 66, 196, 0.6); letter-spacing: 0.15em;">TIER 1</div></div>
<div style="font-size: 1.8rem; font-weight: 900; color: white; margin-bottom: 0.8rem; font-family: Orbitron, sans-serif;">Frontend Architect</div>
<div style="font-size: 1rem; color: #22D3EE; font-weight: 700; margin-bottom: 1.5rem; letter-spacing: 0.05em;">FAANG LEVEL PREP</div>
<div style="color: #C7D2FE; font-size: 0.95rem; margin-bottom: 1.5rem; line-height: 1.6;">Advanced React patterns, System Design, Browser internals, Performance at scale</div>
<div style="display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 1.8rem;">
<span style="background: rgba(107, 46, 158, 0.25); padding: 6px 14px; border-radius: 8px; font-size: 0.8rem; color: #C7D2FE; border: 1.5px solid rgba(139, 66, 196, 0.4); font-weight: 600;">React 19</span>
<span style="background: rgba(107, 46, 158, 0.25); padding: 6px 14px; border-radius: 8px; font-size: 0.8rem; color: #C7D2FE; border: 1.5px solid rgba(139, 66, 196, 0.4); font-weight: 600;">TypeScript</span>
<span style="background: rgba(107, 46, 158, 0.25); padding: 6px 14px; border-radius: 8px; font-size: 0.8rem; color: #C7D2FE; border: 1.5px solid rgba(139, 66, 196, 0.4); font-weight: 600;">Next.js</span>
</div>
        """, unsafe_allow_html=True)
        if st.button(" Start Interview", key="btn_frontend", use_container_width=True):
            pass
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
<div class="glass-card" style="padding: 2rem; position: relative;">
<div style="position: absolute; top: 20px; right: 20px;"><div style="background: rgba(6, 182, 212, 0.35); color: #22D3EE; padding: 6px 16px; border-radius: 999px; font-size: 0.75rem; font-weight: 800; border: 2px solid rgba(6, 182, 212, 0.6); letter-spacing: 0.15em;">POPULAR</div></div>
<div style="font-size: 1.8rem; font-weight: 900; color: white; margin-bottom: 0.8rem; font-family: Orbitron, sans-serif;">Full Stack Engineer</div>
<div style="font-size: 1rem; color: #F59E0B; font-weight: 700; margin-bottom: 1.5rem; letter-spacing: 0.05em;">STARTUPS & SCALE-UPS</div>
<div style="color: #C7D2FE; font-size: 0.95rem; margin-bottom: 1.5rem; line-height: 1.6;">End-to-end development, Cloud architecture, API design, Real-time systems</div>
<div style="display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 1.8rem;">
<span style="background: rgba(6, 182, 212, 0.25); padding: 6px 14px; border-radius: 8px; font-size: 0.8rem; color: #22D3EE; border: 1.5px solid rgba(6, 182, 212, 0.4); font-weight: 600;">Python</span>
<span style="background: rgba(6, 182, 212, 0.25); padding: 6px 14px; border-radius: 8px; font-size: 0.8rem; color: #22D3EE; border: 1.5px solid rgba(6, 182, 212, 0.4); font-weight: 600;">PostgreSQL</span>
<span style="background: rgba(6, 182, 212, 0.25); padding: 6px 14px; border-radius: 8px; font-size: 0.8rem; color: #22D3EE; border: 1.5px solid rgba(6, 182, 212, 0.4); font-weight: 600;">AWS</span>
</div>
        """, unsafe_allow_html=True)
        if st.button(" Start Interview", key="btn_fullstack", use_container_width=True):
            pass
        st.markdown("</div>", unsafe_allow_html=True)

    # Footer
    st.markdown('<div style="margin-top: 7rem; padding: 2.5rem 0; border-top: 2px solid rgba(107, 46, 158, 0.4); text-align: center;"><div style="font-size: 0.9rem; color: #C7D2FE; font-family: Space Grotesk, sans-serif; font-weight: 500;">© 2026 Ultra Cosmos AI • Built with Streamlit <span class="material-symbols-rounded" style="font-size: 14px;">auto_awesome</span></div></div>', unsafe_allow_html=True)
