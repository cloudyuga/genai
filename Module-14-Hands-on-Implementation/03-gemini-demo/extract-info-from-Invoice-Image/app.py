#Invoice Extractor
import os
from dotenv import load_dotenv
import streamlit as st
from PIL import Image   #add pillow in requirements.txt if it encounters an error
import google.generativeai as genai

#load all environment variables from .env
load_dotenv() 

#configure api-key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#function to load gemini pro vision model and get response
def get_gemini_response(input,image,prompt):  #input: how LLM model behave like, #image: To extract info, prompt: ask something
    # loading the gemini model
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input,image[0],prompt]) #get response from model
    return response.text

#function to provide image
def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        #read te file into byte
        bytes_data = uploaded_file.getvalue()        
        image_parts=[
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

#Streamlit App
st.set_page_config(page_title="Invoice Extractor")
st.header("Gemini Application")
#input=st.text_input("Ask question: ",key="input")
uploaded_file = st.file_uploader("choose an image...", type=["jpg","jpeg","png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True) 
input=st.text_input("Ask Question: ",key="input")
submit = st.button("Tell me about the invoice")
input_prompt="""
You are an expert in understanding invoices. you will receive input images as invoices and 
you will have to answer questions based on the input image.
"""
#if submit button is clicked,
if submit:
    image_data=input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The response is..")
    st.write(response)
