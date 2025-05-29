import gradio as gr
import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the model
model = init_chat_model("gpt-4o-mini", model_provider="openai")

# Create the prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a finance assistant. Only answer finance-related questions about investments, banking, budgeting, etc. Keep answers under 50 words."),
    ("human", "Question: {question}\nLevel: {level}")
])

# Create output parser
parser = StrOutputParser()

# Method 1: Traditional approach (without LCEL)
def finance_chatbot_traditional(question, level):
    # Format the prompt
    messages = prompt.format_messages(question=question, level=level)
    
    # Get response from model
    response = model.invoke(messages)
    
    # Parse the output
    final_answer = parser.invoke(response)
    
    return final_answer

# Method 2: LCEL Chain approach
def create_finance_chain():
    """Create a simple LCEL chain"""
    chain = prompt | model | parser
    return chain

# Initialize the chain
finance_chain = create_finance_chain()

def finance_chatbot_lcel(question, level):
    """Use LCEL chain to process the request"""
    # Prepare input
    inputs = {"question": question, "level": level}
    
    # Invoke the chain - this does all steps at once!
    response = finance_chain.invoke(inputs)
    
    return response

with gr.Blocks() as demo:
    gr.Markdown("# Simple Finance Assistant with LCEL")
    gr.Markdown("Compare traditional approach vs LCEL chain approach")

    with gr.Tabs():
        with gr.TabItem("LCEL Chain (Recommended)"):
            gr.Markdown("**Using LCEL Chain: `prompt | model | parser`**")
            
            question1 = gr.Textbox(
                label="Your Finance Question",
                placeholder="e.g., What is compound interest?",
                lines=2
            )
            level1 = gr.Dropdown(
                choices=["beginner", "intermediate", "advanced"],
                label="Level",
                value="beginner"
            )
            
            submit1 = gr.Button("Ask (LCEL Chain)", variant="primary")
            output1 = gr.Textbox(label="Response", lines=3)

        with gr.TabItem("Traditional Approach"):
            gr.Markdown("**Traditional step-by-step approach**")
            
            question2 = gr.Textbox(
                label="Your Finance Question",
                placeholder="e.g., How should I start investing?",
                lines=2
            )
            level2 = gr.Dropdown(
                choices=["beginner", "intermediate", "advanced"],
                label="Level",
                value="beginner"
            )
            
            submit2 = gr.Button("Ask (Traditional)", variant="secondary")
            output2 = gr.Textbox(label="Response", lines=3)

        with gr.TabItem("Code Comparison"):
            gr.Markdown("""
            ## Traditional Approach (Multiple Steps):
            ```python
            def finance_chatbot_traditional(question, level):
                # Step 1: Format the prompt
                messages = prompt.format_messages(question=question, level=level)
                
                # Step 2: Get response from model  
                response = model.invoke(messages)
                
                # Step 3: Parse the output
                final_answer = parser.invoke(response)
                
                return final_answer
            ```
            
            ## LCEL Chain Approach (One Line):
            ```python
            # Create chain
            chain = prompt | model | parser
            
            def finance_chatbot_lcel(question, level):
                # Single step - chain handles everything!
                response = chain.invoke({"question": question, "level": level})
                return response
            ```
            
            ## Benefits of LCEL:
            - **Simpler**: One line instead of multiple steps
            - **Cleaner**: Uses `|` operator like Unix pipes  
            - **Efficient**: Optimized execution
            - **Readable**: Clear data flow from left to right
            """)

    def on_lcel_submit(question, level):
        if not question.strip():
            return "Please enter a question"
        try:
            return finance_chatbot_lcel(question, level)
        except Exception as e:
            return f"Error: {str(e)}"

    def on_traditional_submit(question, level):
        if not question.strip():
            return "Please enter a question"
        try:
            return finance_chatbot_traditional(question, level)
        except Exception as e:
            return f"Error: {str(e)}"

    # Event handlers
    submit1.click(on_lcel_submit, inputs=[question1, level1], outputs=[output1])
    submit2.click(on_traditional_submit, inputs=[question2, level2], outputs=[output2])

demo.launch()
