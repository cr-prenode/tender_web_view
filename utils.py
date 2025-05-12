import streamlit as st
from typing import Literal

def set_page_config(title="TenderTrack", layout: Literal["wide", "centered"] = "wide"):
    """Set the page configuration with consistent settings"""
    st.set_page_config(
        page_title=title,
        page_icon="📊",
        layout=layout,
        initial_sidebar_state="expanded"
    )
    
    # Add the app name to the sidebar
    st.sidebar.title("📊 TenderTrack")
    st.sidebar.markdown("Your Public Tender Tracking System")
    st.sidebar.markdown("---")
