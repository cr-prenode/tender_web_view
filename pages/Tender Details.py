import streamlit as st
import pandas as pd
from utils import set_page_config
from data.tender_provider import get_tenders

# Set page configuration
set_page_config("TenderTrack - Public Tenders")

# Page header
st.title("📜 Public Tenders")
st.subheader("Explore scraped tenders from various sources")

# Get tender data
tenders = get_tenders()

# Create filter and sort options
st.markdown("### Filter and Sort")
col1, col2 = st.columns(2)

with col1:
    # Filter by sector (previously difficulty)
    publication_options = ["All"] 
    selected_sector = st.selectbox("Tender Type", publication_options)
    
with col2:
    # Filter by location
    location_options = ["All"] #+ sorted(tenders["Art des Auftrags"]["content"].unique().tolist())
    selected_location = st.selectbox("Location", location_options)
    
# Apply filters
filtered_tenders = tenders.copy()

if selected_sector != "All":
    filtered_tenders = filtered_tenders[filtered_tenders["difficulty"] == selected_sector]
        
if selected_location != "All":
    filtered_tenders = filtered_tenders[filtered_tenders["location"] == selected_location]

# Display tenders
st.markdown("### Available Public Tenders")

if filtered_tenders is None:
    st.warning("No public tenders found matching your filters. Please try different filter options.")
else:
    for tender in filtered_tenders["tender_id"].keys():
        tender_details = filtered_tenders["tender_id"][tender]['data']
        with st.expander(f"{tender_details['name']} - {tender_details['id']}"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Tender ID:** {tender_details['id']}")
                st.markdown(f"**Title:** {tender_details['name']}")
                st.markdown(f"**Tender Type:** {tender_details['properties']['Art des Auftrags']['content']}")
                st.markdown(f"**Tender Company:** {tender_details['properties']['Auftraggeber']['content']}")
                st.markdown(f"**Submission Deadline:** {tender_details['properties']['Angebotsfrist']['content']}")
                st.markdown(f"**Location:** {tender_details['properties']['Erfüllungsort']['content']}")
            
            with col2:
                # Action buttons
                st.button("Run Index (AI)", key=f"index_{tender_details['id']}")
    pass

# Add a back to home button
if st.button("Back to Home"):
    st.switch_page("app.py")

# Footer
st.markdown("---")
st.markdown("© 2023 TenderTrack - Your Public Tender Tracking System")
