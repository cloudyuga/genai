#Add same files in project directory as we added in MCQGen gradio App
#MCQGen.py
#response.json
#requirements.txt (remove gradio and add streamlit)
#utils.py
import os
import json
import pandas as pd
from dotenv import load_dotenv
from utils import get_table_data, read_data_from_url
import streamlit as st
from MCQGen import generate_evaluate_chain

# loading JSON file
with open('./response.json','r', encoding="utf-8") as file:
    RESPONSE_JSON = json.load(file)

#create a title
st.title("MCQ Creator Application with langchain")

#create a form using st.form
with st.form("user_inputs"):
    #file upload
    # uploaded_file=st.file_uploader("upload a pdf or text file")
    url_add=st.text_input("URL", max_chars=100)
    #input fields
    mcq_count=st.number_input("No. of MCQ", min_value=3, max_value=50)
    #quiz tone
    tone=st.text_input("Complexity level of Questions", max_chars=20, placeholder="simple")
    # Add button
    button=st.form_submit_button("Create MCQs")

    #check if the button is clicked and all fields have input
    if button and url_add is not None and mcq_count and tone:
        with st.spinner("loading..."):
            text = read_data_from_url(url_add)
            response=generate_evaluate_chain(
                {
                "text": text,
                "number": mcq_count,
                "tone": tone,
                "response_json": json.dumps(RESPONSE_JSON)
                }
            )
            if isinstance(response, dict):
                # Extract quiz data from the response
                quiz = response.get("quiz", None)
                if quiz:
                   table_data = get_table_data(quiz)
                   if table_data is not None:
                       df = pd.DataFrame(table_data)
                       df.index = df.index + 1
                       st.table(df)
                       # Display the review in a textbox as well
                       st.text_area(label="Review", value=response.get("review", ""))
                   else:
                       st.error("Error in the table data")
                else:
                    st.error("No quiz found in the response.")
            else:
                st.write("No response found")
