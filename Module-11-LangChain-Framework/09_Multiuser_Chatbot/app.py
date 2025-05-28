import os
import gradio as gr
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

# ✅ Load OpenAI API Key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# ✅ Initialize OpenAI Model with LangChain
model = ChatOpenAI(
    model="gpt-4o-mini", 
    openai_api_key=api_key
)

# ✅ Initialize HuggingFace Embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# ✅ Initialize Chroma Vector Store
vector_store = Chroma(
    collection_name="chat_collection",
    embedding_function=embeddings,
    persist_directory="./chroma_chat_db",
)

# ✅ Fetch Chat History (No Duplicates)
def get_chat_history(user_id):
    """Fetch stored messages for a user without duplicates."""
    retriever = vector_store.as_retriever(
        search_type="mmr",
        search_kwargs={"k": 100, "fetch_k": 100}
    )
    
    results = retriever.invoke("Chat history", filter={"user_id": user_id})
    
    if not results:
        return ""

    # ✅ Remove duplicate messages while maintaining order
    unique_messages = list(dict.fromkeys(doc.page_content for doc in results))
    
    return "\n".join(unique_messages) if unique_messages else ""

# ✅ Store Only Latest Chat Message (No Duplication)
def store_chat_message(user_id, user_input, bot_response):
    """Stores only the latest user-bot conversation in ChromaDB."""
    chat_entry = f"User: {user_input}\nBot: {bot_response}"
    
    # ✅ Store only the latest message instead of the whole history
    vector_store.add_documents([Document(page_content=chat_entry, metadata={"user_id": user_id})])

# ✅ Generate Response and Append to Top
def generate_response(username, user_input):
    """Generates chatbot response using GPT-4 and stores chat history correctly."""
    user_id = username.lower().strip()
    history = get_chat_history(user_id)
    
    messages = [{"role": "system", "content": "You are a helpful AI assistant. Please provide an answer in 20 words only."}]
    
    if history:
        messages.append({"role": "user", "content": f"Chat history:\n{history}"})
    
    messages.append({"role": "user", "content": user_input})
    
    # Generate response from OpenAI model
    response = model.invoke(messages)
    bot_response = response.content

    # ✅ Store only the latest user-input and bot-response
    store_chat_message(user_id, user_input, bot_response)
    
    # ✅ Return updated history with the latest message on top
    return f"User: {user_input}\nBot: {bot_response}\n\n{history}"

# ✅ Reset Outputs When Changing User
def reset_outputs(username, _):
    """Loads chat history for the selected user and clears input field."""
    user_id = username.lower().strip()
    chat_history = get_chat_history(user_id)  # Fetch chat history without duplicates
    return "", chat_history  # Clears input field and updates chat output

# ✅ Gradio UI with Fixes
with gr.Blocks() as demo:
    gr.Markdown("# 🔥 Multi-User Chatbot with GPT-4 and Memory (ChromaDB)")
    
    username_input = gr.Dropdown(label="Select User", choices=["Aarya", "Ved", "Vivaan"])
    chat_input = gr.Textbox(label="Your Message", placeholder="Type here...")
    chat_output = gr.Textbox(label="Chatbot History", interactive=False)
    chat_button = gr.Button("Send")

    # Load chat history when user selection changes
    username_input.change(reset_outputs, inputs=[username_input, chat_input], outputs=[chat_input, chat_output])

    # Send message and update chat history  
    chat_button.click(generate_response, inputs=[username_input, chat_input], outputs=chat_output)

# ✅ Run the Gradio app
demo.launch()
