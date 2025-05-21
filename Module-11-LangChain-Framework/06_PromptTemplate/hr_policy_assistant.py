import gradio as gr
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from langchain_huggingface import HuggingFaceEmbeddings
import numpy as np

# ✅ Load API Keys
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

# ✅ Load Embedding Model
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ Define Knowledge Base
policy_documents = {
    "leave_policy": "Employees are entitled to 20 paid leave days per year. Additional unpaid leave can be requested with manager approval.",
    "work_hours": "Regular work hours are from 9 AM to 6 PM, Monday to Friday. Flexible work hours are allowed with prior approval.",
    "remote_work": "Employees can work remotely up to 3 days a week. Full remote work requires special approval.",
}

# ✅ Precompute Embeddings for Policies
policy_texts = list(policy_documents.values())
policy_embeddings = np.array(embeddings.embed_documents(policy_texts))  # Convert to NumPy array

# ✅ Function to Retrieve Context Using Similarity Search
def retrieve_context(query):
    """Find the most relevant policy using cosine similarity."""
    query_embedding = np.array(embeddings.embed_query(query))  # Convert query embedding to NumPy array
    
    # Compute cosine similarity
    similarities = np.dot(policy_embeddings, query_embedding)
    best_match_idx = np.argmax(similarities)

    return policy_texts[best_match_idx] if similarities[best_match_idx] > 0.5 else "No relevant policy found."

# ✅ Define Chat Prompt Template
prompt = ChatPromptTemplate.from_template(
    """You are a company HR assistant. Answer the question in 70 words, based only on the context provided.
Context: {context}
Question: {question}
If the extracted content and the query are not connected with each other, deny politely 
"""
)
# ✅ Initialize GPT-4o-mini Model
llm = ChatOpenAI(model="gpt-4o-mini", openai_api_key=api_key)

# ✅ Gradio Function
def ask_hr_assistant(question):
    context = retrieve_context(question)  # Retrieve the best matching policy
    response = prompt | llm | StrOutputParser()
    return response.invoke({"context": context, "question": question})

# ✅ Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🤖 HR Policy Assistant")
    gr.Markdown("Ask about company policies such as leave policy, work hours, or remote work.")

    user_input = gr.Textbox(label="Enter Your Question")
    submit_button = gr.Button("Ask HR Assistant")
    output_text = gr.Textbox(label="Response", interactive=False)

    submit_button.click(ask_hr_assistant, inputs=user_input, outputs=output_text)

# ✅ Run Gradio App
demo.launch()
