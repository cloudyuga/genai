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

# Get OpenAI API key
api_key = os.getenv('OPENAI_API_KEY')

# Initialize the OpenAI model with the API key
if not api_key:
    st.error("OpenAI API key is not set. Please set it in your environment.")
else:
    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)

    # Load documents from the directory
    documents = SimpleDirectoryReader("data").load_data()
    if not documents:
        st.error("No documents found in the 'data' directory.")
    else:
        # Create an index from documents with default embedding
        index = VectorStoreIndex.from_documents(documents)  

        # Streamlit app interface
        st.title("LlamaIndex-LangChain Demo")

        query = st.text_input("Enter your question")

        if query:  # Only process if the query is not empty
            # Create a query engine
            query_engine = index.as_query_engine()

            # Query the engine and get the response
            response = query_engine.query(query)

            # Display the response
            st.subheader("Response")
            st.write(response.response)
        else:
            st.warning("Please enter a question to get a response.")
