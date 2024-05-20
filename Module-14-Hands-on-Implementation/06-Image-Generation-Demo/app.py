#app.py
import streamlit as st
from PIL import Image
import torch
from diffusers import StableDiffusionPipeline

def generate_image(input_text):
    # Load Diffusion pipeline
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32)
    # Generate image from text prompt
    prompt = input_text
    generated_image = pipe(prompt).images[0]
    return generated_image
   
st.title("Text to Image Generation App")# Set Streamlit app title
input_text = st.text_input("Enter your image description:", "")# Text input for prompt
if st.button("Generate Image"):# Button to generate image
    # Generate image based on the prompt
    img = generate_image(input_text)
    # Display the generated image
    st.image(img, caption="Generated Image")
