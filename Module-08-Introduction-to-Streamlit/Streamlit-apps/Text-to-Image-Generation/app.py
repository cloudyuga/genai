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
    
# Set Streamlit app title
st.title("Text to Image Generation App")

# Text input for prompt
input_text = st.text_input("Enter your image description:", "")

# Button to generate image
if st.button("Generate Image"):
    # Generate image based on the prompt
    img = generate_image(input_text)
    
    # Display the generated image
    st.image(img, caption="Generated Image")
