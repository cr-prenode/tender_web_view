import streamlit as st

def set_page_config(title="TrailBlaze", layout="wide"):
    """Set the page configuration with consistent settings"""
    st.set_page_config(
        page_title=title,
        page_icon="🏕️",
        layout=layout,
        initial_sidebar_state="expanded"
    )
    
    # Add the app name to the sidebar
    st.sidebar.title("🏕️ TrailBlaze")
    st.sidebar.markdown("Your Adventure Photo Organizer")
    st.sidebar.markdown("---")
