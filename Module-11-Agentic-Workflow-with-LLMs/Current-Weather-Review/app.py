import os
import httpx
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import Tool
from langchain_huggingface import HuggingFaceEndpoint
import urllib.parse

# Load environment variables, Remove comments to load api keys from .env file
#load_dotenv()
#OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
#HF_TOKEN = os.getenv("HF_TOKEN")

# Get API keys from the user
st.title("City Weather Information with AI Review")
OPENWEATHER_API_KEY = st.sidebar.text_input("Enter Weather API Key", type="password")
st.sidebar.write("Check out this [Weather API](https://home.openweathermap.org/api_keys) to generate API key")
HF_TOKEN = st.sidebar.text_input("Enter Hugging Face API Key", type="password")
st.sidebar.write("Check out this [Hugging Face Token](https://huggingface.co/settings/tokens) to generate token")
city = st.text_input("Enter the name of a city:")

# Define a tool to fetch weather information and generate a review
def fetch_and_review_weather(city: str) -> str:
    """Fetch the weather information for a given city and generate a review."""
    city = city.strip()  # Ensure no leading/trailing spaces
    
    # Encode the city name for the URL
    encoded_city = urllib.parse.quote(city)
    url = f"https://api.openweathermap.org/data/2.5/weather?q={encoded_city}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        response = httpx.get(url)
        response.raise_for_status()
        weather_data = response.json()
        
        # Extract weather details
        weather = weather_data['weather'][0]['main']
        temperature = weather_data['main']['temp']
        
        # Generate the review
        input_text = f"The current weather in {city} is {weather} with a temperature of {temperature}°C. As an expert in weather forecast analysis, please provide an appropriate weather review."
        input_text = ''.join(c for c in input_text if c.isprintable())
        
        # Generate the review using the language model
        review = llm(input_text)
        return review
    except Exception as e:
        return f"Error: {e}"

# Initialize the HuggingFace inference endpoint
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=HF_TOKEN.strip(),
    temperature=0.7,
    max_new_tokens=200
)

# Define the tool for the agent
tools_for_agent = [
    Tool(
        name="fetch_and_review_weather",
        func=fetch_and_review_weather,
        description="Fetch the weather information for a given city and generate a review"
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

# Streamlit UI for fetching and reviewing weather

if st.button("Get Weather Information and Review"):
    with st.spinner("Processing..."):
        try:
            # Directly call the fetch_and_review_weather function through the agent
            review = agent_executor.invoke({
                'input': f"Generate weather review for {city}",
                'agent_scratchpad': ''
            }, handle_parsing_errors=True)
            
            st.subheader("AI Generated Weather Review")
            st.write(review['output'])
        except Exception as e:
            st.error(f"Error generating weather review: {e}")
