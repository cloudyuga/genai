import gradio as gr
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

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

# Create the prompt template
chat_template = ChatPromptTemplate.from_messages([
    ("system", "You are a {domain} assistant. You can only respond to questions related to {domain_context}. If a question is unrelated to {domain}, politely decline to answer. Provide your answer in 30 words only."),
    ("human", "Answer the following {domain} question: {question}. Tailor your response for a {level} level understanding in a clear and engaging way.")
])

# Create output parser
output_parser = StrOutputParser()

# Helper function to add domain context
def add_domain_context(inputs):
    """Add domain-specific context to the input dictionary"""
    domain = inputs.get("domain", "Finance")
    domain_context = DOMAIN_CONTEXTS.get(domain, "general topics")
    return {**inputs, "domain_context": domain_context}

# Helper function for logging
def log_input(inputs):
    """Log the input for debugging"""
    print(f"Processing: Domain={inputs.get('domain')}, Level={inputs.get('level')}, Question={inputs.get('question')[:50]}...")
    return inputs

# Helper function for response validation
def validate_response(response):
    """Validate and potentially modify the response"""
    if len(response.split()) > 35:  # If response is too long
        print("Warning: Response exceeded 30 words limit")
    return response

# Create the LCEL chain
def create_chain():
    """Create an LCEL chain for processing requests"""
    chain = (
        RunnablePassthrough.assign(domain_context=RunnableLambda(add_domain_context))
        | RunnableLambda(log_input)
        | chat_template
        | model
        | output_parser
        | RunnableLambda(validate_response)
    )
    return chain

# Alternative chain with error handling
def create_chain_with_error_handling():
    """Create an LCEL chain with built-in error handling"""
    def safe_invoke(inputs):
        try:
            return chain.invoke(inputs)
        except Exception as e:
            return f"Error processing request: {str(e)}"
    
    chain = (
        RunnablePassthrough.assign(domain_context=RunnableLambda(add_domain_context))
        | RunnableLambda(log_input)
        | chat_template
        | model
        | output_parser
        | RunnableLambda(validate_response)
    )
    
    return RunnableLambda(safe_invoke)

# Initialize the chain
main_chain = create_chain()

def multi_domain_chatbot_with_chain(question, level, domain, history=None):
    """Use LCEL chain to process the request"""
    # Prepare input dictionary
    inputs = {
        "question": question,
        "level": level,
        "domain": domain
    }
    
    # Invoke the chain
    response = main_chain.invoke(inputs)
    return response

# Alternative batch processing function
def batch_process_questions(questions_data):
    """Process multiple questions using batch invoke"""
    responses = main_chain.batch(questions_data)
    return responses

with gr.Blocks() as demo:
    gr.Markdown("# Multi-Domain Assistant with LCEL Chains")
    gr.Markdown("Ask questions about Finance, HR, or Sports. Now powered by LangChain Expression Language (LCEL) chains!")

    with gr.Tabs():
        with gr.TabItem("Single Query"):
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

        with gr.TabItem("Batch Processing"):
            gr.Markdown("Process multiple questions at once using batch invoke")
            
            batch_input = gr.Textbox(
                label="Batch Questions (JSON format)",
                lines=8,
                placeholder='[{"question": "What is compound interest?", "level": "beginner", "domain": "Finance"}, {"question": "How to hire good employees?", "level": "intermediate", "domain": "HR"}]',
                value='[{"question": "What is compound interest?", "level": "beginner", "domain": "Finance"}, {"question": "How to hire good employees?", "level": "intermediate", "domain": "HR"}]'
            )
            
            batch_submit_btn = gr.Button("Process Batch", variant="primary")
            batch_output = gr.Textbox(label="Batch Results", lines=10)

        with gr.TabItem("Chain Information"):
            gr.Markdown("""
            ## LCEL Chain Components Used:
            
            1. **RunnablePassthrough.assign()** - Adds domain context to inputs
            2. **RunnableLambda** - Custom functions for logging and validation  
            3. **ChatPromptTemplate** - Formats the conversation
            4. **LLM Model** - Processes the request
            5. **StrOutputParser** - Extracts string response
            6. **Chain Composition** - Uses `|` operator to connect components
            
            ## Chain Flow:
            Input → Add Context → Log → Format Prompt → LLM → Parse → Validate → Output
            """)

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
            status_text = "Processing with LCEL chain..."
            response = multi_domain_chatbot_with_chain(question, level, domain)
            return "Response generated successfully using LCEL!", response
        except Exception as e:
            return f"Error: {str(e)}", ""

    def on_batch_submit(batch_input_text):
        try:
            import json
            questions_data = json.loads(batch_input_text)
            responses = batch_process_questions(questions_data)
            
            # Format results
            results = []
            for i, (question_data, response) in enumerate(zip(questions_data, responses)):
                results.append(f"Q{i+1} [{question_data['domain']}-{question_data['level']}]: {question_data['question']}")
                results.append(f"A{i+1}: {response}")
                results.append("-" * 50)
            
            return "\n".join(results)
        except json.JSONDecodeError:
            return "Error: Invalid JSON format"
        except Exception as e:
            return f"Error processing batch: {str(e)}"

    # Event handlers
    domain.change(update_placeholder, inputs=[domain], outputs=[question])
    submit_btn.click(on_submit, inputs=[question, level, domain], outputs=[status, output])
    clear_btn.click(lambda: ("", "", ""), inputs=None, outputs=[question, output, status])
    batch_submit_btn.click(on_batch_submit, inputs=[batch_input], outputs=[batch_output])

demo.launch()
