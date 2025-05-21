import streamlit as st
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from elasticsearch import Elasticsearch, helpers
import pandas as pd

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, "scheme": "http"}])

prompt_template = """
You are a cricket news anchor, answer the QUESTION based on the CONTEXT.
QUESTION: {question}

CONTEXT: 
{context}
"""

def elastic_search(query):                                                                    
    search_query = {
        "size": 100,
        "query": {"match_all": {}}
    }   
    return search_query

def get_response(query):
    search_query = elastic_search(query)
    response = es.search(index="matches", body=search_query)
    return response['hits']['hits']

# Streamlit App
st.title('IP2023 Analysis')

question = st.text_input('Enter your question here:')

if st.button('Submit'):
    context = get_response(question)
    prompt = prompt_template.format(question=question, context=context).strip()
    #print(prompt)
    chat_response = client.chat(
        model=model,
        messages=[ChatMessage(role="user", content=prompt)]
    )
    results = chat_response.choices[0].message.content 
    print(results)
    if results:
        st.write("Results:")
        st.write(results)
else:
    st.write("Please enter a question.")

