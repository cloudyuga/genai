import os
import httpx
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_huggingface import HuggingFaceEndpoint
import urllib.parse

st.title("City Weather Information with AI Review")
OPENWEATHER_API_KEY = st.sidebar.text_input("Enter Weather API Key", type="password")
st.sidebar.write("Check out this [Weather API](https://home.openweathermap.org/api_keys) to generate API key")
HF_TOKEN = st.sidebar.text_input("Enter Hugging Face API Key", type="password")
st.sidebar.write("Check out this [Hugging Face Token](https://huggingface.co/settings/tokens) to generate token")
city = st.text_input("Enter the name of a city:")

# Define the tool to fetch weather information
def fetch_weather(city: str) -> dict:
    """Fetch the weather information for a given city."""
    city = city.strip()  # Ensure no leading/trailing spaces
    encoded_city = urllib.parse.quote(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={OPENWEATHER_API_KEY}&units=metric"
    try:
        response = httpx.get(url)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return {"error": str(e)}

# Define the tool to generate a review of the weather information
def generate_review(w_info : str) -> str:
    """Generate a review based on the weather information."""
    if "error" in w_info:
        return f"Error fetching weather data: {w_info['error']}"
    input_text = f"The current weather is {w_info}. Provide a detailed review based on this information."
    # Generate the review using the language model
    review = llm(input_text)
    return review

# Initialize the HuggingFace inference endpoint
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=HF_TOKEN.strip(),
    temperature=0.7,
    max_new_tokens=200
)

# Define tools for agents
fetch_weather_tool = Tool(
    name="fetch_weather",
    func=fetch_weather,
    description="Fetch the weather information for a given city."
)

generate_review_tool = Tool(
    name="generate_review",
    func=generate_review,
    description="Generate a review based on the fetched weather information."
)

# Define prompts for the agents
fetch_weather_prompt = PromptTemplate.from_template("""
You are an agent that fetches weather information for a given city.
City: {input} you can use {tools}                                                
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
""")

generate_review_prompt = PromptTemplate.from_template("""
You are an expert reviewer and use you can use {tools} for weather review
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
""")

# Initialize agents
fetch_weather_agent = create_react_agent(
    llm=llm,
    tools=[fetch_weather_tool],
    prompt=fetch_weather_prompt
)
generate_review_agent = create_react_agent(
    llm=llm,
    tools=[generate_review_tool],
    prompt=generate_review_prompt
)

fetch_weather_agent_executor = AgentExecutor(agent=fetch_weather_agent, tools=[fetch_weather_tool], verbose=True,handle_parsing_errors=True )
generate_review_agent_executor = AgentExecutor(agent=generate_review_agent, tools=[generate_review_tool], verbose=True,)

# Streamlit UI
if st.button("Get Weather Information and Review"):
    with st.spinner("Processing..."):
        try:
            # Fetch weather information
            weather_info = fetch_weather_agent_executor.invoke({'input': city})
            w_info=weather_info['output']
            if 'error' in weather_info:
                st.error(f"Error fetching weather data: {weather_info['error']}")
            else:
                # Generate review based on the weather information
                review = generate_review_agent_executor.invoke({'input': w_info})
                st.subheader("Weather Information")
                st.write(weather_info['output'])
                st.subheader("AI Generated Weather Review")
                st.write(review['output'])
        except Exception as e:
            st.error(f"Error: {e}")
