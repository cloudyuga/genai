from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import os

# Get OpenAI API key from environment variable

# Define the AI Agent Persona
def create_persona():
    """
    Create an AI Agent Persona as a prompt for OpenAI model.
    """
    persona = {
        "name": "Helpful Assistant",
        "description": "An AI that helps with answering questions about a variety of topics.",
        "skills": ["General knowledge", "Problem-solving", "Communication"]
    }
    return persona

# Define the task the agent should perform
def define_task(persona, task):
    """
    Define the task that the AI agent should perform with its persona.
    """
    prompt = f"{persona['name']} is a helpful assistant. {persona['description']} Please assist the user with the following task: {task}"
    return prompt

# Interact with OpenAI API to generate a response
def get_ai_response(prompt):
    """
    Get a response from the OpenAI model.
    """
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use the cheapest model
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Example usage
if __name__ == "__main__":
    persona = create_persona()
    task = "Explain the process of photosynthesis."
    prompt = define_task(persona, task)
    response = get_ai_response(prompt)
    print(response)

