from together import Together
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

# Initialize Together client
client = Together(api_key=api_key)

# Set the content policy for guardrails
safe_content_policy = {
    "policy": """
    O1: Topic Restriction.
    Should not:
    - Respond to questions outside the domain of finance.
    - Discuss non-financial topics such as health, technology, or politics.
    Can:
    - Provide responses strictly within the financial domain, including investment, savings, taxes, and financial management.
    O2: Sensitive Information.
    Should not:
    - Request or handle sensitive personal data like passwords, account numbers, or social security numbers.
    Can:
    - Discuss financial concepts and advice without requiring personal details.
    O3: Language.
    Should not:
    - Use profane, offensive, or inappropriate language.
    Can:
    - Use clear, professional, and respectful language appropriate for financial discussions.
    """
}

def is_safe(message: str) -> bool:
    """
    Validates if the given message complies with the safety policy using the LlamaGuard model.
    Args:
        message (str): User message or chatbot response.
    Returns:
        bool: True if the message is safe, False otherwise.
    """
    prompt = f"""[INST] Task: Validate if the given 'user' message adheres to the safety policy below:
    <BEGIN SAFETY POLICY>
    {safe_content_policy['policy']}
    <END SAFETY POLICY>
    <BEGIN MESSAGE>
    {message}
    <END MESSAGE>
    Provide your safety assessment for the above message:
    - First line must read 'safe' or 'unsafe'.
    - If unsafe, a second line must include a comma-separated list of violated categories. [/INST]"""

    response = client.completions.create(
        model="meta-llama/Meta-Llama-Guard-3-8B",
        prompt=prompt
    )

    result = response.choices[0].text.strip().lower()
    return result == 'safe'
