import pandas as pd
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import boto3
import json
import streamlit as st
from data.s3_connection import connect_to_s3
# Load environment variables from .env file
load_dotenv()


def get_tenders():
    """
    Create and return a DataFrame of public tenders.
    This is representative of what would typically come from a database or API.
    """

    client = connect_to_s3()
    response = client.get_object(Bucket="prenode-bucket", Key="metadata.json")
    metadata_content = response['Body'].read().decode('utf-8')
    
    # Parse JSON
    metadata = json.loads(metadata_content)
    return metadata
