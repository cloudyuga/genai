import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")  # Make sure to have your OpenAI API key in .env
client = OpenAI(api_key=api_key)

# Function to query OpenAI for MCQs
def generate_mcq(paragraph, num_mcqs, model="gpt-4o-mini"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"You are a helpful assistant. Please generate {num_mcqs} multiple-choice questions (MCQs) based on the provided paragraph."},
                {"role": "user", "content": f"Here is a paragraph: {paragraph}"}
            ]
        )
        # Correct way to access the content of the response
        return response.choices[0].message.content  # Direct access to message content
    except Exception as e:
        return f"Error: {e}"

# Streamlit app
st.title("Generate MCQs from a Paragraph")

# User input for paragraph
paragraph = st.text_area("Enter a paragraph:")

# Ask user for the number of MCQs to generate
num_mcqs = st.slider("Select the number of MCQs to generate:", min_value=1, max_value=10, value=3)

# Handle user input and display the MCQs
if st.button("Generate MCQs"):
    if paragraph.strip():
        # Get MCQs from OpenAI API
        mcq_response = generate_mcq(paragraph, num_mcqs)

        # Display the MCQs
        st.write("**Generated MCQs:**")
        st.write(mcq_response)
    else:
        st.warning("Please enter a paragraph.")
