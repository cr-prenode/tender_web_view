

# import indexing pipeline
from rag_pipeline.indexer.indexing_pipeline import IndexingPipeline
from dotenv import load_dotenv
import os

load_dotenv()

hf_api_key = os.getenv("HF_API_KEY")

pipeline = IndexingPipeline(
    hf_api_key=hf_api_key,
    embedding_model_id="Xenova/gte-small",
)

pipeline.index_documents("128946")