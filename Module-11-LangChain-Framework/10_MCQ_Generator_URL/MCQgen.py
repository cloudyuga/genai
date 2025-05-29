import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain_openai import ChatOpenAI

# Load API Key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI Chat Model
llm = ChatOpenAI(model="gpt-4o", temperature=0.7, max_tokens=1000)

# Prompt template for quiz generation
TEMPLATE = """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to create a quiz of {number} multiple choice questions for students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. Ensure to make {number} MCQs
{response_json}
"""

quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "tone", "response_json"],
    template=TEMPLATE
)

quiz_chain = LLMChain(
    llm=llm,
    prompt=quiz_generation_prompt,
    output_key="quiz",
    verbose=True
)

# Prompt template for quiz evaluation
TEMPLATE2 = """
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for students.
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
If the quiz is not appropriate for the cognitive and analytical abilities of the students,
update the quiz questions that need to be changed and change the tone such that it perfectly fits the student's abilities.

Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt = PromptTemplate(
    input_variables=["quiz"],
    template=TEMPLATE2
)

review_chain = LLMChain(
    llm=llm,
    prompt=quiz_evaluation_prompt,
    output_key="review",
    verbose=True
)

# Connect both chains
generate_evaluate_chain = SequentialChain(
    chains=[quiz_chain, review_chain],
    input_variables=["text", "number", "tone", "response_json"],
    output_variables=["quiz", "review"],
    verbose=True
)
