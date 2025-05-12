import streamlit as st
from utils import set_page_config

# Set page configuration
set_page_config("TrailBlaze - Home")

# Landing page content
st.title("🏕️ TrailBlaze")
st.subheader("Your Adventure Photo Organizer")

# App description
st.markdown("""
### Welcome to TrailBlaze!

**Organize your outdoor adventure photos and create beautiful memories with TrailBlaze.**

TrailBlaze helps outdoor enthusiasts:
- 📸 Organize photos from your hiking, camping, and outdoor adventures
- 🗺️ Tag photos with location and trail information
- 🏞️ Create beautiful memory collections for each adventure
- ⏰ Set reminders for upcoming adventures
- 🔔 Receive notifications about optimal weather conditions for photography
""")

# Features section
st.header("Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📸 Photo Organization")
    st.markdown("Easily organize your adventure photos by trip, location, or date.")
    
    st.markdown("#### 🗺️ Location Tagging")
    st.markdown("Tag photos with trail information and geographical data.")

with col2:
    st.markdown("#### ⏰ Adventure Reminders")
    st.markdown("Set reminders for upcoming hikes and outdoor activities.")
    
    st.markdown("#### 🔔 Smart Notifications")
    st.markdown("Get notified about ideal weather conditions for your next photography adventure.")

# Call to action
st.header("Ready to Organize Your Adventures?")
st.markdown("Check out our available adventure tenders and start planning your next outdoor expedition!")

if st.button("Explore Adventure Tenders"):
    st.switch_page("pages/tenders.py")

# Footer
st.markdown("---")
st.markdown("© 2023 TrailBlaze - Your Adventure Photo Organizer")
