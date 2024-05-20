# Information Extractor
import os
import streamlit as st
import fitz  # PyMuPDF
from langchain_community.llms import Ollama

# function to load 'llama2' and get response
def get_ollama_response(role,content,prompt):  #input: how LLM model behave like, #content: PDF file info, prompt: ask something
    model=Ollama(model='llama2') # loading llama2 model
    response=model.invoke([role,content,prompt]) #get response from model
    return response

# function to provide pdf
def read_pdf(file):
    if file.name.endswith(".pdf"):
        try:
            text = ""
            doc = fitz.open(stream=file.getvalue(), filetype="pdf")
            for page in doc:
                text += page.get_text()
            return text
        except Exception as e:
            st.error("Error reading the PDF file")
            st.error(e)
            return None
    else:
        st.error("Invalid file format. Please upload a PDF file.")
        return None

#Streamlit App
st.set_page_config(page_title="Chat with PDF File")
st.header("Extract Information from PDF")
uploaded_file = st.file_uploader("choose a pdf file...", type=["pdf"])

if uploaded_file is not None:
    # Display uploaded file details
    st.subheader("Uploaded PDF File Details:")
    st.write("File Name:", uploaded_file.name)
    st.write("File Size:", len(uploaded_file.getvalue()), "bytes")

        # Read the content of the PDF file
    content = read_pdf(uploaded_file)

    if content:
        st.subheader("Extracted Text from PDF:")
        st.write(content)

prompt=st.text_input("Ask Question: ",key="input")
submit = st.button("Tell me about the PDF")
role="""
You are an expert in understanding text contents. you will receive input pdf file and 
you will have to answer questions based on the input file.
"""
#if submit button is clicked,
if submit:
    response=get_ollama_response(role,content,prompt)
    st.subheader("The response is..")
    st.write(response)
