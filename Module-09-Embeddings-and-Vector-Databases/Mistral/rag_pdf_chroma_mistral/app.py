import streamlit as st
import fitz  # PyMuPDF
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

# Initialize Mistral client
client = MistralClient(api_key=mistral_api_key)

def get_llm_response(input, content, prompt):
    # Takes input, content, and prompt to generate a response using the Mistral model
    messages = [
        ChatMessage(role="system", content=input),
        ChatMessage(role="user", content=f"Context: {content}\n\nQuestion: {prompt}\n\nAnswer:")
    ]
    response = client.chat(
        model="mistral-large-latest",
        messages=messages
    )
    return response.choices[0].message.content

# Function to extract text from PDF file
def extract_text_from_pdf(file):
    try:
        doc = fitz.open(stream=file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        st.error(f"Error occurred while reading PDF file: {e}")
        return ""

# Main function
def main():
    # Set title and description
    st.title("PDF Chatbot")

    # Create a sidebar for file upload
    st.sidebar.title("Upload PDF File")
    uploaded_file = st.sidebar.file_uploader("Choose a PDF file", type=['pdf'])

    # Text input for prompt
    prompt = st.text_input("Ask a Question", "")

    # Submit button
    submitted = st.button("Submit")

    if submitted:
        if uploaded_file is not None:
            # Extract text from uploaded PDF file
            pdf_text = extract_text_from_pdf(uploaded_file)
            if pdf_text:
                try:
                    # Create embeddings
                    embeddings = HuggingFaceEmbeddings()

                    # Split text into chunks
                    text_splitter = RecursiveCharacterTextSplitter(
                        chunk_size=1000,
                        chunk_overlap=20,
                        length_function=len,
                        is_separator_regex=False,
                    )
                    chunks = text_splitter.create_documents([pdf_text])

                    # Store chunks in ChromaDB
                    persist_directory = 'pdf_embeddings'
                    vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)
                    vectordb.persist()  # Persist ChromaDB
                    st.write("Embeddings stored successfully in ChromaDB.")
                    st.write(f"Persist directory: {persist_directory}")

                    # Load persisted Chroma database
                    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
                    st.write(vectordb)

                    # Perform question answering
                    if prompt:
                        docs = vectordb.similarity_search(prompt)
                        # st.write(docs[0])
                        text = docs[0].page_content
                        input_prompt = """You are an expert in understanding text contents. You will receive input PDF file and you will have to answer questions based on the input file."""
                        response = get_llm_response(input_prompt, text, prompt)
                        st.subheader("Generated Answer:")
                        st.write(response)
                except Exception as e:
                    st.error(f"Error occurred during text processing: {e}")

if __name__ == "__main__":
    main()
