from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

embedding_function = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Create/load Chroma collection
vectordb = Chroma(
    collection_name="jd_collection",
    persist_directory="chroma_store",
    embedding_function=embedding_function
)

jd_collection = vectordb
