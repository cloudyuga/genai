import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
 
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
        
prompt = "Write a poem about the ocean."
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=50
)
print(response.choices[0].message.content)
