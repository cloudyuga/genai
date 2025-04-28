import gradio as gr
import torch
from diffusers import StableDiffusionPipeline

# Function to generate image from text
def generate_image(input_text):
    # Load Diffusion pipeline
    pipe = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32)
    # Generate image from text prompt
    prompt = input_text
    generated_image = pipe(prompt).images[0]
    return generated_image

# Gradio interface setup
iface = gr.Interface(
    fn=generate_image,
    inputs=gr.Textbox(lines=3, placeholder="Enter your image description", label="Image Description"),
    outputs=gr.Image(label="Generated Image", type="numpy"),  # Generated_image is a numpy array
    title="Text to Image Generation",
    description="Generate an image from a text description using Stable Diffusion Pipeline."
)

if __name__ == "__main__":
    iface.launch()
