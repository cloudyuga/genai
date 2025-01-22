import streamlit as st
import pandas as pd

# Set the title of the app
st.title("App with Form and File Upload")

# Display an image
st.image("./nadi-lok-image.png")

# Sidebar for file upload
st.sidebar.header("Upload CSV File")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

# Display the uploaded file's content if a file is uploaded
if uploaded_file:
    # Read the CSV file
    try:
        data = pd.read_csv(uploaded_file)
        st.sidebar.success("File uploaded successfully!")
        st.sidebar.write("Preview of the uploaded file:")
        st.sidebar.dataframe(data.head())  # Display the first few rows of the data
    except Exception as e:
        st.sidebar.error(f"Error reading file: {e}")

# Main app - Create a form
with st.form("user_form"):
    # Display a header
    st.header("Welcome to Streamlit Form!")

    # Add a text input widget
    user_input = st.text_input("Enter your name:")

    # Add a slider widget
    age = st.slider("Select your age:", 0, 100, 25)

    # Add form buttons
    submit_button = st.form_submit_button("Submit")

# Handle form submission
if submit_button:
    if user_input:
        st.success(f"Hello, {user_input}!")
        st.info(f"You are {age} years old.")
    else:
        st.error("Please enter your name.")
