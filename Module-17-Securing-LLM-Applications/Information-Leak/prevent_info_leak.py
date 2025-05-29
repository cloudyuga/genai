# Your PDF contains sensitive info like Aadhar Number, The following app will not expose your sensitive data.
import os
import gradio as gr
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from openai import OpenAI

# Load environment variable
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# Function to extract text from PDF
def read_pdf(file_obj):
    reader = PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text.strip()

# Function to query OpenAI with context and question
def generate_answer(pdf_file, question):
    if pdf_file is None or question.strip() == "":
        return "Please upload a PDF and enter a valid question."

    context = read_pdf(pdf_file)

    system_prompt = (
        "You are an AI assistant designed to answer questions based on the provided document context.\n"
        "You must not expose any sensitive information such as Aadhar numbers, phone numbers, PAN, etc.\n"
        "If the user asks for such information, respond with: "
        "'Sorry, I cannot share sensitive personal information.'\n\n"
        f"Document Context:\n{context}\n\n"
        f"Question: {question}\nAnswer:"
    )

    try:
        response = client.responses.create(
            model="gpt-4",  # or "gpt-4o" or "gpt-3.5-turbo"
            input=[
                {"role": "system", "content": "You are a helpful assistant that answers based on PDF content."},
                {"role": "user", "content": system_prompt}
            ]
        )
        return response.output_text
    except Exception as e:
        return f"Error: {str(e)}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🔐 Safe PDF Question Answering (OpenAI GPT-4)")
    gr.Markdown("Upload a PDF and ask a question. The assistant won't reveal sensitive information like Aadhar numbers.")

    with gr.Row():
        pdf_input = gr.File(label="Upload PDF", file_types=[".pdf"])
        question_input = gr.Textbox(label="Ask a question")

    answer_output = gr.Textbox(label="Answer", lines=6)

    submit_btn = gr.Button("Get Answer")

    submit_btn.click(fn=generate_answer, inputs=[pdf_input, question_input], outputs=answer_output)

demo.launch()
