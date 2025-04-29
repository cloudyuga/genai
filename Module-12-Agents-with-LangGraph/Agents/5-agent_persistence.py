# agent_persistence.py
import openai
import os
import json
from openai import OpenAI

# Set up your OpenAI API key and create OPENAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# File path for persistent memory
MEMORY_FILE = "agent_memory.json"

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
def retrieve_relevant_memory(memory, prompt):
    """
    Retrieve relevant memory entries based on keywords in the user input.
    """
    relevant_memory = [
        entry for entry in memory if any(word in entry["content"] for word in prompt.split())
    ]
    return relevant_memory

def build_messages(prompt, persona_prefix, memory):
    """
    collate all inputs and build a prompt
    """
    messages = [{"role": "system", "content": persona_prefix}]
    if memory:
        messages.extend(memory)
    messages.append({"role": "user", "content": f"Current Task: {prompt}"})

    #print(messages)
    return messages

# Process input with memory
def process_prompt_with_memory(prompt, persona_prefix, memory):
    """
    Process the input prompt using the LLM with persona and memory.
    """
    # Retrieve relevant memory
    relevant_memory = retrieve_relevant_memory(memory, prompt)
    messages = build_messages(prompt, persona_prefix, relevant_memory)
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use the cheapest model
        messages=messages,
        max_tokens=150,
        temperature=0.7)
        #print(response)
        memory.append({f"role": "user", f"content": prompt})
        save_memory(memory)

        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"


# Main function
if __name__ == "__main__":
    print("Welcome to the Agent with Persistent Memory!")

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

    # Interactive prompt processing
    while True:
        user_input = input("\nEnter a prompt (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting. Goodbye!")

            break

        response = process_prompt_with_memory(user_input, persona_prefix, memory)
        print("\nResponse:")
        print(response)

        # Update memory
        #memory.append({"user_input": user_input, "response": response})
        memory.append({f"role": "assistant", f"content": response})
        save_memory(memory)

