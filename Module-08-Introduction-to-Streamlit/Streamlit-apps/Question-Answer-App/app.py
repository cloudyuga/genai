import streamlit as st
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")  # Make sure to have your OpenAI API key in .env
client = OpenAI(api_key=api_key)

# Function to query OpenAI
def query_openai(question, model="gpt-4o-mini"):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Please answer in 30 words"},
                {"role": "user", "content": question}
            ]
        )
        # Correct way to access message content
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Streamlit app
st.title("Simple Q&A Application")

# User input for asking questions
question = st.text_input("Ask your question:")

# Handle user input and display the answer
if st.button("Get Answer"):
    if question.strip():
        # Get answer from OpenAI API
        answer = query_openai(question)

        # Display the answer
        st.write(f"**Answer:** {answer}")
    else:
        st.warning("Please enter a question.")
