import streamlit as st
from pinecone import Pinecone, ServerlessSpec
import fitz  # PyMuPDF
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

import os
from dotenv import load_dotenv
load_dotenv() #load all environment variables from .env
pinecone_key= os.getenv("PINECONE_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=pinecone_key)
client = MistralClient(api_key=mistral_api_key)
index_name = "pdf-index"

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=1024,
        metric="cosine",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

index = pc.Index(index_name)

# Function to extract text from PDF
def extract_text_from_pdf(file):
    text = ""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

# Function to get embeddings using Mistral API
def get_embeddings(text):
    if not text.strip():
        raise ValueError("Input text is empty.")
    
    embeddings_batch_response = client.embeddings(
        model="mistral-embed",
        input=[text]  # Ensure the input is a list of strings
    )
    return embeddings_batch_response.data[0].embedding

# Function to index PDF content
def index_pdf_content(file_name, pdf_text, embeddings):
    index.upsert([(file_name, embeddings, {"text": pdf_text})])

# Function to query PDF content
def query_pdf_content(question):
    question_embedding = get_embeddings(question)
    results = index.query(vector=question_embedding, top_k=3, include_metadata=True)
    return results

# Function to generate answer using Mistral API with streaming
def generate_answer(question, context):
    messages = [
        ChatMessage(role="user", content=f"Context: {context}\n\nQuestion: {question}\n\nAnswer:")
    ]
    response = client.chat(
        model="mistral-large-latest",
        messages=messages
    )
    return response.choices[0].message.content

# Streamlit app setup
st.title("PDF-based FAQ Chatbot")
st.write("Upload a PDF and ask questions based on its content.")

# PDF upload section
uploaded_file = st.file_uploader("Upload PDF", type="pdf")
if uploaded_file is not None:
    pdf_text = extract_text_from_pdf(uploaded_file)
    if pdf_text.strip():
        try:
            embeddings = get_embeddings(pdf_text)
            index_pdf_content(uploaded_file.name, pdf_text, embeddings)
            st.success("PDF uploaded and indexed successfully!")
        except ValueError as e:
            st.error(f"Error extracting embeddings: {e}")
    else:
        st.error("The extracted text from the PDF is empty. Please upload a valid PDF.")

    # Question input section
    question = st.text_input("Ask a question")
    if question:
        try:
            results = query_pdf_content(question)
            if results["matches"]:
                context = results["matches"][0]["metadata"]["text"]
                response=generate_answer(question, context)
                st.subheader("Response")
                st.write(response)
            else:
                st.write("Sorry, I don't know the answer to that.")
        except ValueError as e:
            st.error(f"Error querying content: {e}")
else:
    st.write("Upload a file")
