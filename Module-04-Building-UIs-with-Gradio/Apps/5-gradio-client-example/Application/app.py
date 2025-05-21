import fitz  # PyMuPDF
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv
import os
import gradio as gr

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# File Path (replace "sample.pdf" with the name of your PDF file)
PDF_FILE = "sample.pdf" #"Company_HR_Policy.pdf"  # Ensure this file is in the same directory as app.py

# Utility Functions
def load_pdf(file_path):
    """Extract text from a PDF file."""
    try:
        with fitz.open(file_path) as doc:
            return "".join([page.get_text() for page in doc])
    except Exception as e:
        return f"Error reading PDF: {e}"

def split_text(text, chunk_size=1000, chunk_overlap=20):
    """Split text into manageable chunks."""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap, length_function=len, is_separator_regex=False
    )
    return text_splitter.create_documents([text])

def create_and_load_db(chunks, persist_directory="pdf_embeddings"):
    """Create and load ChromaDB."""
    embeddings = HuggingFaceEmbeddings()
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
            model="gpt-3.5-turbo",  # Replace with preferred model
            messages=messages,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating response: {e}"

def process_question(question):
    if not question:
        return "Please provide a question."

    # Step 1: Load and extract text from the PDF
    pdf_text = load_pdf(PDF_FILE)
    if pdf_text.startswith("Error"):
        return pdf_text

    # Step 2: Split the text into chunks
    chunks = split_text(pdf_text)

    # Step 3: Create and load ChromaDB
    vectordb = create_and_load_db(chunks)

    # Step 4: Perform similarity search
    try:
        docs = vectordb.similarity_search(question)
        if not docs:
            return "No relevant information found."

        # Step 5: Generate a response using the retrieved context
        context = docs[0].page_content
        response = generate_response(context, question)
        return response
    except Exception as e:
        return f"Error during similarity search or response generation: {str(e)}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# PDF Chatbot")

    with gr.Row():
        question_input = gr.Textbox(label="Ask a Question", placeholder="Enter your question here...")
        output = gr.Textbox(label="Answer", lines=5, interactive=False)

    submit_button = gr.Button("Submit")
    submit_button.click(process_question, inputs=[question_input], outputs=output)

if __name__ == "__main__":
    demo.launch()
