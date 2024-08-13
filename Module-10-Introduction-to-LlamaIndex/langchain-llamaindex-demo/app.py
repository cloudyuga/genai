import os
import streamlit as st
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')

llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=api_key)
documents = SimpleDirectoryReader("data").load_data()
index = VectorStoreIndex.from_documents(documents, llm=llm)

st.title("LlamaIndex-LangChain Demo")
query = st.text_input("Enter your question")
query_engine = index.as_query_engine()
response = query_engine.query(query)
st.subheader("Response")
st.write(response.response)
