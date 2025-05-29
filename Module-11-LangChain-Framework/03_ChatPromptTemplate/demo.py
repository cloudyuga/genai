import gradio as gr
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the model
model = init_chat_model("gpt-4o-mini", model_provider="openai")

# Domain-specific contexts
DOMAIN_CONTEXTS = {
    "Finance": "finance, retirement, insurance, stock, mutual funds, banking, investments, budgeting, taxes",
    "HR": "human resources, recruitment, employee relations, performance management, benefits, payroll, workplace policies",
    "Sports": "sports, athletics, fitness, training, nutrition, exercise, competition, health and wellness"
}

def multi_domain_chatbot(question, level, domain, history=None):
    # Get domain-specific context
    domain_context = DOMAIN_CONTEXTS.get(domain, "general topics")
    
    # Create ChatPromptTemplate with system and human message templates using variables
    chat_template = ChatPromptTemplate.from_messages([
        ("system", "You are a {domain} assistant. You can only respond to questions related to {domain_context}. If a question is unrelated to {domain}, politely decline to answer. Provide your answer in 30 words only."),
        ("human", "Answer the following {domain} question: {question}. Tailor your response for a {level} level understanding in a clear and engaging way.")
    ])

    # Format the prompt with user inputs
    formatted_prompt = chat_template.format_messages(
        domain=domain,
        domain_context=domain_context,
        question=question,
        level=level
    )
    
    print("Formatted messages:", formatted_prompt)

    # Get the model response
    response = model.invoke(formatted_prompt)

    # Extract the text from the response object and return it
    return response.content

with gr.Blocks() as demo:
    gr.Markdown("# Multi-Domain Assistant with ChatPromptTemplate")
    gr.Markdown("Ask questions about Finance, HR, or Sports based on your selected domain!")

    with gr.Row():
        with gr.Column():
            domain = gr.Dropdown(
                choices=["Finance", "HR", "Sports"],
                label="Choose Domain",
                value="Finance"
            )
            level = gr.Dropdown(
                choices=["beginner", "intermediate", "advanced"],
                label="Choose Level",
                value="beginner"
            )
        
        with gr.Column():
            question = gr.Textbox(
                label="Your Question", 
                lines=3, 
                placeholder="Ask me anything related to your selected domain..."
            )

    with gr.Row():
        submit_btn = gr.Button("Submit", variant="primary")
        clear_btn = gr.Button("Clear")

    output = gr.Textbox(label="AI Response", lines=4)
    status = gr.Textbox(label="Status", interactive=False)

    # Function to update placeholder text based on domain selection
    def update_placeholder(domain):
        placeholders = {
            "Finance": "e.g., How should I start investing? What is compound interest?",
            "HR": "e.g., How to conduct effective interviews? What are employee benefits?",
            "Sports": "e.g., How to improve running endurance? What is proper nutrition for athletes?"
        }
        return gr.Textbox(placeholder=placeholders.get(domain, "Ask me anything..."))

    def on_submit(question, level, domain):
        if not question.strip():
            return "Please enter a question", ""
        
        try:
            status_text = "Generating response..."
            response = multi_domain_chatbot(question, level, domain)
            return "Response generated successfully!", response
        except Exception as e:
            return f"Error: {str(e)}", ""

    # Update placeholder when domain changes
    domain.change(update_placeholder, inputs=[domain], outputs=[question])
    
    submit_btn.click(on_submit, inputs=[question, level, domain], outputs=[status, output])
    clear_btn.click(lambda: ("", "", ""), inputs=None, outputs=[question, output, status])

demo.launch()
