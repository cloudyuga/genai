# agent_base.py
import openai
import os
from openai import OpenAI

# Set up your OpenAI API key and create OPENAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Process a single prompt
def process_prompt(prompt):
    """
    Process the input prompt using the LLM and return the response.

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

# Main function for testing
if __name__ == "__main__":
    print("Welcome to the Agent Base Script!")
      
    # Interactive prompt processing
    while True:
        user_input = input("\nEnter a prompt (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting. Goodbye!")
            break
        
        response = process_prompt(user_input)
        print("\nResponse:")
        print(response)

