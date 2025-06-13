import gradio as gr
import os
from github import Github
from langchain_community.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Fetch GitHub repo text
def fetch_github_repo_data(repo_name, github_token):
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
                    continue
        return repo_data
    except Exception as e:
        return f"❌ Error fetching GitHub repository data: {e}"

# Generate answer from OpenAI
def generate_response(context, question):
    try:
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
        return f"❌ Error generating response: {e}"

# Main function to handle RAG
def github_repo_chat(github_token, repo_name, question):
    repo_data = fetch_github_repo_data(repo_name, github_token)
    if repo_data.startswith("❌"):
        return repo_data

    try:
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=20, length_function=len
        )
        chunks = text_splitter.create_documents([repo_data])

        persist_directory = "github_repo_embeddings"
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        vectordb.persist()

        vectordb = Chroma(
            persist_directory=persist_directory,
            embedding_function=embeddings
        )

        docs = vectordb.similarity_search(question)
        if not docs:
            return "⚠️ No relevant documents found."

        context = docs[0].page_content
        return generate_response(context, question)

    except Exception as e:
        return f"❌ Error performing RAG: {e}"

# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 🐙 Chat with GitHub Repo using RAG + OpenAI")
    gr.Markdown("Enter a GitHub repo and ask questions based on its content.")

    github_token_input = gr.Textbox(label="GitHub Token", type="password")
    repo_name_input = gr.Textbox(label="GitHub Repo (e.g. owner/repo)")
    question_input = gr.Textbox(label="Your Question")
    answer_output = gr.Textbox(label="Answer", lines=10)

    submit_button = gr.Button("Ask")
    submit_button.click(
        github_repo_chat,
        inputs=[github_token_input, repo_name_input, question_input],
        outputs=answer_output
    )

# Run
if __name__ == "__main__":
    demo.launch()
