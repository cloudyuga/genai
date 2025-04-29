import os
import gradio as gr
import hashlib
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv
from langchain_core.documents import Document

# ✅ Load API Keys
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Initialize GPT-4o-mini Model
model = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=api_key
)

# ✅ Initialize Embedding Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ Initialize ChromaDB
vector_store = Chroma(
    collection_name="pdf_embeddings",
    embedding_function=embeddings,
    persist_directory="./chroma_pdf_db",
)

# ✅ Function to Generate Unique PDF Hash
def get_pdf_hash(pdf_path):
    """Generate a unique hash for a PDF file."""
    hasher = hashlib.md5()
    with open(pdf_path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()

# ✅ Check If PDF Exists in ChromaDB
def is_pdf_processed(pdf_hash):
    """Check if a PDF hash exists in ChromaDB metadata."""
    existing_docs = vector_store.get(include=["metadatas"])
    for metadata in existing_docs["metadatas"]:
        if metadata and metadata.get("pdf_hash") == pdf_hash:
            return True
    return False

# ✅ Process and Store PDF in ChromaDB (Avoiding Duplicates)
def process_pdf(pdf_file):
    """Loads a PDF, extracts text, and stores embeddings only if not already processed."""
    if not pdf_file:
        return "Please upload a PDF file."

    pdf_hash = get_pdf_hash(pdf_file.name)  # Get unique file hash

    if is_pdf_processed(pdf_hash):  # Check if it's already stored
        return "PDF already processed. You can start searching!"

    # Load and extract text
    loader = PyPDFLoader(pdf_file.name)
    pages = loader.load()
    documents = [Document(page_content=page.page_content, metadata={"pdf_hash": pdf_hash}) for page in pages]

    # Store in ChromaDB
    vector_store.add_documents(documents)

    return f"Processed {len(documents)} pages and stored embeddings successfully!"

# ✅ Search for Similar Text in PDF and Generate GPT-4o-mini Response
def search_pdf(query):
    """Find relevant text in stored PDF embeddings and generate a response using GPT-4o-mini.
       If the query is unrelated to the PDF, politely decline to answer.
    """
    if not query:
        return "Please enter a query."

    results = vector_store.similarity_search(query, k=2)  # Get results with similarity scores

    if results:
        retrieved_text = "\n".join([doc.page_content[:500] for doc in results])  # Limiting output to 500 chars

        # Generate response using GPT-4o-mini
        response = model.invoke([
            {"role": "system", "content": "You are a helpful AI assistant."},
            {"role": "user", "content": (
                f"Based on the following extracted content, answer concisely in 70 words:\n\n"
                f"{retrieved_text}\n\n"
                f"{query}. If the extracted content and the query are not connected with each other, "
                f"deny politely by saying 'I'm sorry, but I can only answer questions related to the uploaded PDFs.'"
            ), 
            },
        ])
        
        return response.content  # Return AI-generated response
    
    return "No relevant text found."

# ✅ Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📕 PDF Upload & AI-Powered Search (No Duplicate Processing)")

    pdf_input = gr.File(label="Upload PDF")
    process_button = gr.Button("Process PDF")
    process_output = gr.Textbox(label="Processing Status", interactive=False)

    query_input = gr.Textbox(label="Enter Query", placeholder="Search something in the PDF...")
    search_button = gr.Button("Search in PDF")
    search_output = gr.Textbox(label="AI Response", interactive=False)

    # Upload and process PDF (avoiding duplicates)
    process_button.click(process_pdf, inputs=[pdf_input], outputs=[process_output])

    # Search within the stored PDF embeddings and generate response
    search_button.click(search_pdf, inputs=[query_input], outputs=[search_output])

    # ✅ Clear outputs when a new file is uploaded or removed
    pdf_input.change(
        lambda _: ("", "", ""),  # Reset process_output and search_output
        inputs=[pdf_input],
        outputs=[process_output, search_output, query_input]
    )

# ✅ Run the Gradio App
demo.launch()
