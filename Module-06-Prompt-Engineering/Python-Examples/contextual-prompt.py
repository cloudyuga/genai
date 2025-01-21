import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Function to generate a response
def generate_response(context, question):
    prompt = f"""
    You are a knowledgeable assistant with expertise in various domains. Based on the provided context, deliver a clear, concise, and accurate response to the question.

    Context:
    {context}

    Question:
    {question}

    Response:
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert assistant providing insightful and well-reasoned answers."},
                {"role": "user", "content": prompt.strip()}
            ],
            max_tokens=150,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

# Get user input
context = input("Enter the context (provide detailed background information): ")
question = input("Enter the question (what do you want to know?): ")

# Generate and display the response
response = generate_response(context, question)
print("\nResponse:\n", response)


Output:
python .\contextual-prompt.py       
Enter the context (provide detailed background information): The time from Britain's first inhabitation until the Last Glacial Maximum is known as the Old Stone Age, or Palaeolithic era. Archaeological evidence indicates that what was to become England was colonised by humans long before the rest of the British Isles because of its more hospitable climate between and during the various glacial periods of the distant past. This earliest evidence, from Happisburgh in Norfolk, includes the oldest hominid artefacts found in Britain, and points to dates of more than 800,000 RCYBP.[1] These earliest inhabitants were hunter-gatherers. Low sea-levels meant that Britain was attached to the continent for much of this earliest period of history, and varying temperatures over tens of thousands of years meant that it was not always inhabited.
Enter the question (what do you want to know?): what is old stone age?

Response:
The Old Stone Age, or Palaeolithic era, is the earliest period of human history characterized by the use of stone tools. It spans from the first appearance of hominins over 2 million years ago until approximately 10,000 years ago, leading up to the end of the Last Glacial Maximum. During this time, humans were primarily hunter-gatherers, relying on foraging and hunting for survival. In Britain, archaeological evidence suggests that this period began with the inhabitation of the region over 800,000 years ago, facilitated by varying and more hospitable climatic conditions during glacial and interglacial periods.
