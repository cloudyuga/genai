# app.py
import gradio as gr
import os
from PIL import Image
import requests
from io import BytesIO
from openai import OpenAI 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")  # Ensure your OpenAI API key is stored in the .env file
client = OpenAI(api_key=api_key)

from io import BytesIO

# Initialize OpenAI client
client = OpenAI()

def generate_image(input_text):
    # Call OpenAI's DALL·E 3 model for image generation
    response = client.images.generate(
        model="dall-e-2",
        prompt=input_text,
        size="256x256",
        quality="standard",
        n=1
    )
    # Extract the image URL from the response
    image_url = response.data[0].url
    
    # Fetch the image from the URL
    image_response = requests.get(image_url)
    img = Image.open(BytesIO(image_response.content))
    
    return img

# Create a Gradio interface
def create_interface():
    with gr.Blocks() as demo:
        gr.Markdown("# Text to Image Generation App with OpenAI")  # Title
        
        with gr.Row():
            # Textbox for user input
            input_text = gr.Textbox(label="Enter your image description:")
            
            # Button to generate image
            generate_btn = gr.Button("Generate Image")
        
        # Image output
        image_output = gr.Image(label="Generated Image", type="pil")

        # Define the interaction: When the button is clicked, generate the image
        generate_btn.click(generate_image, inputs=input_text, outputs=image_output)

    return demo

# Launch the Gradio app
if __name__ == "__main__":
    demo = create_interface()
    demo.launch()
