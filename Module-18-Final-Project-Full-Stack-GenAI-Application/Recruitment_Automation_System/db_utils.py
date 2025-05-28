import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
import chromadb

embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

chroma_client = chromadb.HttpClient(
    host="chroma",  # Replace with your service name
    port=8000
)

jd_collection = Chroma(
    client=chroma_client,
    collection_name="jd_collection",
    embedding_function=embedding_function
)
