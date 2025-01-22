import gradio as gr
from openai import OpenAI
import os
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")  # Ensure your OpenAI API key is stored in the .env file
client = OpenAI(api_key=api_key)

# Define the paragraph as a global variable
paragraph = """Artificial Intelligence (AI) refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. AI systems can perform tasks such as recognizing speech, understanding natural language, making decisions, and identifying patterns. These systems are powered by algorithms and vast amounts of data, enabling them to improve their performance over time. AI has a wide range of applications, including autonomous vehicles, medical diagnostics, customer service, and more. As AI continues to evolve, it holds the potential to revolutionize industries and change the way humans interact with technology. 
            Machine Learning (ML) is a subset of Artificial Intelligence that focuses on the development of algorithms that allow computers to learn from and make predictions or decisions based on data. Unlike traditional programming, where a developer explicitly tells the computer how to perform tasks, ML algorithms improve their performance by analyzing patterns and making adjustments without human intervention. ML is widely used in applications such as recommendation systems, fraud detection, image recognition, and natural language processing. The field continues to grow rapidly, driven by advancements in computational power, data availability, and algorithmic improvements."""


# Function to generate embeddings
def get_embeddings(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-ada-002"  # Using a more efficient embedding model
    )
    return np.array(response.data[0].embedding)

# Function to retrieve relevant part of the paragraph based on the query
def retrieve_relevant_paragraph(paragraph, question):
    # Get the embeddings of the paragraph and question
    paragraph_embedding = get_embeddings(paragraph)
    question_embedding = get_embeddings(question)
    
    # Compute cosine similarity between the paragraph and question embeddings
    similarity = cosine_similarity([question_embedding], [paragraph_embedding])[0][0]
    
    # Return the similarity score (you can use this to decide how relevant the paragraph is)
    if similarity > 0.7:
        return paragraph  # If the paragraph is relevant enough, return the full paragraph
    else:
        return "The question does not match the paragraph well enough."

# Function to generate response from OpenAI based on the context
def generate_response(question):
    relevant_paragraph = retrieve_relevant_paragraph(paragraph, question)
    print(relevant_paragraph)
    if relevant_paragraph == "The question does not match the paragraph well enough.":
        return relevant_paragraph
    else:
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. Answer questions based on the provided paragraph in 30 words."},
                    {"role": "user", "content": f"Here is the paragraph: {relevant_paragraph}\n\nQuestion: {question}"}
                ]
            )
            # Extract the response
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error: {e}"

# Gradio app
with gr.Blocks() as app:
    gr.Markdown("# Chat with a Paragraph 📄🤖")
    
    # Display the paragraph stored in the global variable
    gr.Markdown(f"### Paragraph: \n{paragraph}")
    
    # User input for the question
    question = gr.Textbox(label="Ask a Question", placeholder="Ask a question about the paragraph...")
    
    # Button to trigger the response generation
    submit_button = gr.Button("Get Answer")
    
    # Output text area for the response
    answer = gr.Textbox(label="Answer", interactive=False)

    # Define the button click behavior
    submit_button.click(generate_response, inputs=[question], outputs=answer)

# Launch the Gradio app
app.launch()
