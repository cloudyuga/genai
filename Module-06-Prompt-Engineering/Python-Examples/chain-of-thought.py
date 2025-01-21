import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Chain-of-Thought Prompting
prompt = """
Solve the following problem step by step:

Tom has 12 apples. He gave 4 apples to Jerry, then bought 7 more apples. After that, he gave 5 apples to Sally. 
How many apples does Tom have now?

Explain your reasoning step by step.
"""

# Generate response
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a reasoning assistant. Provide detailed step-by-step solutions."},
        {"role": "user", "content": prompt}
    ],
)

# Print the response
print(response.choices[0].message.content.strip())


Output:

python .\chain-of-thought.py
To determine how many apples Tom has after the transactions described, we can break it down step by step:

1. **Initial Number of Apples**: Tom starts with 12 apples.

   \[
   \text{Apples with Tom} = 12
   \]

2. **Giving Apples to Jerry**: Tom gives 4 apples to Jerry. To find out how many apples Tom has after this, we subtract the 4 apples he gave away from his initial amount.

   \[
   12 - 4 = 8
   \]

   Now, Tom has 8 apples left. 

3. **Buying More Apples**: Next, Tom buys 7 more apples. To find Tom's new total after buying these apples, we add the 7 apples to the 8 apples he had after giving some to Jerry.

   \[
   8 + 7 = 15
   \]

   Now, Tom has 15 apples.

4. **Giving Apples to Sally**: Finally, Tom gives 5 apples to Sally. We need to subtract these 5 apples from the 15 apples he currently has.

   \[
   15 - 5 = 10
   \]

After all the transactions, Tom has 10 apples left.

So, the final answer is:

\[
\text{Tom has } 10 \text{ apples now.}
\]
