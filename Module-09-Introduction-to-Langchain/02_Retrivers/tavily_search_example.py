import gradio as gr
import os
from dotenv import load_dotenv
from langchain_community.retrievers import TavilySearchAPIRetriever

# Load environment variables (TAVILY_API_KEY should be set in .env file)
load_dotenv()

# Initialize Tavily retriever
retriever = TavilySearchAPIRetriever(api_key=os.getenv("TAVILY_API_KEY"))

# Function to fetch search results
def fetch_results(query):
    results = retriever.invoke(query)
    
    # Extract content and link properly
    formatted_results = [
        f"🔹 {doc.page_content}\n🔗 {doc.metadata.get('source', 'No link')}"
        for doc in results
    ]
    
    return "\n\n".join(formatted_results) if formatted_results else "No results found."

# Create Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("## 🔍 Tavily Search Chatbot")
    with gr.Row():
        query_input = gr.Textbox(label="Enter your search query:")
        search_button = gr.Button("Search")
    results_output = gr.Textbox(label="Search Results", interactive=False)

    search_button.click(fetch_results, inputs=query_input, outputs=results_output)

demo.launch()
