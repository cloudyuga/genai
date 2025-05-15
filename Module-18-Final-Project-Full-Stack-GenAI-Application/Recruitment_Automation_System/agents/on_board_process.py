from typing import TypedDict, Literal, Annotated, List
from operator import add
from langchain_core.messages import HumanMessage, SystemMessage, BaseMessage
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode
from langchain_core.tools import tool
from utils import get_llm

# ---------------------------
# Step 1: Define State Schema
# ---------------------------
class OnboardInputState(TypedDict):
    resume: str
    jd_output: str

class OnboardOutputState(TypedDict):
    onboarding_result: str

class OnboardState(OnboardInputState, OnboardOutputState):
    # The "messages" field accumulates BaseMessage objects and is reduced via operator.add
    messages: Annotated[List[BaseMessage], add]

# --------------------------
# Step 2: Define Tool
# --------------------------
@tool
def simulate_onboarding(resume: str, jd_output: str) -> str:
    """Simulate onboarding process for selected candidate"""
    return f"Candidate with resume '{resume[:30]}...' has been successfully onboarded for JD: '{jd_output[:30]}...'"

tools_onboard = [simulate_onboarding]

# --------------------------
# Step 3: Agent Logic
# --------------------------
def call_onboarding_model(state: OnboardState) -> OnboardState:
    # Lazily instantiate LLM and bind onboarding tool
    llm = get_llm()
    model_onboard = llm.bind_tools(tools_onboard)

    local_messages = state.get("messages", [])
    if not local_messages:
        content = (
            f"Onboard candidate with the following JD:\n{state['jd_output']}\n\n"
            f"Resume:\n{state['resume']}"
        )
        local_messages.append(HumanMessage(content=content))

    system_message = SystemMessage(
        content="You are an onboarding automation assistant. Complete onboarding based on JD and resume."
    )

    response = model_onboard.invoke([system_message] + local_messages)

    state["onboarding_result"] = response.content
    state["messages"] = local_messages + [response]
    return state

# --------------------------
# Step 4: Continuation Logic
# --------------------------
def should_continue_onboarding(state: OnboardState) -> Literal["tools", END]:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END

# --------------------------
# Step 5: Onboarding Agent Graph
# --------------------------
onboard_graph = StateGraph(OnboardState, input=OnboardInputState, output=OnboardOutputState)
onboard_graph.add_node("call_onboarding_model", call_onboarding_model)
onboard_graph.add_node("tools", ToolNode(tools_onboard))
onboard_graph.add_edge(START, "call_onboarding_model")
onboard_graph.add_conditional_edges("call_onboarding_model", should_continue_onboarding)
onboard_graph.add_edge("tools", "call_onboarding_model")

onboard_agent = onboard_graph = onboard_graph = onboard_graph.compile()  # compiled agent