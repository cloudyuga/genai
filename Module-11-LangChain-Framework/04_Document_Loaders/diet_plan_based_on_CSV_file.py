import os
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import CSVLoader
from dotenv import load_dotenv

# ✅ Load API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Load CSV Data
csv_file = "./user_details.csv"  # Ensure this file is in the same directory
loader = CSVLoader(file_path=csv_file)
data = loader.load()

# ✅ Process CSV Data
def parse_csv_data():
    user_data = {}
    for doc in data:
        content_lines = doc.page_content.split("\n")
        details = {k.strip(): v.strip() for k, v in (line.split(":") for line in content_lines)}
        user_data[details["Name"]] = details
    return user_data

user_data_dict = parse_csv_data()
names_list = list(user_data_dict.keys())

# ✅ Initialize OpenAI Model
model = ChatOpenAI(
    model="gpt-4o-mini",
    openai_api_key=api_key
)

# ✅ Function to Retrieve Data & Generate Diet Plan
def get_user_data_and_diet(name):
    if name not in user_data_dict:
        return "User not found.", ""

    details = user_data_dict[name]
    user_info = (
        f"Age: {details['Age']}, Gender: {details['Gender']}, "
        f"Height: {details['Height_cm']}cm, Weight: {details['Weight_kg']}kg, "
        f"Activity Level: {details['Activity_Level']}"
    )

    prompt = (f"Suggest a 50-word diet plan for {details['Name']} ({details['Age']} years, {details['Gender']}), "
              f"who is {details['Activity_Level']}, weighs {details['Weight_kg']}kg and is {details['Height_cm']}cm tall.")

    response = model.invoke(prompt)
    return user_info, response.content

# ✅ Function to Reset Outputs When Changing Selection
def reset_outputs(_):
    return "", ""  # Clears user details and diet plan

# ✅ Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🍽️ Personalized Diet Plan Generator")

    name_input = gr.Dropdown(label="Select Name", choices=names_list)
    user_data_output = gr.Textbox(label="User Details", interactive=False)
    diet_output = gr.Textbox(label="Diet Plan", interactive=False)
    generate_button = gr.Button("Generate Diet Plan")

    # ✅ Clears previous output when selecting a new user
    name_input.change(reset_outputs, inputs=name_input, outputs=[user_data_output, diet_output])

    # ✅ Generates data on button click
    generate_button.click(get_user_data_and_diet, inputs=name_input, outputs=[user_data_output, diet_output])

# ✅ Run the App
demo.launch()
