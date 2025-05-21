from typing import TypedDict, Literal, Annotated, List
from operator import add
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from utils import get_llm

# ---------------------------
# Step 1: Define State Schema
# ---------------------------
class ResumeInputState(TypedDict):
    jd_output: str
    resume: str

class ResumeOutputState(TypedDict):
    match_result: str

class ResumeMatchingState(ResumeInputState, ResumeOutputState):
    messages: Annotated[List[BaseMessage], add]

# ----------------------------------------
# Step 2: Helper functions to Define Tool
# ----------------------------------------
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_core.output_parsers import StrOutputParser

# Prompt to extract skills from text
skill_extraction_prompt = PromptTemplate.from_template("""
You are an expert technical recruiter. Extract only the relevant technical and soft skills from the following text.
Return them as a Python list of strings.

Text:
{text}

Skills List:
""")

# Chain to extract skills using LLM


# Use with job description
def extract_skills_from_jd(job_description: str) -> list:
    llm = get_llm()
    skill_extractor_chain = skill_extraction_prompt | llm | StrOutputParser()
    result = skill_extractor_chain.invoke({"text": job_description})
    try:
        return eval(result.strip())
    except Exception:
        return []

# Use with resume
def extract_skills_from_resume(resume_text: str) -> list:
    llm = get_llm()
    skill_extractor_chain = skill_extraction_prompt | llm | StrOutputParser()
    result = skill_extractor_chain.invoke({"text": resume_text})
    try:
        return eval(result.strip())
    except Exception:
        return []


# --------------------------
# Step 3: Define Tool
# --------------------------
@tool
def check_resume_match(jd: str, resume: str) -> str:
    """Check whether the resume matches the job description."""
    # Parse the job description and resume to extract required and present skills
    required_skills = extract_skills_from_jd(jd)
    candidate_skills = extract_skills_from_resume(resume)

    # Calculate the match percentage based on the presence of required skills
    matched_skills = required_skills.intersection(candidate_skills)
    match_percentage = (len(matched_skills) / len(required_skills)) * 100

    # Generate reasoning
    missing_skills = required_skills - matched_skills
    reasoning = f"Matched skills: {matched_skills}. Missing skills: {missing_skills}."

    return f"**Match Percentage: {match_percentage}%**\n**Reasoning:** {reasoning}"

# --------------------------
# Step 4: Bind Tool
# --------------------------
tools_rm = [check_resume_match]

# --------------------------
# Step 5: Agent Logic
# --------------------------
def call_model_resume_matcher(state: ResumeMatchingState) -> ResumeMatchingState:
    llm = get_llm()
    model_rm = llm.bind_tools(tools_rm)
    local_messages = state.get("messages", [])
    jd = state["jd_output"]
    resume = state["resume"]

    if not local_messages:
        local_messages.append(HumanMessage(content=f"JD: {jd}\n\nResume: {resume}"))

    system_message = SystemMessage(content="""
You are a professional recruiter analyzing whether a resume is suitable for the job description.
- Prioritize the presence of core technical skills explicitly mentioned in the job description, such as Python and Docker.
- If these skills are missing, assign a significantly lower match percentage.
- Consider transferable skills only if they are directly relevant to the job requirements.
- Provide a clear explanation for the match percentage assigned.
""")
    response = model_rm.invoke([system_message] + local_messages)
    state["match_result"] = response.content
    state["messages"] = local_messages + [response]
    return state

def should_continue_rm(state: ResumeMatchingState) -> Literal["tools", END]:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END

# --------------------------------------
# Step 6: Resume Scanner Agent SubGraph
# --------------------------------------
resume_graph = StateGraph(ResumeMatchingState, input=ResumeInputState, output=ResumeOutputState)
resume_graph.add_node("call_model_resume_matcher", call_model_resume_matcher)
resume_graph.add_node("tools", ToolNode(tools_rm))
resume_graph.add_edge(START, "call_model_resume_matcher")
resume_graph.add_conditional_edges("call_model_resume_matcher", should_continue_rm)
resume_graph.add_edge("tools", "call_model_resume_matcher")

resume_matcher_agent = resume_graph.compile()

"""
# ---------------------------------
# Step 8: Run Resume matcher Agent
# ---------------------------------
resume_result = resume_matcher_agent.invoke({
   # "jd_output": result["jd_output"],
    "jd_output": "We are looking for a Data Scientist skilled in Machine Learning and Python to analyze data and create predictive models.",
    "resume": "I have 2 years experence in JAVA"
})

print("Resume Match Result:", resume_result["match_result"])
"""
