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
class InputState(TypedDict):
    requirement: str  # HR input like "Need a Python Backend Engineer"

class OutputState(TypedDict):
    jd_output: str

class JDState(InputState, OutputState):
    # The "messages" field accumulates BaseMessage objects and is reduced via operator.add
    messages: Annotated[List[BaseMessage], add]

# --------------------------
# Step 2: Define Tool
# --------------------------
@tool
def generate_jd(role_description: str) -> str:
    """Generate a job description for the given role"""
    return f"Auto-generated JD for: {role_description}"  # placeholder

tools_jd = [generate_jd]

# --------------------------
# Step 3: Agent Logic
# --------------------------

def call_model_jd_generator(state: JDState) -> JDState:
    # Lazily instantiate LLM and bind tools
    llm = get_llm()
    model_jd = llm.bind_tools(tools_jd)

    local_messages = state.get("messages", [])
    if not local_messages:
        local_messages.append(HumanMessage(content=state["requirement"]))

    system_message = SystemMessage(content="""
You are a professional HR assistant.
Generate a clear, concise job description using the provided requirement in 50 words.
""")

    # Invoke the model
    response = model_jd.invoke([system_message] + local_messages)

    # Update state
    state["jd_output"] = response.content
    state["messages"] = local_messages + [response]
    return state


def should_continue_jd(state: JDState) -> Literal["tools", END]:
    last_message = state["messages"][-1]
    if getattr(last_message, "tool_calls", None):
        return "tools"
    return END

# --------------------------
# Step 4: JD Agent Subgraph
# --------------------------
jd_graph = StateGraph(JDState, input=InputState, output=OutputState)
jd_graph.add_node("call_model_jd_generator", call_model_jd_generator)
jd_graph.add_node("tools", ToolNode(tools_jd))
jd_graph.add_edge(START, "call_model_jd_generator")
jd_graph.add_conditional_edges("call_model_jd_generator", should_continue_jd)
jd_graph.add_edge("tools", "call_model_jd_generator")

# Compile agent
jd_generator_agent = jd_graph.compile()
