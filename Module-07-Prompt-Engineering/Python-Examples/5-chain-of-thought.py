import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Chain-of-Thought Prompting
prompt = """
Solve the following problem step by step:

Tom has 12 apples. He gave 4 apples to Jerry, then bought 7 more apples. After that, he gave 5 apples to Sally. 
How many apples does Tom have now?

Explain your reasoning step by step.
"""

# Generate response
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a reasoning assistant. Provide detailed step-by-step solutions."},
        {"role": "user", "content": prompt}
    ],
)

# Print the response
print(response.choices[0].message.content.strip())
