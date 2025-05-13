import os
import streamlit as st
import boto3


def connect_to_s3():
    try:
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")
        s3_endpoint_url = os.getenv("S3_ENDPOINT_URL")
        
        if not all([aws_access_key_id, aws_secret_access_key, s3_endpoint_url]):
            st.error("Missing required environment variables. Check your .env file.")
            return None
            
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=s3_endpoint_url
        )
        return s3_client
    except Exception as e:
        st.error(f"Error connecting to S3: {e}")
        return None

# Function to list PDF objects in a bucket
def list_pdf_objects(s3_client, bucket_name, prefix=""):
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
        pdf_objects = []
        if 'Contents' in response:
            for obj in response['Contents']:
                if obj['Key'].endswith('.pdf'):
                    pdf_objects.append(obj['Key'])
        return pdf_objects
    except Exception as e:
        st.error(f"Error listing objects: {e}")
        return []
