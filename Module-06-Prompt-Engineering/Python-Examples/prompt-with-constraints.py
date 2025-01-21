import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
 
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)
        

prompt = """Write a description of climate change in a formal tone. Your response must be complete in 50-words."""
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    max_tokens=150
)
print(response.choices[0].message.content)

Output:
python .\prompt-with-constraints.py
Climate change refers to long-term alterations in temperature, precipitation, and other atmospheric conditions, primarily attributed to human activities such as fossil fuel combustion and deforestation. It poses significant environmental challenges, including increased frequency of extreme weather events, rising sea levels, and biodiversity loss, necessitating urgent global cooperation to mitigate its effects.
