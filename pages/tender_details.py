import streamlit as st
import pandas as pd
from utils import set_page_config
from data.tender_provider import get_tenders
from rag_pipeline.indexer.indexing_pipeline import IndexingPipeline
from rag_pipeline.pipeline.query_pipeline import QueryPipeline
from dotenv import load_dotenv
import os

load_dotenv()


hf_api_key = os.getenv("HF_API_KEY")


# Initialize Indexing Pipeline
indexing_pipeline = IndexingPipeline(
    hf_api_key=hf_api_key,
    embedding_model_id="intfloat/multilingual-e5-large-instruct",
)

query_pipeline = QueryPipeline(
    hf_api_key=hf_api_key,
    llm_id="deepseek-ai/DeepSeek-R1-Distill-Qwen-32B",
    embedding_model_id="intfloat/multilingual-e5-large-instruct",
)

def run_query(tender, question):
    """Runs the query pipeline on the selected tender."""
    try:
        # Assuming the tender ID is the S3 object key
        result = query_pipeline.answer_question(tender, question)
        return result
    except Exception as e:
        st.error(f"Error during querying: {e}")
        return None

def navigate_to_document_viewer(tender_id):
    """Sets the document ID and navigates to the document viewer page."""
    st.session_state.tender_id = tender_id
    st.switch_page("pages/document_viewer.py")

def run_index(tender_id):
    """Runs the indexing pipeline on the selected tender."""
    try:
        # Assuming the tender ID is the S3 object key
        indexing_pipeline.index_documents(tender_id)
        st.success(f"Indexing completed for Tender ID: {tender_id}")
    except Exception as e:
        st.error(f"Error during indexing: {e}")

# Page header
st.title("📜 Public Tenders")
st.subheader("Explore scraped tenders from various sources")

# Get tender data
tenders = get_tenders()

# Create filter and sort options
# st.markdown("### Filter and Sort")
# col1, col2 = st.columns(2)

# with col1:
#     # Filter by sector (previously difficulty)
#     publication_options = ["All"] 
#     selected_sector = st.selectbox("Tender Type", publication_options)
    
# with col2:
#     # Filter by location
#     location_options = ["All"] #+ sorted(tenders["Art des Auftrags"]["content"].unique().tolist())
#     selected_location = st.selectbox("Location", location_options)
    
# Apply filters
filtered_tenders = tenders.copy()

# if selected_sector != "All":
#     filtered_tenders = filtered_tenders[filtered_tenders["difficulty"] == selected_sector]
        
# if selected_location != "All":
#     filtered_tenders = filtered_tenders[filtered_tenders["location"] == selected_location]

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
                
                if st.button("Run Index (AI)", key=f"index_{tender_details['id']}"):
                    with st.spinner('Indexing in progress...'):
                        # Call the function to run the indexing pipeline
                        run_index(tender_details['id'])
                
                # This button now calls a callback function that sets the state and switches page
                if st.button("Document Details", key=f"details_{tender_details['id']}"):
                    navigate_to_document_viewer(tender_details['id'])
            st.markdown("#### Fügen Sie Fragen hinzu, die Sie über Ihre Dokumente stellen möchten")
            
            # Display a text input for each existing question
            st.text_input(
                    "Frage",
                    placeholder="Geben Sie Ihre Frage ein",
                    key=f"question_{tender_details['id']}"
                )

            # Button to add a new question field
            if st.button("Frage stellen" , key=f"add_question_{tender_details['id']}"):
                answer = run_query(tender_details['id'], st.session_state[f"question_{tender_details['id']}"])
                if answer:
                    st.success(f"Antwort: {answer}")
                else:
                    st.error("Fehler bei der Beantwortung der Frage. Bitte versuchen Sie es erneut.")

# Footer
st.markdown("---")
st.markdown("© 2023 TenderTrack - Your Public Tender Tracking System")