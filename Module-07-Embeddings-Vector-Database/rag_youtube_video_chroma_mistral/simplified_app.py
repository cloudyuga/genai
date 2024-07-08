#Youtube_video = "https://www.youtube.com/watch?v=4O1rs7mrNDo"
import streamlit as st
from mistralai.client import MistralClient
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import tempfile
import os

# Load environment variables
from dotenv import load_dotenv

load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")
embeddings = HuggingFaceEmbeddings() # all-mpnet-base-v2 model is used as a default model for this class

# Initialize Mistral client
client = MistralClient(api_key=mistral_api_key)

# Function to fetch YouTube transcript text
def fetch_youtube_transcript(video_url):
    try:
        yt = YouTube(video_url)
        captions = YouTubeTranscriptApi.get_transcript(yt.video_id, languages=['en'])
        transcript_text = '\n'.join([caption['text'] for caption in captions])
        return transcript_text
    except Exception as e:
        st.error(f"Error fetching YouTube transcript: {e}")
        return None

def create_chunks(transcript_text):
    if transcript_text:
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=20,
            length_function=len,
            is_separator_regex=False,
        )
        chunks = text_splitter.create_documents([transcript_text])
        return chunks

def embed_store(chunks):
    persist_directory = 'youtube_embeddings'
    vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)
    vectordb.persist()  # Persist ChromaDB
    # Load persisted Chroma database
    vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
    return vectordb

def retriever(vectordb, prompt):
    docs = vectordb.similarity_search(prompt)
    if docs:
        text = docs[0].page_content
        return text
    else:
        st.warning("No relevant documents found.")
        return None
    
def get_llm_response(text, prompt):                        
    # Perform response generation using MistralAI
    if text is not None and prompt is not None:
        messages = [
                {"role": "system", "content": text},
                {"role": "user", "content": f"Context: {text}\n\nQuestion: {prompt}\n\nAnswer:"}
            ]
        response = client.chat(model="mistral-large-latest", messages=messages)
            
        return response.choices[0].message.content
    else:
        st.warning("No video found or error occurred.")
        return None

# Streamlit application
def main():
    st.title("YouTube RAG Chatbot 📺")
    st.caption("This app allows you to chat with a YouTube video using RAG (Retrieval-Augmented Generation)")

    # Text input for YouTube video URL
    video_url = st.text_input("Enter YouTube Video URL")

    # Text input for prompt
    prompt = st.text_input("Ask any question about the YouTube Video")

    # Button to perform RAG
    if st.button("Chat with Video"):
        if video_url and prompt:
            # Perform RAG with MistralAI and Chroma
            transcript_text=fetch_youtube_transcript(video_url)
            chunks = create_chunks(transcript_text)
            vectordb = embed_store(chunks)
            text = retriever(vectordb, prompt)
            answer = get_llm_response(text, prompt)
            if answer:
                # Display generated answer
                st.subheader("Generated Answer:")
                st.write(answer)

if __name__ == "__main__":
    main()
