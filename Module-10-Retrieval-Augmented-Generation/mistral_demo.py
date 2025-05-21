from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import os
from elasticsearch import Elasticsearch, helpers
import pandas as pd

api_key = os.environ["MISTRAL_API_KEY"]
model = "mistral-large-latest"

client = MistralClient(api_key=api_key)

question = "how many matches total matches played in IPL 2023"

chat_response = client.chat(
    model=model,
    messages=[ChatMessage(role="user", content=question)]
)
print(chat_response.choices[0].message.content)
#reply = llm(prompt)
#print(reply)

