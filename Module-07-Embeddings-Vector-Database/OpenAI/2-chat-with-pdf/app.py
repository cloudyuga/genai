import streamlit as st
import fitz  # PyMuPDF
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Utility Functions
def load_pdf(file):
    """Extract text from a PDF file."""
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        return "".join([page.get_text() for page in doc])
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

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
        st.error(f"Error generating response: {e}")
        return None

# Main Application Logic
def main():
    st.title("PDF Chatbot with OpenAI")

    # Sidebar: File upload
    uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=['pdf'])
    prompt = st.text_input("Ask a Question", "")
    submitted = st.button("Submit")

    if submitted and uploaded_file:
        pdf_text = load_pdf(uploaded_file)

        if pdf_text:
            st.write("PDF Content Loaded!")
            chunks = split_text(pdf_text)
            vectordb = create_and_load_db(chunks)

            if prompt:
                docs = vectordb.similarity_search(prompt)
                if docs:
                    context = docs[0].page_content
                    response = generate_response(context, prompt)
                    st.subheader("Generated Answer:")
                    st.write(response)
                else:
                    st.warning("No relevant information found.")
        else:
            st.error("Unable to extract text from the PDF.")

if __name__ == "__main__":
    main()
