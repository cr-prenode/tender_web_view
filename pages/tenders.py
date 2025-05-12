import streamlit as st
import pandas as pd
from utils import set_page_config
from data.sample_tenders import get_tenders

# Set page configuration
set_page_config("TrailBlaze - Adventure Tenders")

# Page header
st.title("🌄 Adventure Tenders")
st.subheader("Find your next outdoor adventure opportunity")

# Get tender data
tenders = get_tenders()

# Create filter and sort options
st.markdown("### Filter and Sort")
col1, col2 = st.columns(2)

with col1:
    # Filter by difficulty
    difficulty_options = ["All"] + sorted(tenders["difficulty"].unique().tolist())
    selected_difficulty = st.selectbox("Difficulty Level", difficulty_options)
    
    # Filter by activity type
    activity_options = ["All"] + sorted(tenders["activity_type"].unique().tolist())
    selected_activity = st.selectbox("Activity Type", activity_options)

with col2:
    # Filter by location
    location_options = ["All"] + sorted(tenders["location"].unique().tolist())
    selected_location = st.selectbox("Location", location_options)
    
    # Sort options
    sort_by = st.selectbox(
        "Sort By",
        ["Date (Newest First)", "Date (Oldest First)", "Difficulty (Easiest First)", "Difficulty (Hardest First)"]
    )

# Apply filters
filtered_tenders = tenders.copy()

if selected_difficulty != "All":
    filtered_tenders = filtered_tenders[filtered_tenders["difficulty"] == selected_difficulty]
    
if selected_activity != "All":
    filtered_tenders = filtered_tenders[filtered_tenders["activity_type"] == selected_activity]
    
if selected_location != "All":
    filtered_tenders = filtered_tenders[filtered_tenders["location"] == selected_location]

# Apply sorting
if sort_by == "Date (Newest First)":
    filtered_tenders = filtered_tenders.sort_values(by="date", ascending=False)
elif sort_by == "Date (Oldest First)":
    filtered_tenders = filtered_tenders.sort_values(by="date", ascending=True)
elif sort_by == "Difficulty (Easiest First)":
    difficulty_order = {"Easy": 1, "Moderate": 2, "Hard": 3, "Expert": 4}
    filtered_tenders["difficulty_numeric"] = filtered_tenders["difficulty"].map(difficulty_order)
    filtered_tenders = filtered_tenders.sort_values(by="difficulty_numeric", ascending=True)
    filtered_tenders = filtered_tenders.drop(columns=["difficulty_numeric"])
elif sort_by == "Difficulty (Hardest First)":
    difficulty_order = {"Easy": 1, "Moderate": 2, "Hard": 3, "Expert": 4}
    filtered_tenders["difficulty_numeric"] = filtered_tenders["difficulty"].map(difficulty_order)
    filtered_tenders = filtered_tenders.sort_values(by="difficulty_numeric", ascending=False)
    filtered_tenders = filtered_tenders.drop(columns=["difficulty_numeric"])

# Display tenders
st.markdown("### Available Adventure Tenders")

if filtered_tenders.empty:
    st.warning("No adventure tenders found matching your filters. Please try different filter options.")
else:
    for index, tender in filtered_tenders.iterrows():
        with st.expander(f"{tender['title']} - {tender['location']} ({tender['date']})"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**ID:** {tender['id']}")
                st.markdown(f"**Date:** {tender['date']}")
                st.markdown(f"**Activity Type:** {tender['activity_type']}")
                st.markdown(f"**Location:** {tender['location']}")
                st.markdown(f"**Difficulty:** {tender['difficulty']}")
                st.markdown(f"**Duration:** {tender['duration']}")
                st.markdown(f"**Description:**")
                st.markdown(tender['description'])
            
            with col2:
                # Action buttons
                st.button("Set Reminder", key=f"reminder_{tender['id']}")
                st.button("Register Interest", key=f"register_{tender['id']}")
                st.button("View Photos", key=f"photos_{tender['id']}")

# Add a back to home button
if st.button("Back to Home"):
    st.switch_page("app.py")

# Footer
st.markdown("---")
st.markdown("© 2023 TrailBlaze - Your Adventure Photo Organizer")
