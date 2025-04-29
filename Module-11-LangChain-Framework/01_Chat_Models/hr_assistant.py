import gradio as gr
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load environment variables
load_dotenv()
api_key=os.getenv("OPENAI_API_KEY")
# Initialize the model with system_message
model = ChatOpenAI(
    model="gpt-4o-mini", 
    openai_api_key=api_key
)

# Define the HR chatbot function
def hr_chatbot(message, history=None):
    # Prepare the system message to guide the behavior
    system_message = {
        "role": "system", 
        "content": "You are an HR assistant. You can only respond to questions related to HR policies, employee benefits, recruitment, and workplace guidelines. If a question is unrelated to HR, politely decline to answer."
    }

    # Create a list of messages including the system message and user input
    messages = [system_message, {"role": "user", "content": message}]
    
    # Get the model response
    response = model.invoke(messages)

    # Extract the text from the response object and return it
    return response.content

# Define the Gradio UI with the updated chatbot type
with gr.Blocks() as demo:
    gr.Markdown("## HR Assistant Chatbot")
    chatbot = gr.ChatInterface(fn=hr_chatbot, title="HR Assistant", type="messages")

demo.launch()
