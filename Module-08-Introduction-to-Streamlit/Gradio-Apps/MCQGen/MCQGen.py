from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain,SequentialChain
from langchain_huggingface import HuggingFaceEndpoint
from dotenv import load_dotenv
import os

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Initialize tokenizer and language model
repo_id = "mistralai/Mistral-7B-Instruct-v0.3"
llm=HuggingFaceEndpoint(repo_id=repo_id,temperature=0.7,max_new_tokens=1000,huggingfacehub_api_token=HF_TOKEN)

# Template for quiz generation
TEMPLATE = """
Text: {text}
You are an expert MCQ maker. Given the above text, it is your job to create a quiz of {number} multiple choice questions for students in {tone} tone.
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like RESPONSE_JSON below and use it as a guide. Ensure to make {number} MCQs
{response_json}
"""

# Prompt template configuration
quiz_generation_prompt = PromptTemplate(
    input_variables=["text", "number", "tone", "response_json"],
    template=TEMPLATE
)

# Initialize LLMChain
quiz_chain = LLMChain(llm=llm, prompt=quiz_generation_prompt, output_key="quiz", verbose=True)

TEMPLATE2="""
You are an expert English grammarian and writer. Given a Multiple Choice Quiz for students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis.
if the quiz is not as per with the cognitive and analytical abilities of the students,\
update the quiz questions that need to be changed and change the tone such that it perfectly fits the student's abilities
Quiz_MCQs:
{quiz}
Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["quiz"], template=TEMPLATE2)

review_chain=LLMChain(llm=llm , prompt=quiz_evaluation_prompt , output_key="review", verbose=True)


#connect both chain quiz_chain & review_chain
generate_evaluate_chain=SequentialChain(chains=[quiz_chain, review_chain], input_variables=["text", "number", "tone", "response_json"], output_variables=["quiz", "review"], verbose=True)

