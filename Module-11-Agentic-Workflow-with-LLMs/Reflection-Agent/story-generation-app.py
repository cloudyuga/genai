import os
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEndpoint
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph

# Load environment variables
load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

# Define prompts
generation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a creative story writer. Generate a detailed and engaging story based on the user's request in 250 words. Ensure the story is well-structured, captivating, and includes rich descriptions and characters."
            "If the user provides a specific topic or theme, ensure the story aligns with that theme."
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

reflection_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a story writer tasked with improving the provided story. Each time, refine the story to enhance its narrative flow, character development, and overall engagement. Ensure that each iteration produces a more polished and captivating version of the story."

        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Initialize LLM
llm = HuggingFaceEndpoint(
    repo_id="mistralai/Mistral-7B-Instruct-v0.3",
    huggingfacehub_api_token=HF_TOKEN,
    temperature=0.7,
    max_new_tokens=350
)

# Define chains
generate_chain = generation_prompt | llm
reflect_chain = reflection_prompt | llm

# Define nodes
def generation_node(state: Sequence[BaseMessage]):
    return generate_chain.invoke({"messages": state})

def reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res)]

# Build message graph
builder = MessageGraph()
builder.add_node("generate", generation_node)
builder.add_node("reflect", reflection_node)
builder.set_entry_point("generate")

def should_continue(state: List[BaseMessage]):
    if len(state) > 4:
        return END
    return "reflect"

builder.add_conditional_edges("generate", should_continue)
builder.add_edge("reflect", "generate")

graph = builder.compile()
print(graph.get_graph().draw_mermaid())
graph.get_graph().print_ascii()

# For testing
if __name__ == "__main__":
    print("LangGraph")
    inputs = HumanMessage(content="Write a story about animals in 150 words.")
    response = graph.invoke(inputs)
    print("Final Story:")
    for msg in response:
        print(msg.content)
