# Example URL: https://cloudyuga.guru/blogs/beyond-boundaries-the-artistry-of-generative-ai/
import os
import gradio as gr
from langchain_openai import ChatOpenAI
from langchain_community.document_loaders import WebBaseLoader
from dotenv import load_dotenv

# ✅ Load OpenAI API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Initialize OpenAI Model
model = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)

# ✅ Extract Web Content
def extract_text_from_web(url):
    """Fetch and extract text from a given web URL."""
    loader = WebBaseLoader(url)
    docs = loader.load()
    
    if docs:
        return docs[0].page_content  # Return main page content
    return "Could not extract content from the provided URL."

# ✅ Generate Summary
def generate_summary(text):
    """Generate a concise summary of the given text."""
    messages = [
        {"role": "system", "content": "You are a helpful AI that summarizes content."},
        {"role": "user", "content": f"Summarize the following text in 70 words:\n\n{text}"}
    ]
    response = model.invoke(messages)
    return response.content

# ✅ Generate MCQs
def generate_mcqs(text):
    """Generate multiple-choice questions (MCQs) based on the extracted text."""
    messages = [
        {"role": "system", "content": "You are a quiz creator. Generate 3 MCQs based on the given text."},
        {"role": "user", "content": f"Generate 3 MCQs from the following text:\n\n{text}"}
    ]
    response = model.invoke(messages)
    return response.content

# ✅ Gradio UI
def process_url(url):
    """Process the URL and return summary + MCQs."""
    extracted_text = extract_text_from_web(url)
    summary = generate_summary(extracted_text)
    mcqs = generate_mcqs(extracted_text)
    
    return summary, mcqs

with gr.Blocks() as demo:
    gr.Markdown("# 🌐 Web Content Extractor + AI Summary & MCQs")
    
    url_input = gr.Textbox(label="Enter Website URL", placeholder="https://example.com")
    summary_output = gr.Textbox(label="Summary", interactive=False)
    mcq_output = gr.Textbox(label="Generated MCQs", interactive=False)
    
    process_button = gr.Button("Generate Summary & MCQs")
    
    process_button.click(process_url, inputs=url_input, outputs=[summary_output, mcq_output])

# ✅ Run the Gradio App
demo.launch()
