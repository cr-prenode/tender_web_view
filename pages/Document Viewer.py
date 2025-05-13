import streamlit as st
import boto3
import tempfile
import os
import io
import json
from PyPDF2 import PdfReader
import base64
from dotenv import load_dotenv
from data.s3_connection import connect_to_s3, list_pdf_objects
# Load environment variables from .env file
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="S3 PDF Viewer",
    layout="wide"
)


# Function to display PDF
def display_pdf(s3_client, bucket_name, object_key):
    try:
        # Get the PDF object from S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        pdf_content = response['Body'].read()
        
        # Create a base64 encoded PDF for display
        base64_pdf = base64.b64encode(pdf_content).decode('utf-8')
        pdf_display = f'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)
        
        # Option to extract text
        if st.button("Extract Text from PDF"):
            with io.BytesIO(pdf_content) as pdf_file:
                reader = PdfReader(pdf_file)
                text = ""
                for page_num in range(len(reader.pages)):
                    text += reader.pages[page_num].extract_text()
                st.text_area("Extracted Text", text, height=400)
                
    except Exception as e:
        st.error(f"Error displaying PDF: {e}")

# Function to get and display metadata.json
def display_metadata(s3_client, bucket_name):
    try:
        # Get the metadata.json file from the top directory
        response = s3_client.get_object(Bucket=bucket_name, Key="metadata.json")
        metadata_content = response['Body'].read().decode('utf-8')
        
        # Parse JSON
        metadata = json.loads(metadata_content)
        
        # Display in expandable section
        with st.expander("Document Metadata", expanded=False):
            # Display as formatted JSON
            st.json(metadata)
            
            # Option to download metadata
            metadata_download = io.BytesIO(metadata_content.encode())
            st.download_button(
                label="Download metadata.json",
                data=metadata_download,
                file_name="metadata.json",
                mime="application/json"
            )
            
        return metadata
    except Exception as e:
        st.warning(f"metadata.json not found or error: {str(e)}")
        return None

# Main app
def main():
    st.title("S3 PDF Document Viewer")
    
    # Get S3 bucket name from environment variable
    bucket_name = os.getenv("S3_BUCKET_NAME")
    if not bucket_name:
        st.error("S3_BUCKET_NAME not found in environment variables. Check your .env file.")
        return
    
    # Connection status and metadata in session state
    if 's3_client' not in st.session_state:
        st.session_state.s3_client = connect_to_s3()
    if 'metadata' not in st.session_state:
        st.session_state.metadata = None
    
    # Show connection info in sidebar
    with st.sidebar:
        st.header("Connection Info")
        st.info(f"Connected to bucket: {bucket_name}")
        st.info(f"Endpoint: {os.getenv('S3_ENDPOINT_URL')}")
        
        # Add a refresh button
        if st.button("Refresh Connection"):
            st.session_state.s3_client = connect_to_s3()
            st.rerun()
        
        # Show other environment variables for debugging
        with st.expander("Environment Variables", expanded=False):
            st.text(f"Service Account: {os.getenv('S3_SERVICE_ACCOUNT', 'Not set')}")
            st.text(f"Bucket ARN: {os.getenv('S3_BUCKET_ARN', 'Not set')}")
            
    if st.session_state.s3_client:
        # Display metadata if available
        metadata = display_metadata(st.session_state.s3_client, bucket_name)
        if metadata:
            st.session_state.metadata = metadata
        
        # Create tabs for different functionalities
        tab1, tab2 = st.tabs(["PDF Documents", "Metadata Explorer"])
        
        with tab1:
            # Optional prefix/folder filter
            prefix = st.text_input("Prefix Filter (optional)", "")
            
            # List PDFs in the configured bucket
            pdf_objects = list_pdf_objects(st.session_state.s3_client, bucket_name, prefix)
            
            if pdf_objects:
                selected_pdf = st.selectbox("Select PDF Document", pdf_objects)
                
                if selected_pdf:
                    st.subheader(f"Viewing: {os.path.basename(selected_pdf)}")
                    display_pdf(st.session_state.s3_client, bucket_name, selected_pdf)
            else:
                st.info(f"No PDF documents found in bucket {bucket_name} with prefix '{prefix}'")
        
        with tab2:
            if st.session_state.metadata:
                st.subheader("Metadata Explorer")
                # Allow searching through metadata
                search_term = st.text_input("Search in metadata", "")
                
                if search_term:
                    # Simple recursive function to search in nested JSON
                    def search_json(data, term, path=""):
                        results = []
                        if isinstance(data, dict):
                            for k, v in data.items():
                                new_path = f"{path}.{k}" if path else k
                                if term.lower() in str(k).lower() or term.lower() in str(v).lower():
                                    results.append((new_path, v))
                                if isinstance(v, (dict, list)):
                                    results.extend(search_json(v, term, new_path))
                        elif isinstance(data, list):
                            for i, item in enumerate(data):
                                new_path = f"{path}[{i}]"
                                if term.lower() in str(item).lower():
                                    results.append((new_path, item))
                                if isinstance(item, (dict, list)):
                                    results.extend(search_json(item, term, new_path))
                        return results
                    
                    search_results = search_json(st.session_state.metadata, search_term)
                    if search_results:
                        st.subheader(f"Found {len(search_results)} matches")
                        for path, value in search_results:
                            with st.expander(f"Path: {path}"):
                                st.write(value)
                    else:
                        st.info(f"No matches found for '{search_term}'")
                else:
                    # Display complete metadata in a structured way
                    st.json(st.session_state.metadata)
            else:
                st.info("metadata.json not found in the bucket's top directory")
    else:
        st.error("Failed to connect to S3. Check your environment variables and connection.")

# Example .env file content for reference
env_example = """
# S3 Configuration
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
S3_ENDPOINT_URL=https://your-endpoint-url
S3_BUCKET_NAME=your-bucket-name
S3_SERVICE_ACCOUNT=your-service-account
S3_BUCKET_ARN=arn:aws:s3:::your-bucket-name
"""

# Check if .env file exists and provide helpful message if it doesn't
if not os.path.exists(".env"):
    st.error("No .env file found. Please create one with the required variables.")
    st.code(env_example, language="text")
    
if __name__ == "__main__":
    main()