"""
Premium AI Text Display Helper
Makes all AI-generated text bright, visible, and attractive
"""
import streamlit as st

def display_ai_response(text, title=None):
    """
    Display AI-generated text with premium cosmic styling
    
    Args:
        text: The AI response text to display
        title: Optional title for the response
    """
    html = '<div class="glass-card" style="padding: 2rem; margin: 1.5rem 0; border: 2px solid rgba(6, 182, 212, 0.4); box-shadow: 0 8px 32px rgba(6, 182, 212, 0.3);">'
    
    if title:
        html += f'<h3 style="color: #22D3EE; font-family: Orbitron, sans-serif; margin-bottom: 1.5rem; text-shadow: 0 0 20px rgba(6, 182, 212, 0.7);">{title}</h3>'
    
    html += f'<div style="color: #FFFFFF; font-size: 1.1rem; line-height: 1.9; font-weight: 400;">{text}</div>'
    html += '</div>'
    
    st.markdown(html, unsafe_allow_html=True)


def display_ai_list(items, title=None):
    """
    Display a list of AI-generated items with premium styling
    
    Args:
        items: List of strings to display
        title: Optional title for the list
    """
    html = '<div class="glass-card" style="padding: 2rem; margin: 1.5rem 0; border: 2px solid rgba(6, 182, 212, 0.4);">'
    
    if title:
        html += f'<h3 style="color: #22D3EE; font-family: Orbitron, sans-serif; margin-bottom: 1.5rem;">{title}</h3>'
    
    html += '<ul style="list-style: none; padding: 0;">'
    for item in items:
        html += f'<li style="color: #FFFFFF; font-size: 1.05rem; line-height: 1.9; margin-bottom: 1rem; padding-left: 1.5rem; position: relative;"><span style="position: absolute; left: 0; color: #22D3EE;">•</span>{item}</li>'
    html += '</ul></div>'
    
    st.markdown(html, unsafe_allow_html=True)
