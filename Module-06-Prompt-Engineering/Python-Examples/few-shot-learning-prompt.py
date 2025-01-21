import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
 
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
        

prompt = """Translate the following sentence:
- "Hello, how are you?" -> "Bonjour, comment ça va?"
- "What is your name?" -> "Comment tu t'appelles?"
- "I love programming." ->"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=50
)
print(response.choices[0].message.content)


Output:
python .\few-shot-learning-prompt.py
"I love programming." -> "J'adore la programmation."
