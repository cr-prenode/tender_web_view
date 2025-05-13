import streamlit as st
from utils import set_page_config


tender_details = st.Page("pages/Tender Details.py", title = "Tender Details")
document_viewer = st.Page("pages/document_viewer.py", title = "Document Viewer")
welcome_page = st.Page("pages/Welcome.py", title = "Welcome")


# Set page configuration
set_page_config("AI Tender Analysis - Home")

pg = st.navigation(
    {
        "Welcome": [welcome_page],
        "Tools": [tender_details],
    }
)

pg.run()
