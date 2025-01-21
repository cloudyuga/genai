import gradio as gr
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")  # Ensure you have the OpenAI API key in .env
client = OpenAI(api_key=api_key)

# Function to query OpenAI for content summary
def generate_summary(text, model="gpt-4o-mini"):
    try:
        # Call OpenAI's API for text summarization
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Please summarize the following content in 30 words ."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content # Direct access to the message content
    except Exception as e:
        return f"Error: {e}"

# Gradio app layout
with gr.Blocks() as demo:
    gr.Markdown("# Content Summarizer")
    gr.Markdown("### Paste text, and the app will generate a summary for you.")
    
    
    # Text input area
    text_input = gr.Textbox(label="Paste Your Text Here", lines=10)
    
    # Output area for the summary
    summary_output = gr.Textbox(label="Summary", lines=5)
    
    # Button to generate the summary
    generate_button = gr.Button("Generate Summary")
    
    # Logic to handle text input and generate the summary
    def handle_input(text):
        if text.strip():
            # Generate summary
            summary = generate_summary(text)
            return summary
        else:
            return "Please enter some text to summarize."

    generate_button.click(fn=handle_input, inputs=[text_input], outputs=summary_output)

# Launch the Gradio app
demo.launch()

