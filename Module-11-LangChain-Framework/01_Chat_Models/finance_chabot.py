import gradio as gr
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
# Initialize the model with system_message
model = init_chat_model("gpt-4o-mini", model_provider="openai")


# Define the Finance chatbot function
def finance_chatbot(message, history=None):
    # Prepare the system message to guide the behavior
    system_message = {
        "role": "system", 
        "content": "You are a finance assistant. You can only respond to questions related to finance, retirement, insurance, stock, mutual funds etc. If a question is unrelated to finance, politely decline to answer. Provide your answer in 30 words only."
    }

    # Create a list of messages including the system message and user input
    messages = [system_message, {"role": "user", "content": message}]
    
    # Get the model response
    response = model.invoke(messages)

    # Extract the text from the response object and return it
    return response.content

# Define the Gradio UI with the updated chatbot type
with gr.Blocks() as demo:
    gr.Markdown("## Finance Assistant Chatbot")
    chatbot = gr.ChatInterface(fn=finance_chatbot, title="Finance Assistant", type="messages")

demo.launch()
