import streamlit as st
from typing import Literal

def set_page_config(title="TenderTrack", logo_path="logo.png", layout: Literal["wide", "centered"] = "wide"):
    """Set the page configuration with consistent settings and logo"""
    st.set_page_config(
        page_title=title,
        layout=layout,
        initial_sidebar_state="expanded"
    )
    
    # Add the app logo to the sidebar
    st.sidebar.image(logo_path, use_container_width=True)
 