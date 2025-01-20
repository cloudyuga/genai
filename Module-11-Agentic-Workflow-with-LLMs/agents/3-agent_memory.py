# agent_memory.py
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

# Define tasks
def define_task(task_type):
    """
    Return a task-specific instruction.
    """
    tasks = {
        "summarization": "Your task is to summarize the user's input into a concise statement.",
        "brainstorming": "Your task is to generate creative ideas or solutions based on the user's input.",
        "question_answering": "Your task is to answer questions accurately and informatively.",
    }
    return tasks.get(task_type, "")


def build_messages(prompt, persona_prefix, task_instruction, memory):
    """
    collate all inputs and build a prompt
    """
    messages = [{"role": "system", "content": persona_prefix}]
    messages.append({"role": "user", "content": f"Global Instruction: {task_instruction}"})
    if memory:
        messages.extend(memory)
    messages.append({"role": "user", "content": f"Current Task: {prompt}"})
    memory.append({f"role": "user", f"content": prompt})

    #print(messages)
    return messages

# Process input with memory
def process_prompt_with_memory(prompt, persona_prefix, task_instruction, memory):
    """
    Process the input prompt using the LLM with persona, task, and memory.
    """
   # memory_text = "\n".join(memory[-5:])  # Use the last 5 interactions for short-term memory
    messages = build_messages(prompt, persona_prefix, task_instruction, memory)
    #print(messages)
     
    try:
        response = client.chat.completions.create(model="gpt-3.5-turbo",  # Use the cheapest model
        messages=messages,
        max_tokens=150,
        temperature=0.7)
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Main function
if __name__ == "__main__":
    print("Welcome to the Agent with Memory Script!")

    # Persona selection
    print("\nSelect a persona:")
    personas = ["friendly_assistant", "technical_expert", "creative_writer", "strict_tutor"]
    for i, persona in enumerate(personas, start=1):
        print(f"{i}. {persona}")

    choice = int(input("\nEnter the number for your desired persona: "))
    selected_persona = personas[choice - 1]
    persona_prefix = define_persona(selected_persona)
    print(f"\nYou selected: {selected_persona}\n")

    # Task selection
    print("\nSelect a task:")
    tasks = ["summarization", "brainstorming", "question_answering"]
    for i, task in enumerate(tasks, start=1):
        print(f"{i}. {task}")

    task_choice = int(input("\nEnter the number for your desired task: "))
    selected_task = tasks[task_choice - 1]
    task_instruction = define_task(selected_task)
    print(f"\nYou selected: {selected_task}\n")

    # Initialize memory
    memory = []

    # Interactive prompt processing
    while True:
        user_input = input("\nEnter a prompt (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            print("Exiting. Goodbye!")
            break

        response = process_prompt_with_memory(user_input, persona_prefix, task_instruction, memory)
        print("\nResponse:")
        print(response)

        # Update memory
        memory.append({f"role": "assistant", f"content": response})
        print(memory)

        