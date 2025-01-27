from gradio_client import Client

# Connect to the Gradio app
client = Client("https://pratikshahp-chat-with-hr-assistant.hf.space")

# View the available API information
client.view_api()

# Make a prediction
response = client.predict("Who is the candidate?")
print(response)
