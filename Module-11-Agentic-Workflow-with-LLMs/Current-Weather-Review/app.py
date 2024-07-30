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
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Define a tool to fetch weather information
def fetch_weather(city: str) -> dict:
    """Fetch the weather information for a given city."""
    city = city.strip()  # Ensure no leading/trailing spaces
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = httpx.get(url)
    response.raise_for_status()
    return response.json()

# Define a tool to review the weather
def review_weather_tool(city: str, weather_data: dict) -> str:
    """Generate a review of the weather data."""
    weather = weather_data['weather'][0]['main']
    temperature = weather_data['main']['temp']
    
    # Sanitize the input text to remove non-printable characters
    input_text = f"The current weather in {city} is {weather} with a temperature of {temperature}°C. As an expert in weather forecast analysis, please provide an appropriate weather review."
    input_text = ''.join(c for c in input_text if c.isprintable())
    
    # Generate the review
    review = llm(input_text)
    return review

# Initialize the HuggingFace inference endpoint
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=HF_TOKEN.strip(),
    temperature=0.7,
    max_new_tokens=200
)

# Define tools for the agent
tools_for_agent = [
    Tool(
        name="fetch_weather",
        func=fetch_weather,
        description="Fetch the weather information for a given city"
    ),
    Tool(
        name="review_weather",
        func=lambda city, weather_data: review_weather_tool(city, weather_data),
        description="Generate a review of the weather data"
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

st.title("City Weather Information with AI Review")

# Streamlit UI for fetching and reviewing weather
city = st.text_input("Enter the name of a city:")

if st.button("Get Weather Information"):
    with st.spinner("Fetching weather information..."):
        try:
            city_sanitized = city.strip()  # Ensure no leading/trailing spaces
            weather_data = fetch_weather(city_sanitized)
            st.write(f"Weather in {city_sanitized}:")
            st.write(f"Weather: {weather_data['weather'][0]['main']}")
            st.write(f"Temperature: {weather_data['main']['temp']}°C")
        except Exception as e:
            st.error(f"Error fetching weather data: {e}")
            weather_data = {}

    if weather_data:
        with st.spinner("Generating AI review of the weather..."):
            try:
                input_data = {
                    'input': f"Generate a weather review for {city_sanitized}.",
                    'fetch_weather': weather_data,
                    'city': city_sanitized,
                    'agent_scratchpad': ''
                }
                # Directly call the review_weather_tool without the agent for this step
                review = review_weather_tool(city_sanitized, weather_data)
                st.subheader("AI Generated Weather Review")
                st.write(review)
            except Exception as e:
                st.error(f"Error generating weather review: {e}")
