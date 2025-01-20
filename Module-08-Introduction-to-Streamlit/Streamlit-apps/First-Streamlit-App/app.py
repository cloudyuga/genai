import streamlit as st

# Set the title of the app
st.title("Basic Streamlit App")

# Display a header
st.header("Welcome to Streamlit!")

# Add a text input widget
user_input = st.text_input("Enter your name:")

# Display the user's input
if user_input:
    st.write(f"Hello, {user_input}!")

# Add a slider widget
age = st.slider("Select your age:", 0, 100, 25)

# Display the selected age
st.write(f"You are {age} years old.")
