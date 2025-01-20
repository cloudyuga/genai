# agent_reasoning.py
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

# Define reasoning strategies
def reasoning_strategy(strategy_type):
    """
    Return a reasoning-specific prompt suffix.
    """
    strategies = {
        "chain_of_thought": "Explain your reasoning step by step before providing the final answer.",
        "self_reflection": "After answering, critique your own response for accuracy and clarity, and refine it if needed."
    }
    return strategies.get(strategy_type, "")


# Process input with reasoning
def process_prompt_with_reasoning(prompt, persona_prefix, reasoning_suffix):
    """
    Process the input prompt using the LLM with persona and reasoning strategy.
    """
    prompt = f"{persona_prefix}\n\nUser: {user_input}\nAI:\n{reasoning_suffix}"

    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use the cheapest model
        messages=[
            {"role": "system", "content": persona_prefix},
            {"role": "user", "content": reasoning_suffix},
            {"role": "user", "content": prompt}
        ],
        max_tokens=150,
        temperature=0.7)
        #print(response)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"


# Main function
if __name__ == "__main__":
    print("Welcome to the Agent with Advanced Reasoning Script!")

    # Persona selection
    print("\nSelect a persona:")
    personas = ["friendly_assistant", "technical_expert", "creative_writer", "strict_tutor"]
    for i, persona in enumerate(personas, start=1):
        print(f"{i}. {persona}")

    choice = int(input("\nEnter the number for your desired persona: "))
    selected_persona = personas[choice - 1]
    persona_prefix = define_persona(selected_persona)
    print(f"\nYou selected: {selected_persona}\n")

    # Reasoning strategy selection
    print("\nSelect a reasoning strategy:")
    strategies = ["chain_of_thought", "self_reflection"]
    for i, strategy in enumerate(strategies, start=1):
        print(f"{i}. {strategy}")

    strategy_choice = int(input("\nEnter the number for your desired strategy: "))
    selected_strategy = strategies[strategy_choice - 1]
    reasoning_suffix = reasoning_strategy(selected_strategy)
    print(f"\nYou selected: {selected_strategy}\n")

    # Interactive prompt processing
    while True:
        user_input = input("\nEnter a prompt (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting. Goodbye!")
            break

        response = process_prompt_with_reasoning(user_input, persona_prefix, reasoning_suffix)
        print("\nResponse:")
        print(response)

