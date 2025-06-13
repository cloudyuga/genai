#Example video link: https://www.youtube.com/watch?v=4O1rs7mrNDo
import gradio as gr
from langchain_community.vectorstores import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI()

# Fetch transcript
def fetch_youtube_transcript(video_url):
    try:
        yt = YouTube(video_url)
        captions = YouTubeTranscriptApi.get_transcript(yt.video_id, languages=['en'])
        return '\n'.join([caption['text'] for caption in captions])
    except Exception as e:
        return f"❌ Error fetching YouTube transcript: {e}"

# Core RAG function
def perform_rag(video_url, prompt):
    try:
        transcript_text = fetch_youtube_transcript(video_url)
        if transcript_text.startswith("❌"):
            return transcript_text

        # Create embeddings and split text
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.create_documents([transcript_text])

        # Store in Chroma
        persist_directory = 'youtube_embeddings'
        vectordb = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory
        )
        vectordb.persist()
        vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)

        docs = vectordb.similarity_search(prompt)
        if not docs:
            return "⚠️ No relevant documents found."

        context = docs[0].page_content
        messages = [
            {"role": "system", "content": "You are an AI assistant that helps answer questions based on provided context."},
            {"role": "user", "content": f"Context: {context}\n\nQuestion: {prompt}\n\nAnswer:"}
        ]

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Error performing RAG: {e}"

# Gradio interface
with gr.Blocks() as demo:
    gr.Markdown("# 🎥 YouTube RAG Chatbot with OpenAI")
    gr.Markdown("Chat with any YouTube video using RAG (Retrieval-Augmented Generation)")

    with gr.Row():
        video_url = gr.Textbox(label="YouTube Video URL", placeholder="Enter the full URL")
        prompt = gr.Textbox(label="Your Question", placeholder="Ask something based on the video")

    submit_btn = gr.Button("Chat with Video")
    output = gr.Textbox(label="Generated Answer", lines=10)

    submit_btn.click(fn=perform_rag, inputs=[video_url, prompt], outputs=output)

# Entry point
if __name__ == "__main__":
    demo.launch()
