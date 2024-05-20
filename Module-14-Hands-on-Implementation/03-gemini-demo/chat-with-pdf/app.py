import os
from dotenv import load_dotenv
import streamlit as st
import fitz  # PyMuPDF
import google.generativeai as genai


load_dotenv() #load all environment variables from .env

#configure api-key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load gemini pro vision model and get response
def get_gemini_response(role,content,prompt):  #input: how LLM model behave like, #image: To extract info, prompt: ask something
    # loading the gemini model
    model=genai.GenerativeModel('gemini-pro')
    response=model.generate_content([role,content,prompt]) #get response from model
    return response.text

#function to provide pdf
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
st.set_page_config(page_title="PDF Extractor")
st.header("Extract Information from your own PDF")
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
   # cont=read_pdf(uploaded_file)
    response=get_gemini_response(role,content,prompt)
    st.subheader("The response is..")
    st.write(response)
