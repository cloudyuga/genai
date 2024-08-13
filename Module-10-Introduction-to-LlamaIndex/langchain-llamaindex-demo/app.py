# In this app we will use data directory to get the contents. 
# By default LlamaIndex uses text-embedding-ada-002, which is the default embedding used by OpenAI. please refer below link.
# https://docs.llamaindex.ai/en/stable/understanding/indexing/indexing/

import os
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the language model
api_key = os.getenv('OPENAI_API_KEY')
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Load documents
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents, llm=llm)

# Streamlit app setup
st.title("llamaindex-langchain-demo")
query = st.text_input("Enter your question")

if query:
    # Construct the prompt by combining the user's query and document texts
    document_texts = "\n".join(doc.text for doc in documents)
    prompt = f"{query}\n{document_texts}"
    
    # Invoke the language model directly
    response = llm.invoke(prompt)
    
    # Display the response
    st.subheader("Response")
    st.write(response.content)
