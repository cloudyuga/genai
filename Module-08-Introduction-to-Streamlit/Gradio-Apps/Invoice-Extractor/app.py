import gradio as gr
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API key for Google Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to process the image and get response from Gemini model
def get_gemini_response(uploaded_file_path, query):
    try:
        # Define input prompt
        input_prompt = """
        You are an expert in understanding invoices. You will receive input images as invoices and 
        you will have to answer questions based on the input image.
        """
        # Validate the image file path
        if not uploaded_file_path or not os.path.exists(uploaded_file_path):
            return "Please upload a valid image."

        # Read the image file as binary data
        with open(uploaded_file_path, "rb") as f:
            image_data = f.read()

        # Prepare the image parts for the model
        mime_type = f"image/{uploaded_file_path.split('.')[-1]}"  # Dynamically detect mime type
        image_parts = [{"mime_type": mime_type, "data": image_data}]

        # Load the Gemini model and get the response
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([input_prompt, image_parts[0], query])
        return response.text
    except Exception as e:
        return f"Error: {e}"


# Define Gradio interface
with gr.Blocks() as invoice_extractor:
    gr.Markdown("# Invoice Extractor")
    gr.Markdown(
        """
        Upload an invoice image and ask specific questions about it. 
        The system uses Google's Gemini model to extract and interpret the invoice details.
        """
    )
    image_input = gr.Image(label="Upload Invoice Image", type="filepath")  # Use type="filepath"
    query_input = gr.Textbox(label="Enter your query about the invoice", placeholder="e.g., What is the total amount?")
    output_response = gr.Textbox(label="Response", lines=5)

    # Button to process the image and query
    submit_btn = gr.Button("Process Invoice")

    # Set the button to call the processing function
    submit_btn.click(
        get_gemini_response, 
        inputs=[image_input, query_input],
        outputs=output_response
    )

# Launch the app
invoice_extractor.launch()
