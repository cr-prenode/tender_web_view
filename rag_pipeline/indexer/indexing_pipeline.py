from haystack import Pipeline, Document
from haystack.utils import Secret
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack.components.retrievers.in_memory import (
    InMemoryBM25Retriever,
    InMemoryEmbeddingRetriever,
)
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.components.generators import HuggingFaceAPIGenerator
from haystack.components.converters import PyPDFToDocument
from haystack.components.preprocessors import DocumentCleaner
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter
from haystack.components.embedders import (
    SentenceTransformersTextEmbedder,
    SentenceTransformersDocumentEmbedder,
    HuggingFaceAPITextEmbedder,
    HuggingFaceAPIDocumentEmbedder,
)
from haystack.document_stores.types import DuplicatePolicy
from haystack.components.rankers import LostInTheMiddleRanker
from haystack_integrations.document_stores.chroma import ChromaDocumentStore
from haystack_integrations.components.retrievers.chroma import ChromaEmbeddingRetriever
from haystack.dataclasses.byte_stream import ByteStream
import os
from pathlib import Path
from dotenv import load_dotenv
import io
from data.s3_connection import connect_to_s3, list_pdf_objects
from tqdm import tqdm
client = connect_to_s3()


class IndexingPipeline:
    """
    A class to extract summaries from PDF documents using a pipeline of components.
    Attributes:
        indexing_pipeline (Pipeline): The pipeline used for indexing documents.
        query_pipeline (Pipeline): The pipeline used for querying and generating summaries.
    Methods:
        __init__(hf_api_key: str):
            Initializes the SummaryExtractor with the provided Hugging Face API key.
        _setup_pipelines(api_key: str) -> Tuple[Pipeline, Pipeline]:
            Sets up the indexing and query pipelines using the provided API key.
        create_summary(pdf_data: bytes) -> str:
            Creates a summary from the provided PDF data.
    """

    def __init__(self, hf_api_key: str, embedding_model_id: str):
        self.document_store = ChromaDocumentStore(host="localhost", port="8000")
        self.embedding_model_id = embedding_model_id
        self.indexing_pipeline = self._setup_pipelines(hf_api_key)

    def _setup_pipelines(self, api_key):
        prompt_template = """
        Write a high-quality answer for the given question using only the provided search results (some of which might be irrelevant). Your answer must be written in german!
        Documents:
        {% for doc in documents %}
            {{ doc.content }}
        {% endfor %}
        Question: {{question}}
        Answer:
        """

        indexing_pipeline = Pipeline()
        # indexing_pipeline.add_component("converter", PyPDFToDocument())
        indexing_pipeline.add_component("cleaner", DocumentCleaner())
        indexing_pipeline.add_component(
            "splitter", DocumentSplitter(split_by="period", split_length=6)
        )
        indexing_pipeline.add_component(
            "document_embedder",
            HuggingFaceAPIDocumentEmbedder(
                api_type="serverless_inference_api",
                api_params={"model": self.embedding_model_id},
                token=Secret.from_token(api_key),
                meta_fields_to_embed=["tender_id"],
            ),
        )
        indexing_pipeline.add_component(
            "writer", DocumentWriter(document_store=self.document_store, policy=DuplicatePolicy.SKIP)
        )

        # indexing_pipeline.connect("converter", "cleaner")
        indexing_pipeline.connect("cleaner", "splitter")
        indexing_pipeline.connect("splitter", "document_embedder")
        indexing_pipeline.connect("document_embedder", "writer")

        return indexing_pipeline
    

    def index_documents(self, tender_id):

        pdfs = list_pdf_objects(client, bucket_name="prenode-bucket", prefix=tender_id)
        converter = PyPDFToDocument()
        # download the files
        file_paths = []
        raw_docs = []
        for pdf in tqdm(pdfs):
            file_path = f"/tmp/{os.path.basename(pdf)}"
            client.download_file("prenode-bucket", pdf, file_path)
            file_paths.append(file_path)
            documents = converter.run(sources = [Path(file_path)])

            for doc in documents:
                # Add metadata during creation
                raw_docs.append(
                    Document(
                        content=doc,
                        meta={"tender_id": tender_id},
                    )
                )
            # Add metadata during creation
        
        self.indexing_pipeline.run(
            {
                "cleaner": {"documents": raw_docs}
                
            },
        )