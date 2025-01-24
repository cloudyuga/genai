from together import Together
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = Together(api_key=api_key)

# Set the content policy
safe_content_policy = {
    "policy": """O1: Subject Relevance.
Should not
- Provide responses unrelated to Math, English, Science, Geography, or History.
- Generate content related to entertainment, sports, movies, fantasy, or other unrelated subjects.
Can
- Answer questions only if they are directly related to Math, English, Science, Geography, or History.
O2: Accuracy.
Should not
- Provide incorrect or misleading information in responses.
- Use non-factual information within the allowed subjects.
Can
- Correctly answer questions based on known facts within the specified subjects.
O3: Language and Tone.
Should not
- Use harsh, discouraging, or condescending language.
- Use overly complex language that might confuse younger students.
Can
- Use simple, clear, and positive language suitable for children under 16.
O4: Sensitive Content.
Should not
- Include any content that is inappropriate for children (e.g., references to violence, hate, or inappropriate language).
- Provide examples or explanations outside the scope of Math, English, Science, Geography, or History.
Can
- Provide age-appropriate examples and explanations within the scope of allowed subjects.
O5: Encouragement and Support.
Should not
- Discourage curiosity or make learning feel overwhelming.
Can
- Encourage students to explore and learn with positive reinforcement within the allowed subjects."""
}

# Function to validate safety
def is_safe(message, response=None):
    prompt = f"""[INST] Task: Check if there is unsafe content in the 
    'user' messages and optionally in 'assistant' responses according to our safety policy.
    
    <BEGIN UNSAFE CONTENT CATEGORIES>
    {safe_content_policy['policy']}
    <END UNSAFE CONTENT CATEGORIES>
    
    <BEGIN CONVERSATION>
    user: {message}
    """
    if response:
        prompt += f"assistant: {response}\n"

    prompt += """
    Provide your safety assessment for the above conversation:
    - First line must read 'safe' or 'unsafe'.
    - If unsafe, a second line must include a comma-separated list of violated categories. [/INST]"""

    response = client.completions.create(
        model="Meta-Llama/LlamaGuard-2-8b",
        prompt=prompt,
    )

    result = response.choices[0].text.strip()
    return result.split("\n")[0] == 'safe'
