import gradio as gr
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the model
model = init_chat_model("gpt-4o-mini", model_provider="openai")

def finance_chatbot(question, level, history=None):
    # Prepare the system message to guide the behavior
    system_message = {
        "role": "system",
        "content": "You are a finance assistant. You can only respond to questions related to finance, retirement, insurance, stock, mutual funds etc. If a question is unrelated to finance, politely decline to answer. Provide your answer in 30 words only."
    }

    # Fixed template with correct variable names
    template = PromptTemplate(
        input_variables=["question", "level"],
        template="Answer the following finance question: {question}. Tailor your response for a {level} level understanding in a clear and engaging way."
    )

    # Use actual user inputs
    prompt = template.format(question=question, level=level)
    print(prompt)

    # Create a list of messages including the system message and user input
    messages = [system_message, {"role": "user", "content": prompt}]

    # Get the model response
    response = model.invoke(messages)

    # Extract the text from the response object and return it
    return response.content

with gr.Blocks() as demo:
    gr.Markdown("# Finance Assistance")

    with gr.Row():
        question = gr.Textbox(label="Your Question", lines=2, placeholder="Ask me any finance related...")
        level = gr.Dropdown(
            choices=["beginner", "intermediate", "advanced"],
            label="Choose level",
            value="beginner"
        )

    with gr.Row():
        submit_btn = gr.Button("Submit")
        clear_btn = gr.Button("Clear")

    output = gr.Textbox(label="AI Response", lines=4)
    status = gr.Textbox(label="Status", interactive=False)

    def on_submit(question, level):
        if not question.strip():
            return "Please enter a question", ""
        
        try:
            status_text = "Generating response..."
            response = finance_chatbot(question, level)
            return "Response generated successfully!", response
        except Exception as e:
            return f"Error: {str(e)}", ""

    submit_btn.click(on_submit, inputs=[question, level], outputs=[status, output])
    clear_btn.click(lambda: ("", "", ""), inputs=None, outputs=[question, output, status])

demo.launch()
