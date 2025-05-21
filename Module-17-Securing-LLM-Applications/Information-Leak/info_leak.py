# Your PDF contains Sensitive Info like Aadhar Number. The following app will display all the information.
import os
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize the HuggingFace endpoint
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=HF_TOKEN.strip(),
    temperature=0.7,
    max_new_tokens=200
)

# Function to read PDF and extract text
def read_pdf(file_path):
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

# Function to generate answers from the text using LLM
def generate_answer(question, context):
    # System prompt to instruct the LLM
    system_prompt = """
    You are an AI assistant designed to answer questions based on the provided text. 
    
    Here is the context extracted from the document:
    {context}

    Now, answer the following question based on the provided context:

    Question: {question}
    Answer:
    """
    
    # Format the prompt
    input_text = system_prompt.format(context=context, question=question)
    return llm(input_text)

# Streamlit UI
st.title("PDF Question Answering System")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    with st.spinner("Processing..."):
        # Read and process the PDF
        pdf_text = read_pdf(uploaded_file)
        
        st.sidebar.subheader("PDF Data")
        st.sidebar.write(pdf_text)
        # Ask a question about the PDF
        question = st.text_input("Ask a question about the PDF:")
        
        if st.button("Get Answer"):
            if question:
                # Generate answer using LLM with the system prompt
                answer = generate_answer(question, pdf_text)
                st.subheader("Answer")
                st.write(answer)
            else:
                st.error("Please enter a question.")
