import os
import httpx
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import MessageGraph, END
from typing import Sequence

# Load environment variables
load_dotenv()
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize the HuggingFace inference endpoint
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=HF_TOKEN.strip(),
    temperature=0.7,
    max_new_tokens=100
)

# Define nodes
def fetch_weather_node(state: Sequence[BaseMessage]) -> str:
    city = state[0].content.strip()
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        response = httpx.get(url)
        response.raise_for_status()
        weather_data = response.json()
        weather = weather_data['weather'][0]['main']
        temperature = weather_data['main']['temp']
        return f"The current weather in {city} is {weather} with a temperature of {temperature}°C."
    except Exception as e:
        return f"Error: {e}"

def generate_review_node(state: Sequence[BaseMessage]) -> str:
    input_text = state[0].content
    response = llm(input_text)
    return response

# Define the prompt template for generating weather reviews
review_prompt_template = """
You are an expert weather analyst. Based on the provided weather information, generate a detailed and insightful review. 
Weather Information: {weather_info[1]}
Your review should include an analysis of the weather conditions.
Review:
"""

# Create and configure the graph
builder = MessageGraph()

# Add nodes
builder.add_node("fetch_weather", fetch_weather_node)
builder.add_node("generate_review", generate_review_node)
builder.set_entry_point("fetch_weather")

# Define transitions
builder.add_edge("fetch_weather", "generate_review")
builder.set_finish_point("generate_review")

# Compile the graph
graph = builder.compile()

print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()

# Streamlit app
st.title("City Weather Information with AI Review")

city = st.text_input("Enter the name of a city:")

if st.button("Get Weather Information and Review"):
    if city:
        with st.spinner("Processing..."):
            try:
                # Prepare the input for the graph
                weather_info = graph.invoke(HumanMessage(content=city))
                st.write(weather_info[1].content)
                # Generate the review using the refined prompt
                review_input = review_prompt_template.format(weather_info=weather_info)
                review = graph.invoke(HumanMessage(content=review_input))
                
                st.subheader("AI Generated Weather Review")
                st.write(review[2].content)
            except Exception as e:
                st.error(f"Error generating weather review: {e}")
    else:
        st.warning("Please enter a city name.")
