import streamlit as st
import pandas as pd
from utils import set_page_config
from data.sample_tenders import get_tenders

# Set page configuration
set_page_config("TenderTrack - Public Tenders")

# Page header
st.title("📜 Public Tenders")
st.subheader("Find relevant business opportunities")

# Get tender data
tenders = get_tenders()

# Create filter and sort options
st.markdown("### Filter and Sort")
col1, col2 = st.columns(2)

with col1:
    # Filter by sector (previously difficulty)
    sector_options = ["All"] + sorted(tenders["difficulty"].unique().tolist())
    selected_sector = st.selectbox("Sector", sector_options)
    
    # Filter by tender type (previously activity type)
    type_options = ["All"] + sorted(tenders["activity_type"].unique().tolist())
    selected_type = st.selectbox("Tender Type", type_options)

with col2:
    # Filter by location
    location_options = ["All"] + sorted(tenders["location"].unique().tolist())
    selected_location = st.selectbox("Location", location_options)
    
    # Sort options
    sort_by = st.selectbox(
        "Sort By",
        ["Deadline (Soonest First)", "Deadline (Latest First)", "Budget (Highest First)", "Budget (Lowest First)"]
    )

# Apply filters
filtered_tenders = tenders.copy()

if selected_sector != "All":
    filtered_tenders = filtered_tenders[filtered_tenders["difficulty"] == selected_sector]
    
if selected_type != "All":
    filtered_tenders = filtered_tenders[filtered_tenders["activity_type"] == selected_type]
    
if selected_location != "All":
    filtered_tenders = filtered_tenders[filtered_tenders["location"] == selected_location]

# Apply sorting
if sort_by == "Deadline (Soonest First)":
    filtered_tenders = filtered_tenders.sort_values(by="date", ascending=True)
elif sort_by == "Deadline (Latest First)":
    filtered_tenders = filtered_tenders.sort_values(by="date", ascending=False)
elif sort_by == "Budget (Highest First)":
    # Using difficulty as a proxy for budget for now
    difficulty_order = {"Easy": 1, "Moderate": 2, "Hard": 3, "Expert": 4}
    filtered_tenders["budget_numeric"] = filtered_tenders["difficulty"].map(difficulty_order)
    filtered_tenders = filtered_tenders.sort_values(by="budget_numeric", ascending=False)
    filtered_tenders = filtered_tenders.drop(columns=["budget_numeric"])
elif sort_by == "Budget (Lowest First)":
    # Using difficulty as a proxy for budget for now
    difficulty_order = {"Easy": 1, "Moderate": 2, "Hard": 3, "Expert": 4}
    filtered_tenders["budget_numeric"] = filtered_tenders["difficulty"].map(difficulty_order)
    filtered_tenders = filtered_tenders.sort_values(by="budget_numeric", ascending=True)
    filtered_tenders = filtered_tenders.drop(columns=["budget_numeric"])

# Display tenders
st.markdown("### Available Public Tenders")

if filtered_tenders.empty:
    st.warning("No public tenders found matching your filters. Please try different filter options.")
else:
    for index, tender in filtered_tenders.iterrows():
        with st.expander(f"{tender['title']} - {tender['location']} (Deadline: {tender['date']})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Tender ID:** {tender['id']}")
                st.markdown(f"**Submission Deadline:** {tender['date']}")
                st.markdown(f"**Tender Type:** {tender['activity_type']}")
                st.markdown(f"**Location:** {tender['location']}")
                st.markdown(f"**Sector:** {tender['difficulty']}")
                st.markdown(f"**Contract Duration:** {tender['duration']}")
                st.markdown(f"**Description:**")
                st.markdown(tender['description'])
            
            with col2:
                # Action buttons
                st.button("Set Deadline Alert", key=f"reminder_{tender['id']}")
                st.button("Express Interest", key=f"register_{tender['id']}")
                st.button("View Documents", key=f"documents_{tender['id']}")

# Add a back to home button
if st.button("Back to Home"):
    st.switch_page("app.py")

# Footer
st.markdown("---")
st.markdown("© 2023 TenderTrack - Your Public Tender Tracking System")
