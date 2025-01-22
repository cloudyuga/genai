import gradio as gr
from openai import OpenAI
from PyPDF2 import PdfReader
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")  # Make sure to have your OpenAI API key in .env
client = OpenAI(api_key=api_key)

# Set OpenAI API key

# Function to extract text from PDF
def extract_pdf_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to split text into chunks
def split_text(text, chunk_size=500, overlap=50):
    chunks = []
    for i in range(0, len(text), chunk_size - overlap):
        chunks.append(text[i:i + chunk_size])
    return chunks

# Function to generate embeddings
def get_embeddings(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-small"
    )
    return np.array(response.data[0].embedding)

# Function to retrieve relevant chunks
def retrieve_relevant_chunks(query, chunks, chunk_embeddings):
    query_embedding = get_embeddings(query)
    similarities = cosine_similarity([query_embedding], chunk_embeddings)[0]
    top_indices = np.argsort(similarities)[::-1][:3]  # Get top 3 relevant chunks
    return [chunks[i] for i in top_indices]   #we use the chunks list to retrieve the actual text of those relevant chunks. These text chunks will form the context.

# Function to generate a response
def generate_response(context, query):
    messages = [
        {"role": "system", "content": "You are an assistant that answers questions based on the provided context in 30 words."},
        {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}\n\nAnswer:"}
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=300
    )
    return response.choices[0].message.content

# Global variables to store chunks and embeddings
chunks = []
chunk_embeddings = []

# Gradio interface functions
def process_pdf(pdf_file):
    global chunks, chunk_embeddings
    text = extract_pdf_text(pdf_file)
    chunks = split_text(text)
    chunk_embeddings = [get_embeddings(chunk) for chunk in chunks]
    return "PDF processed successfully! You can now chat with it."

def chat_with_pdf(query):
    global chunks, chunk_embeddings
    if not chunks or not chunk_embeddings:
        return "Please upload and process a PDF first."
    relevant_chunks = retrieve_relevant_chunks(query, chunks, chunk_embeddings)
    context = "\n".join(relevant_chunks)
    return generate_response(context, query)

# Gradio app
with gr.Blocks() as app:
    gr.Markdown("# Chat with Your PDF 📄🤖")
    pdf_file = gr.File(label="Upload PDF", file_types=[".pdf"])
    process_button = gr.Button("Process PDF")
    process_status = gr.Textbox(label="Status", interactive=False)
    
    query = gr.Textbox(label="Ask a Question")
    chat_button = gr.Button("Chat with PDF")
    response = gr.Textbox(label="Response", interactive=False)

    process_button.click(process_pdf, inputs=pdf_file, outputs=process_status)
    chat_button.click(chat_with_pdf, inputs=query, outputs=response)

app.launch()
