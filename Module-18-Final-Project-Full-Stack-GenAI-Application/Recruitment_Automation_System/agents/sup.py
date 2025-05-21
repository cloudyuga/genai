import re
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from agents.jd_gen import jd_generator_agent
from agents.rs import resume_matcher_agent
from agents.on_board_process import onboard_agent
from db_utils import jd_collection
class SupervisorState(TypedDict):
    requirements: str
    resume: str
    jd_output: str
    match_result: str
    match_percent: int
    interview_decision: str
    onboarding_result: str
    decision: str
    steps_done: List[str]

initial_state = {
    "jd_output": "",
    "match_result": "",
    "match_percent": 0,
    "interview_decision": "",
    "onboarding_result": "",
    "decision": "",
    "steps_done": []
}

# Individual nodes
def get_or_generate_jd(state: SupervisorState) -> SupervisorState:
    requirement = state["requirements"]

    # Search in vector DB
    result = jd_collection.similarity_search(requirement, k=1)
    if result:
        print("✔ Found similar JD from Chroma")
        state["jd_output"] = result[0].page_content
    else:
        print("⚠ No similar JD found, generating new")
        new_jd = jd_generator_agent.invoke({"requirement": requirement})["jd_output"]

        # Store to Chroma
        jd_collection.add_texts(
            texts=[new_jd],
            metadatas=[{"requirement": requirement}]
        )
        state["jd_output"] = new_jd

    state["steps_done"].append("jd_node")
    return state

"""def jd_node(state: SupervisorState) -> SupervisorState:
    if "jd_node" not in state["steps_done"]:
        jd_output = jd_generator_agent.invoke({"requirement": state["requirements"]})
        state["jd_output"] = jd_output["jd_output"]
        state["steps_done"].append("jd_node")
    return state
"""
def resume_match_node(state: SupervisorState) -> SupervisorState:
    if "resume_match_node" not in state["steps_done"]:
        print("=== Running resume_match_node ===")
        #print("JD Output:", state["jd_output"])
        #print("Resume:", state["resume"])

        result = resume_matcher_agent.invoke({
            "jd_output": state["jd_output"],
            "resume": state["resume"]
        })

        #print("Match Result Response:", result)
        state["match_result"] = result["match_result"]

        #match = re.search(r"Match Percentage:\s*(\d+)", state["match_result"])
        #state["match_percent"] = int(match.group(1)) if match else 0
        match = re.search(r"(\d+)\s*%", state["match_result"])
        state["match_percent"] = int(match.group(1)) if match else 0

        print("Extracted Match Percent:", state["match_percent"])

        state["steps_done"].append("resume_match_node")
    return state


def human_interview_node(state: SupervisorState, decision: str) -> SupervisorState:
    if "human_interview_node" not in state["steps_done"]:
        state["interview_decision"] = decision.strip()
        state["steps_done"].append("human_interview_node")
    return state

def onboard_process_node(state: SupervisorState) -> SupervisorState:
    if "onboard_process_node" not in state["steps_done"]:
        result = onboard_agent.invoke({
            "resume": state["resume"],
            "jd_output": state["jd_output"]
        })
        state["onboarding_result"] = result["onboarding_result"]
        state["decision"] = "Selected and Onboarded"
        state["steps_done"].append("onboard_process_node")
    return state

# Orchestration logic
def process_job(requirements: str, resume: str) -> SupervisorState:
    state = SupervisorState(
        requirements=requirements,
        resume=resume,
        **initial_state
    )
    state = get_or_generate_jd(state)
    state = resume_match_node(state)
    if state["match_percent"] < 40:
        state["decision"] = f"Rejected (Match Percentage: {state['match_percent']}%)"
    return state

def process_interview(state: SupervisorState, decision: str) -> SupervisorState:
    state = human_interview_node(state, decision)
    if decision.lower() == "rejected":
        state["decision"] = "Rejected by Interviewer"
    else:
        state = onboard_process_node(state)
    return state
