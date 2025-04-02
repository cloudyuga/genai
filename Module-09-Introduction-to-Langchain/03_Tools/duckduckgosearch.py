#pip install -qU duckduckgo-search langchain-community

import gradio as gr
from langchain_community.tools import DuckDuckGoSearchResults
# Initialize DuckDuckGo search
ddg_search = DuckDuckGoSearchResults(output_format="json")
#output_format="list"
#output_format="json"
def search_duckduckgo(query):
    """Performs a DuckDuckGo search and returns results."""
    return ddg_search.invoke(query)

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("# 🔍 DuckDuckGo Search with LangChain")
    
    query_input = gr.Textbox(label="Enter Search Query", placeholder="Type your search here...")
    search_button = gr.Button("Search")
    result_output = gr.Textbox(label="Search Result")
    
    search_button.click(search_duckduckgo, inputs=query_input, outputs=result_output)

demo.launch()
