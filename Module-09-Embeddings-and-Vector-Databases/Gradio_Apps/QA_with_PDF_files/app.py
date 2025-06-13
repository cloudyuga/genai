import gradio as gr
import fitz  # PyMuPDF
from langchain_community.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Utility Functions
def load_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        doc = fitz.open(file_path)  # Use the path directly
        return "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"❌ Error reading PDF: {e}"


def split_text(text, chunk_size=1000, chunk_overlap=20):
    """Split text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len, is_separator_regex=False
    )
    return text_splitter.create_documents([text])

def create_and_load_db(chunks, persist_directory="pdf_embeddings"):
    """Create and load ChromaDB."""
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)
    vectordb.persist()
    return Chroma(persist_directory=persist_directory, embedding_function=embeddings)

def generate_response(context, question):
    """Generate a response using OpenAI."""
    try:
        messages = [
            {"role": "system", "content": "You are an assistant that answers questions based on PDF content."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"}
        ]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Error generating response: {e}"

# Core Gradio function
def chat_with_pdf(file, question):
    if not file:
        return "⚠️ Please upload a PDF file."
    if not question:
        return "⚠️ Please enter a question."

    pdf_text = load_pdf(file.name)
    if pdf_text.startswith("❌"):
        return pdf_text

    chunks = split_text(pdf_text)
    vectordb = create_and_load_db(chunks)
    docs = vectordb.similarity_search(question)

    if not docs:
        return "⚠️ No relevant information found in the PDF."

    context = docs[0].page_content
    return generate_response(context, question)

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📄 Chat with your PDF using OpenAI + Chroma")
    gr.Markdown("Upload a PDF and ask questions. The app retrieves relevant chunks using ChromaDB.")

    with gr.Row():
        pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
        question_input = gr.Textbox(label="Your Question", placeholder="Ask something from the PDF...")

    submit_btn = gr.Button("Get Answer")
    output = gr.Textbox(label="Answer", lines=8)

    submit_btn.click(fn=chat_with_pdf, inputs=[pdf_input, question_input], outputs=output)

# Launch app
if __name__ == "__main__":
    demo.launch()
