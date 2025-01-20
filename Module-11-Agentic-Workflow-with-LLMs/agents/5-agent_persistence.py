# agent_persistence.py
import openai
import os
import json
from openai import OpenAI

# Set up your OpenAI API key and create OPENAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# File path for persistent memory
MEMORY_FILE = "agent_memory.json"


# Load persistent memory
def load_memory():
    """
    Load memory from a persistent storage file.
    """
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return []

# Save persistent memory
def save_memory(memory):
    """
    Save memory to a persistent storage file.
    """
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

# Retrieve relevant memory
def retrieve_relevant_memory(memory, prompt, max_entries=3):
    """
    Retrieve relevant memory entries based on keywords in the user input.
    """
    relevant_memory = [
        entry for entry in memory if any(word in entry["prompt"] for word in prompt.split())
    ]
    return relevant_memory[-max_entries:]

# Process input with memory
def process_prompt_with_memory(llm, user_input, persona_prefix, reasoning_suffix, memory):
    """
    Process the input prompt using the LLM with persona, reasoning, and memory.
    """
    # Retrieve relevant memory
    relevant_memory = retrieve_relevant_memory(memory, user_input)
    print(relevant_memory)
    memory_text = "\n".join([f"role: {entry['user_input']}\nAI: {entry['response']}" for entry in relevant_memory])

    # Construct the prompt
    prompt = f"{persona_prefix}\n\nRelevant Memory:\n{memory_text}\n\nUser: {user_input}\nAI:\n{reasoning_suffix}"

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
    print("Welcome to the Agent with Persistent Memory!")

    # Initialize LLM
    llm = initialize_llm()
    print("LLM Initialized. Ready to process prompts.")

    # Load persistent memory
    memory = load_memory()

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

        response = process_prompt_with_memory(llm, user_input, persona_prefix, reasoning_suffix, memory)
        print("\nResponse:")
        print(response)

        # Update memory
        #memory.append({"user_input": user_input, "response": response})
        memory.append({f"role": "assistant", f"content": response})
        save_memory(memory)

