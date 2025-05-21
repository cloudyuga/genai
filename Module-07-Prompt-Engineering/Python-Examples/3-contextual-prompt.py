import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Function to generate a response
def generate_response(context, question):
    prompt = f"""
    You are a knowledgeable assistant with expertise in various domains. Based on the provided context, deliver a clear, concise, and accurate response to the question.

    Context:
    {context}

    Question:
    {question}

    Response:
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert assistant providing insightful and well-reasoned answers."},
                {"role": "user", "content": prompt.strip()}
            ],
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Get user input
context = input("Enter the context (provide detailed background information): ")
question = input("Enter the question (what do you want to know?): ")

# Generate and display the response
response = generate_response(context, question)
print("\nResponse:\n", response)
