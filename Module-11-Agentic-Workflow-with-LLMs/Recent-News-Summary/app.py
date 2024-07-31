import os
import httpx
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_huggingface import HuggingFaceEndpoint

# Load environment variables, Remove comments to load api keys from .env file 
# load_dotenv()
# NEWS_API_KEY = os.getenv("NEWS_API_KEY")
# HF_TOKEN = os.getenv("HF_TOKEN")

st.title("India News Summary")

# Get API keys from the user
NEWS_API_KEY = st.sidebar.text_input("Enter News API Key", type="password")
st.sidebar.write("Check out this [News API](https://newsapi.org/) to generate API key")
HF_TOKEN = st.sidebar.text_input("Enter Hugging Face API Key", type="password")
st.sidebar.write("Check out this [Hugging Face Token](https://huggingface.co/settings/tokens) to generate token")

# Define a combined tool function to fetch and summarize news
def fetch_and_summarize_news(arg: str = None) -> str:
    """Fetch the latest news articles and summarize them."""
    try:
        # Fetch news
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY.strip()}"
        response = httpx.get(url)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        
        if not articles:
            return "No news articles found."
    
        # Prepare articles for summarization
        sanitized_articles = []
        for article in articles:
            title = (article.get('title') or '').replace('\n', ' ').replace('\r', ' ')
            description = (article.get('description') or '').replace('\n', ' ').replace('\r', ' ')
            sanitized_articles.append(f"Title: {title}\nDescription: {description}")
    
        news_text = "\n\n".join(sanitized_articles)
        prompt = f"Summarize the following news articles:\n\n{news_text}. Please do not write the title. The summary should be in one sentence for each news."
    
        # Generate the summary
        summary = llm(prompt)
        return summary
    except Exception as e:
        return f"Error: {e}"

# Initialize the HuggingFace inference endpoint
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=HF_TOKEN.strip(),
    temperature=0.7,
    max_new_tokens=500
)

# Define tools for the agent
tools_for_agent = [
    Tool(name="fetch_and_summarize_news", func=fetch_and_summarize_news, description="Fetch and summarize the latest news articles")
]

# Define a prompt template for the agent
template = """
Answer the following question using the available tool:
{tools}
Use the following format:
1. **Question**: {input}
2. **Thought**: Determine which action to take.
3. **Action**: {tool_names}
4. **Action Input**: Provide the input required for the action.
5. **Observation**: Note the result from the action.
6. **Thought**: Analyze the observations and decide on the next steps.
7. **Final Answer**: Provide the final answer based on the observations.
Begin!
Question: {input}
Thought:{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template=template).partial(
    tools="\n".join([f"{t.name}: {t.description}" for t in tools_for_agent]),
    tool_names=", ".join([t.name for t in tools_for_agent])
)

# Initialize the agent
react_prompt = prompt
agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True, handle_parsing_errors=True)

# Streamlit UI for fetching and summarizing news
if st.button("Get and Summarize News"):
    with st.spinner("Processing..."):
        try:
            # Create the input data for the agent
            input_data = {
                'input': "Fetch and summarize the latest news articles.",
                'agent_scratchpad': ''
            }

            # Execute the agent workflow
            result = agent_executor.invoke({
                'input': input_data['input'],
                'agent_scratchpad': input_data['agent_scratchpad']
            }, handle_parsing_errors=True)
            
            # Check if the result contains the expected data
            st.subheader("News Summary")
            st.write(result['output'])  
        except Exception as e:
            st.error(f"An error occurred: {e}")
