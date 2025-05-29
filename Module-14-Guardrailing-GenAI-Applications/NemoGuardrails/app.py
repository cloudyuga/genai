from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from nemoguardrails import RailsConfig, LLMRails

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Set the environment variable for OpenAI API key
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

# Load the Rails configuration from the path to your .co file
config = RailsConfig.from_path("./config")

# Initialize the LLMRails object with the config
llm_rail = LLMRails(config)

# Disallowed Topic: politics-related query

response = llm_rail.generate(messages=[
    {
     "role": "user", 
     "content": "your views on politics"}
])

print(response["content"])  # This should return the refusal message defined in your .co file
