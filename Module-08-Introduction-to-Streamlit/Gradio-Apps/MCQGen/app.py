import os
import json
import pandas as pd
from dotenv import load_dotenv
import gradio as gr
from utils import get_table_data, read_data_from_url
from MCQGen import generate_evaluate_chain

# Load environment variables
load_dotenv()

# Loading JSON file
with open('./response.json', 'r', encoding="utf-8") as file:
    RESPONSE_JSON = json.load(file)

def create_mcqs(hf_token, url_add, mcq_count, tone):
    os.environ["HF_TOKEN"] = hf_token  # Set HF_TOKEN from input
    if url_add and mcq_count and tone:
        text = read_data_from_url(url_add)
        response = generate_evaluate_chain(
            {
                "text": text,
                "number": mcq_count,
                "tone": tone,
                "response_json": json.dumps(RESPONSE_JSON)
            }
        )
        if isinstance(response, dict):
            quiz = response.get("quiz", None)
            if quiz:
                table_data = get_table_data(quiz)
                if table_data is not None:
                    df = pd.DataFrame(table_data)
                    df.index = df.index + 1
                    review = response.get("review", "")
                    return df, review
                else:
                    return "Error in the table data", ""
            else:
                return "No quiz found in the response.", ""
        else:
            return "No response found", ""
    else:
        return "Please fill in all fields.", ""

# Define the Gradio interface
interface = gr.Interface(
    fn=create_mcqs,
    inputs=[
        gr.Textbox(label="HuggingFace API Token", type="password"),  # Add HF_TOKEN input
        gr.Textbox(label="URL"),
        gr.Number(label="No. of MCQ"),
        gr.Textbox(label="Complexity level of Questions")
    ],
    outputs=[
        gr.Dataframe(label="Generated MCQs"),
        gr.Textbox(label="Review")
    ],
    title="MCQ Creator Application with LangChain"
)

# Launch the Gradio app
if __name__ == "__main__":
    interface.launch()
