# agent_base.py
import openai
import os
from openai import OpenAI

# Set up your OpenAI API key and create OPENAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define personas
def define_persona(persona_type):
    """
    Return a persona-specific prompt prefix.
    """
    personas = {
        "friendly_assistant": "You are a friendly and helpful assistant. Always be cheerful and concise.",
        "technical_expert": "You are a technical expert specializing in cloud computing and DevOps. Provide detailed, technical answers.",
        "creative_writer": "You are a creative writer skilled in crafting compelling stories and metaphors.",
        "strict_tutor": "You are a strict but fair tutor who explains concepts clearly and ensures learning through quizzes."
    }
    return personas.get(persona_type, "You are a helpful AI assistant.")

# Process input with persona
def process_prompt_with_persona(prompt, persona_prefix):
    """
    Process the input prompt using the LLM with a persona-specific prefix.
    """
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use the cheapest model
        messages=[
            {"role": "system", "content": persona_prefix},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7)
        print(response)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"


# Main function
if __name__ == "__main__":
    print("Welcome to the Agent Persona Script!")


    # Persona selection
    print("\nSelect a persona:")
    personas = ["friendly_assistant", "technical_expert", "creative_writer", "strict_tutor"]
    for i, persona in enumerate(personas, start=1):
        print(f"{i}. {persona}")

    choice = int(input("\nEnter the number for your desired persona: "))
    selected_persona = personas[choice - 1]
    persona_prefix = define_persona(selected_persona)
    print(f"\nYou selected: {selected_persona}\n")
    # print(persona_prefix)

    # Interactive prompt processing
    while True:
        user_input = input("\nEnter a prompt (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting. Goodbye!")
            break

        response = process_prompt_with_persona(user_input, persona_prefix)
        print("\nResponse:")
        print(response)