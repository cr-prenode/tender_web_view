import streamlit as st
from utils import set_page_config


# Landing page content
st.title("AI Tender Analysis")
st.subheader("Track and Analyze Public Tenders with AI")

# App description
st.markdown("""
**Efficiently track and manage public tender offerings with TenderTrack.**

TenderTrack helps organizations and individuals:
- 📄 Track public tender announcements and deadlines
- 🔍 Search for relevant tender opportunities
- 📝 Organize tender documentation and requirements
- ⏰ Set reminders for important submission dates
- 🔔 Receive notifications about new tender opportunities
""")

# Features section
st.header("Features")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 📄 Tender Tracking")
    st.markdown("Easily track public tenders by sector, location, or deadline.")
    
    st.markdown("#### 🔍 Advanced Search")
    st.markdown("Find relevant tender opportunities with powerful search filters.")

with col2:
    st.markdown("#### ⏰ Deadline Reminders")
    st.markdown("Set reminders for important submission dates and never miss a deadline.")
    
    st.markdown("#### 🔔 Opportunity Alerts")
    st.markdown("Get notified about new tender opportunities in your areas of interest.")

# Call to action
st.header("Ready to Find Tender Opportunities?")
st.markdown("Check out our available public tenders and start tracking potential business opportunities!")

if st.button("Explore Public Tenders"):
    st.switch_page("pages/Tender Details.py")

if st.button("Document Details"):
    st.switch_page("pages/Document Viewer.py")

# Footer
st.markdown("---")
st.markdown("© 2023 TenderTrack - Your Public Tender Tracking System")
