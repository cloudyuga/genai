# app.py (Finance Chatbot)

import gradio as gr
from guardrail import is_safe
from together import Together
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = Together(api_key=api_key)

# Function to handle the chatbot's response to user queries
# You can only answer finance-related queries.
# - Do not answer non-finance questions.
def run_action(message, history):
    system_prompt = """You are a financial assistant. 
    - Answer in 50 words.
    - Ensure responses adhere to the safety policy."""

    messages = [{"role": "system", "content": system_prompt}]

    # Convert history into the appropriate format
    for entry in history:
        if entry["role"] == "user":
            messages.append({"role": "user", "content": entry["content"]})
        elif entry["role"] == "assistant":
            messages.append({"role": "assistant", "content": entry["content"]})

    # Add the user's current action
    messages.append({"role": "user", "content": message})

    # Get the model's response
    model_output = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        messages=messages,
    )

    return model_output.choices[0].message.content

# Main loop for the chatbot to handle user input
def main_loop(message, history):
    """
    Main loop for the chatbot to handle user input.
    """
    # Validate the user's input for safety
    if not is_safe(message):
        return "Your input violates our safety policy. Please try again with a finance-related query."
    
    # Generate and validate the response
    return run_action(message, history)

# Gradio Chat Interface
demo = gr.ChatInterface(
    main_loop,
    chatbot=gr.Chatbot(
        height=450,
        placeholder="Ask a finance-related question. Type 'exit' to quit.",
        type="messages",  # Proper rendering of chat format
    ),
    textbox=gr.Textbox(
        placeholder="What do you want to ask about finance?",
        container=False,
        scale=7,
    ),
    title="Finance Chatbot",
    theme="Monochrome",
    examples=["What is compound interest?", "How to save for retirement?", "What are tax-saving options?"],
    cache_examples=False,
)

# Launch the Gradio app
demo.launch(share=True, server_name="0.0.0.0")
