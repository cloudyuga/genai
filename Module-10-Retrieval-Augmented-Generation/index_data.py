import pandas as pd
from elasticsearch import Elasticsearch, helpers

# Load CSV data into a DataFrame
df = pd.read_csv('IPL23dataset.csv')

# Connect to Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200, "scheme": "http"}])

# Define a function to index data
def index_data(df, index_name='matches'):
    # Convert DataFrame to a list of dictionaries
    records = df.to_dict(orient='records')
    # Define Elasticsearch actions
    actions = [
        {
            "_index": index_name,
            "_id": i,
            "_source": record,
        }
        for i, record in enumerate(records)
    ]
    # Bulk index data
    try:
        helpers.bulk(es, actions)
        print("Data indexed successfully")
    except helpers.BulkIndexError as e:
        print(f"Bulk indexing failed for {len(e.errors)} documents")
        for error in e.errors:
            print(error)

# Index the data
index_data(df)

response = es.search(index="matches", body={"size": 100, "query": {"match_all": {}}})
print(f"Got {response['hits']['total']['value']} Hits:")
print (response['hits']['hits'])
#for hit in response['hits']['hits']:
#    print(hit["_source"])
