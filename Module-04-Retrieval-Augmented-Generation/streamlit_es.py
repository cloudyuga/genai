import streamlit as st
from elasticsearch import Elasticsearch, helpers
import pandas as pd


# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, "scheme": "http"}])

def elastic_search(query):
    search_query = {
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["Venue", "First batting team"],
                        "type": "best_fields"
                    }
                },
            }
        }
    }
    return search_query


def elastic_search1(query):                                                                    
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
    results = get_response(question) 
    if results:
        st.write("Results:")
        print (len(results))
        for result in results:
            st.write(result['_source'])
else:
    st.write("Please enter a question.")

