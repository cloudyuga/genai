import streamlit as st
import os
from github import Github
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Function to fetch repository data from GitHub
def fetch_github_repo_data(repo_name, github_token):
    """Fetch all text content from a GitHub repository."""
    try:
        g = Github(github_token)
        repo = g.get_repo(repo_name)
        contents = repo.get_contents("")
        repo_data = ""

        while contents:
            file_content = contents.pop(0)
            if file_content.type == "dir":
                contents.extend(repo.get_contents(file_content.path))
            else:
                try:
                    file_data = repo.get_contents(file_content.path).decoded_content
                    text = file_data.decode("utf-8")
                    repo_data += f"\n\nFile: {file_content.path}\n{text}"
                except UnicodeDecodeError:
                    # Skip non-text files
                    continue

        return repo_data
    except Exception as e:
        st.error(f"Error fetching GitHub repository data: {e}")
        return None

# Function to generate a response using OpenAI
def generate_response(context, question):
    """Generate a response using OpenAI."""
    try:
        from openai import OpenAI

        client = OpenAI(api_key=openai_api_key)
        messages = [
            {"role": "system", "content": "You are an assistant that answers questions based on repository content."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"}
        ]
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Error generating response: {e}")
        return None

# Function to perform RAG using OpenAI and Chroma
def perform_rag(repo_data, question):
    """Perform retrieval-augmented generation using ChromaDB and OpenAI."""
    try:
        if not repo_data:
            st.warning("Repository data is empty.")
            return None

        # Create embeddings
        embeddings = HuggingFaceEmbeddings()

        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=20, length_function=len
        )
        chunks = text_splitter.create_documents([repo_data])

        # Store chunks in ChromaDB
        persist_directory = "github_repo_embeddings"
        vectordb = Chroma.from_documents(
            documents=chunks, embedding=embeddings, persist_directory=persist_directory
        )
        vectordb.persist()

        # Load persisted Chroma database
        vectordb = Chroma(
            persist_directory=persist_directory, embedding_function=embeddings
        )

        # Perform retrieval using Chroma
        docs = vectordb.similarity_search(question)
        if not docs:
            st.warning("No relevant documents found.")
            return None

        context = docs[0].page_content
        return generate_response(context, question)

    except Exception as e:
        st.error(f"Error performing RAG: {e}")
        return None

# Streamlit application
def main():
    st.title("Chat with GitHub Repository")
    st.caption("This app allows you to interact with a GitHub repository using OpenAI and ChromaDB.")

    # Get user inputs
    github_token = st.text_input("Enter your GitHub Token", type="password")
    git_repo = st.text_input("Enter the GitHub Repo (owner/repo)")

    if github_token and git_repo:
        repo_data = fetch_github_repo_data(git_repo, github_token)

        if repo_data:
            st.success(f"Successfully added {git_repo} to the knowledge base!")

            question = st.text_input("Ask any question about the repository")

            if question:
                answer = perform_rag(repo_data, question)

                if answer:
                    st.subheader("Generated Answer:")
                    st.write(answer)
        else:
            st.error("Failed to fetch repository data. Ensure the repository name and token are correct.")

if __name__ == "__main__":
    main()
