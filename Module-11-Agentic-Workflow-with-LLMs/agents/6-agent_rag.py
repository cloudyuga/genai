# agent_rag.py
import openai
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import os

# Set up your OpenAI API key

# Initialize the base LLM
def initialize_llm():
    """
    Initialize the base Language Learning Model (LLM) using LangChain and OpenAI.
    """
    return OpenAI(model_name="gpt-4", temperature=0.7)

# Initialize the vector store
def initialize_vector_store(knowledge_path, embedding_model):
    """
    Initialize the vector store with the knowledge base documents.
    """
    # Load documents
    loader = TextLoader(knowledge_path)
    documents = loader.load()

    # Split documents into smaller chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.split_documents(documents)

    # Create vector store
    vector_store = Chroma.from_documents(docs, embedding_model)
    return vector_store

# Retrieve relevant context
def retrieve_context(vector_store, query, top_k=3):
    """
    Retrieve the top-k relevant documents for the given query.
    """
    return vector_store.similarity_search(query, k=top_k)

# Process input with RAG
def process_prompt_with_rag(llm, user_input, persona_prefix, reasoning_suffix, vector_store):
    """
    Process the input prompt using the LLM with persona, reasoning, and retrieved context.
    """
    # Retrieve relevant context
    relevant_docs = retrieve_context(vector_store, user_input)
    context = "\n".join([doc.page_content for doc in relevant_docs])

    # Construct the prompt
    prompt = f"{persona_prefix}\n\nRelevant Context:\n{context}\n\nUser: {user_input}\nAI:\n{reasoning_suffix}"

    try:
        response = llm(prompt)
        return response
    except Exception as e:
        return f"Error processing the prompt: {e}"

# Main function
if __name__ == "__main__":
    print("Welcome to the Agent with Retrieval-Augmented Generation!")

    # Initialize LLM
    llm = initialize_llm()
    print("LLM Initialized. Ready to process prompts.")

    # Initialize embeddings and vector store
    embedding_model = OpenAIEmbeddings()
    knowledge_base_path = "knowledge_base.txt"  # Replace with the path to your knowledge base file
    vector_store = initialize_vector_store(knowledge_base_path, embedding_model)
    print("Vector Store Initialized with Knowledge Base.")

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

        response = process_prompt_with_rag(llm, user_input, persona_prefix, reasoning_suffix, vector_store)
        print("\nResponse:")
        print(response)

