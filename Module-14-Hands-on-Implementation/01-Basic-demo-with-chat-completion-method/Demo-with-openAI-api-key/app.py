# chat.py
from openai import OpenAI
OPENAI_API_KEY="sk-......" # your API key
client = OpenAI(api_key=OPENAI_API_KEY)
# add your completion code
prompt = "Complete the following: Once upon a time there was a"
messages = [{"role": "user", "content": prompt}]
model="gpt-3.5-turbo"
# make completion
completion = client.chat.completions.create(model=model, messages=messages)
# print response
print(completion.choices[0].message.content)
