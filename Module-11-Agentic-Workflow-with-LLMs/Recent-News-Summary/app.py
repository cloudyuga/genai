import os
import httpx
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_huggingface import HuggingFaceEndpoint
from langchain import globals

# Load environment variables
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

st.title("India News Summary")

# Define a tool to fetch news
def fetch_news(api_key: str = None) -> list:
    """Fetch the latest news articles."""
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key.strip()}"
    response = httpx.get(url)
    response.raise_for_status()
    return response.json().get("articles", [])

# Define a tool to summarize news
def summarize_news_tool(news_articles: list) -> str:
    """Summarize a list of news articles."""
    sanitized_articles = []
    for article in news_articles:
        title = (article.get('title') or '').replace('\n', ' ').replace('\r', ' ')
        description = (article.get('description') or '').replace('\n', ' ').replace('\r', ' ')
        sanitized_articles.append(f"Title: {title}\nDescription: {description}")
    
    news_text = "\n\n".join(sanitized_articles)
    prompt = f"Summarize the following news articles:\n\n{news_text}. Please do not write the title. The summary should be in one point for each news."
    
    # Generate the summary
    summary = llm(prompt)
    return summary

# Initialize the HuggingFace inference endpoint
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=HF_TOKEN.strip(),
    temperature=0.7,
    max_new_tokens=500
)

# Define tools for the agent
tools_for_agent = [
    Tool(
        name="fetch_news",
        func=fetch_news,
        description="Fetch the latest news articles"
    ),
    Tool(
        name="summarize_news",
        func=summarize_news_tool,
        description="Summarize a list of news articles"
    )
]

# Define a prompt template for the agent
template = """
Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:
{agent_scratchpad}
"""

prompt = PromptTemplate.from_template(template=template).partial(
    tools="\n".join([f"{t.name}: {t.description}" for t in tools_for_agent]),
    tool_names=", ".join([t.name for t in tools_for_agent]),
)

# Initialize the agent
react_prompt = prompt
agent = create_react_agent(
    llm=llm,
    tools=tools_for_agent,
    prompt=react_prompt
)
agent_executor = AgentExecutor(agent=agent, tools=tools_for_agent, verbose=True)

# Set verbose globally
globals.set_verbose(True)

# Streamlit UI for fetching and summarizing news
if st.button("Get and Summarize News"):
    with st.spinner("Fetching news..."):
        try:
            news_articles = fetch_news(NEWS_API_KEY)
            st.write(f"Fetched {len(news_articles)} articles")
        except Exception as e:
            st.error(f"Error fetching news: {e}")
            news_articles = []

    if not news_articles:
        st.error("No news articles found.")
    else:
        with st.spinner("Summarizing news..."):
            try:
                input_data = {
                    'input': "Summarize the latest news articles.",
                    'fetch_news': news_articles,
                    'agent_scratchpad': ''
                }
                # Directly call the summarize_news_tool without the agent for this step
                summary = summarize_news_tool(news_articles)
                st.subheader("News Summary")
                st.write(summary)
            except Exception as e:
                st.error(f"Error summarizing news: {e}")

        st.subheader("Full News Articles")
        for article in news_articles:
            st.write(f"**Title:** {article.get('title', 'N/A')}")
            st.write(f"**Description:** {article.get('description', 'N/A')}")
            st.write(f"**URL:** {article.get('url', 'N/A')}")
            st.write("---")
