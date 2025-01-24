import gradio as gr
from together import Together
from guardrail import is_safe
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = Together(api_key=api_key)

# Function to handle user questions and provide safe answers
def get_answer(question, history):
    # Subject-specific prompt
    subject_prompt = """You are an AI teacher specializing in helping students under 16.
    You can only answer questions about the following subjects: Math, Science, Geography, History, and English.
    Instructions:
    - Do NOT answer questions about sports, movies, entertainment, or other unrelated topics.
    - Use simple, clear, and positive language.
    - Avoid lengthy or irrelevant explanations.
    Examples of allowed questions:
    - What is 8 x 7?
    - Explain photosynthesis.
    - What is the capital of France?
    Examples of disallowed questions:
    - Who won the 2011 Cricket World Cup?
    - Tell me about the latest Marvel movie.
    - What's the score of the last football game?
    If a question is disallowed, respond: 'I can only answer questions about Math, Science, Geography, History, or English.'"""

    # Check if the question is safe
    if not is_safe(question):
        return "Your question contains inappropriate content. Please ask about Math, Science, Geography, History, or English."

    # Generate response
    messages = [
        {"role": "system", "content": subject_prompt},
        {"role": "user", "content": question}
    ]
    response = client.chat.completions.create(
        model="meta-llama/Llama-3-70b-chat-hf",
        temperature=0.7,
        messages=messages,
    )
    answer = response.choices[0].message.content.strip()

    # Check if the answer is safe
    if not is_safe(question, answer):
        return "The generated response violated the safety policy and cannot be displayed."

    return answer

# Gradio interface function
def main_loop(question, history):
    # Validate user question
    if not is_safe(question):
        return "Your question contains inappropriate content. Please ask about Math, Science, Geography, History, or English."

    # Get response and validate
    response = get_answer(question, history)
    return response

# Gradio Interface
demo = gr.ChatInterface(
    fn=main_loop,  # Function that processes each interaction
    chatbot=gr.Chatbot(
        height=350,
        placeholder="Ask a question from Math, Science, Geography, History, or English.",
        type="messages",
    ),
    textbox=gr.Textbox(
        placeholder="Enter your question here.",
        container=False,
        scale=7,
    ),
    title="Education Chatbot: Your Personal AI Teacher",
    theme="huggingface",
    examples=["What is the capital of France?", "What is 8 x 7?", "Explain photosynthesis."],
    cache_examples=False,
    css='''
    .gradio-container {
        background-color: #F8FAFC;
        padding: 30px;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    }
    .gradio-title {
        font-size: 28px;
        font-weight: bold;
        color: #333333;
        text-align: center;
        margin-bottom: 20px;
    }
    .gr-textbox input {
        background-color: #FFFFFF;
        border: 2px solid #cccccc;
        border-radius: 10px;
        padding: 12px;
        font-size: 16px;
        color: #333;
        width: 100%;
    }
    .gr-chatbot {
        background-color: #ffffff;
        border-radius: 10px;
        border: 1px solid #dddddd;
        padding: 15px;
    }
    .gr-button {
        background-color: #007BFF;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
        transition: background-color 0.3s;
    }
    .gr-button:hover {
        background-color: #0056b3;
    }
    .gr-chatbot .message {
        font-size: 16px;
        line-height: 1.6;
    }
    '''
)

# Launch the Gradio app
demo.launch(share=True, server_name="0.0.0.0")
