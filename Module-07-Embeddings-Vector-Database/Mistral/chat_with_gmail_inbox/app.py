import tempfile #file handling
import streamlit as st #web app creation
import os
from google.oauth2.credentials import Credentials #google auth
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from langchain_community.vectorstores import Chroma #vector store management
from langchain_community.embeddings import HuggingFaceEmbeddings #embedding
from langchain_text_splitters import RecursiveCharacterTextSplitter 
from mistralai.client import MistralClient #llm
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv #environment variable management
import base64 #encoding/decoding

# Load environment variables
load_dotenv()
mistral_api_key = os.getenv("MISTRAL_API_KEY")

# Function to fetch Gmail emails based on a filter
def fetch_gmail_emails():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    creds = None

    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('gmail', 'v1', credentials=creds)
        results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="").execute()
        messages = results.get('messages', [])
        
        email_texts = []
        for message in messages[:10]:  # Limiting to first 10 emails for brevity
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg['payload']
            headers = payload.get('headers', [])
            for header in headers:
                if header.get('name') == 'Subject':
                    subject = header.get('value')
                    break
            parts = payload.get('parts', [])
            for part in parts:
                if part['mimeType'] == 'text/plain':
                    body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
                    email_texts.append(f"Subject: {subject}\n\n{body}")
        
        return "\n".join(email_texts)
    except Exception as e:
        st.error(f"Error fetching Gmail emails: {e}")
        return None

# Function to perform RAG using MistralAI and Chroma
def perform_rag(email_text, prompt):
    try:
        if email_text:
            # Create embeddings
            embeddings = HuggingFaceEmbeddings()
            
            # Split text into chunks
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=20,
                length_function=len,
                is_separator_regex=False,
            )
            chunks = text_splitter.create_documents([email_text])

            # Store chunks in ChromaDB
            persist_directory = 'gmail_embeddings'
            vectordb = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_directory)
            vectordb.persist()  # Persist ChromaDB
            
            # Load persisted Chroma database
            vectordb = Chroma(persist_directory=persist_directory, embedding_function=embeddings)
            
            # Perform retrieval using Chroma
            docs = vectordb.similarity_search(prompt)
            if docs:
                text = docs[0].page_content
            else:
                st.warning("No relevant documents found.")
                return None
            
            # Perform response generation using MistralAI
            client = MistralClient(api_key=mistral_api_key)
            messages = [
                ChatMessage(role="system", content="You are an assistant to help with email queries."),
                ChatMessage(role="user", content=f"Context: {text}\n\nQuestion: {prompt}\n\nAnswer:")
            ]
            response = client.chat(model="mistral-large-latest", messages=messages)
            
            return response.choices[0].message.content
        
        else:
            st.warning("No emails found or error occurred.")
            return None
        
    except Exception as e:
        st.error(f"Error performing RAG: {e}")
        return None

# Streamlit application
def main():
    st.title("Chat with your Gmail Inbox 📧")
    st.caption("This app allows you to chat with your Gmail inbox using MistralAI and ChromaDB")

    # Add the Gmail data to the knowledge base if the Mistral API key is provided
    if mistral_api_key:
        # Fetch Gmail emails
        email_text = fetch_gmail_emails()

        # Ask a question about the emails
        prompt = st.text_input("Ask any question about your emails")

        # Chat with the emails
        if prompt:
            answer = perform_rag(email_text, prompt)
            if answer:
                st.subheader("Generated Answer:")
                st.write(answer)

if __name__ == "__main__":
    main()
