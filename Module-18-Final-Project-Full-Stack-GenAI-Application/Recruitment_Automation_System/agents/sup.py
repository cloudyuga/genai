#Working
import re
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from agents.jd_gen import jd_generator_agent
from agents.rs import resume_matcher_agent
from agents.on_board_process import onboard_agent
from db_utils import jd_collection
from typing import Tuple

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

def get_or_generate_jd(state: SupervisorState, log=print) -> SupervisorState:
    requirement = state["requirements"]
    existing_jds = jd_collection.get(include=["metadatas", "documents"])

    for doc, meta in zip(existing_jds["documents"], existing_jds["metadatas"]):
        if meta.get("requirement", "").lower().strip() == requirement.lower().strip():
            log("✅ Exact requirement match found in metadata. Get JD from Chroma")
            state["jd_output"] = doc
            state["steps_done"].append("jd_node")
            return state

    result = jd_collection.similarity_search_with_score(requirement, k=1)
    if result:
        doc, distance = result[0]
        log(f"✔ Found similar JD from Chroma (Distance: {distance:.2f})")
        if distance < 0.6:
            state["jd_output"] = doc.page_content
            state["steps_done"].append("jd_node")
            return state
        else:
            log("⚠ Distance too high, generating new JD")

    new_jd = jd_generator_agent.invoke({"requirement": requirement})["jd_output"]
    log("Added new JD to Chroma")
    jd_collection.add_texts(texts=[new_jd], metadatas=[{"requirement": requirement}])
    state["jd_output"] = new_jd
    state["steps_done"].append("jd_node")
    return state

def resume_match_node(state: SupervisorState, log=print) -> SupervisorState:
    if "resume_match_node" not in state["steps_done"]:
        
        result = resume_matcher_agent.invoke({
            "jd_output": state["jd_output"],
            "resume": state["resume"]
        })

        state["match_result"] = result["match_result"]

        match = re.search(r"(\d+)\s*%", state["match_result"])
        state["match_percent"] = int(match.group(1)) if match else 0

        #log(f"Extracted Match Percent: {state['match_percent']}")
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
def process_job(requirements: str, resume: str) -> Tuple[SupervisorState, str]:
    logs = []

    def log(msg):
        print(msg)
        logs.append(msg)

    state = SupervisorState(
        requirements=requirements,
        resume=resume,
        **initial_state
    )
    state["steps_done"] = []

    state = get_or_generate_jd(state, log)
    state = resume_match_node(state, log)

    if state["match_percent"] < 40:
        state["decision"] = f"Rejected (Match Percentage: {state['match_percent']}%)"

    return state, "\n".join(logs)


def process_interview(state: SupervisorState, decision: str) -> SupervisorState:
    state = human_interview_node(state, decision)
    if decision.lower() == "rejected":
        state["decision"] = "Rejected by Interviewer"
    else:
        state = onboard_process_node(state)
    return state
