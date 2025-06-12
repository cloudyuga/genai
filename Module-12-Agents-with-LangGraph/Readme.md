# 🤖 LangGraph Module – Agentic Workflows with Human-in-the-Loop

This module focuses on **LangGraph**, a powerful extension of LangChain for building agentic, graph-based workflows. It introduces branching logic, cycles, memory, streaming, and real-time interaction with human feedback.

---

## 🔧 Core LangGraph Notebooks : /LangGraph

| Code | Notebook File                                     | Feature Focus                        | Description                                                                 |
|------|---------------------------------------------------|--------------------------------------|-----------------------------------------------------------------------------|
| LG01 | `LG01_Basic_Concepts.ipynb`                       | 🌱 Basics                            | Learn about nodes, state, and edge in LangGraph + Conditional edges .                |
| LG02 | `LG02_HR__Policy_Assistant.ipynb`                | 📃 Simple Assistant                  | HR Assistant bot using LLM.                             |
| LG03 | `LG03_ReAct_Agents_Basic.ipynb`                  | 🔄 ReAct Loop                        | Build a reasoning+acting agent from scratch with LangGraph using simple math functions.                 |
| LG04 | `LG04_Chain_HR_Policy_Assistant.ipynb`           | 🔗 Chaining Nodes                    | Combine multiple tools in a LangGraph workflow to generate response.                  |
| LG05 | `LG05_RAG_with_Langgraph.ipynb`                  | 🔍 RAG                               | Retrieval-Augmented Generation pipeline with LangGraph.                     |
| LG06 | `LG06_Weather_News_Agents.ipynb`                 | 🌦️ Agent Use Case                    | Weather & news agents demo using 3rd party API. Output: `LG06_*.png`.      |
| LG07 | `LG07_Human_in_loop_branch_and_cycle_in_graph.ipynb` | 🔄 Branch + Cycle + Human Loop   | LLM back in a looped and ask human to repharse the query if it is not relevent.                   |
| LG08 | `LG08_Streaming.ipynb`                           | 🧵 Streaming Responses               | Implement token-by-token streaming using LangGraph + async.                 |
| LG09 | `LG09_Chatbot_with_Memory_and_Thread.ipynb`      | 💬 Chat Memory + Threading          | Stateful conversation with threaded memory over sessions.                   |
| LG10 | `LG10_Multi_Agent_Human_In_Loop.ipynb`           | 👥 Multi-Agent + Human Feedback Loop       | Coordinate multiple agents with human judgment loop in complex tasks like automated recruitment system.       |
| LG11 | `LG11_Human_In_the_Loop.ipynb`                   | 🧑‍💼 Feedback Decisions              | Manual decision branching using human input before proceeding.              |

---

## 🧪 Included Labs Overview

| Lab | Notebook File                                     | Focus Area                          | Description                                                                 |
|-----|---------------------------------------------------|--------------------------------------|-----------------------------------------------------------------------------|
| 1   | `Lab-1-Agentic_Workflow_with_Langgraph.ipynb`     | 🔁 Agentic Flow                      | Intro to building agent with tools using LangGraph workflow.   |
| 2   | `Lab-2-hr_assistant_with_memory.ipynb`            | 🧠 Memory                    | HR Assistant using LangGraph + document + memory + retrieval capabilities.    |
| 3   | `Lab-3-Connect_LangSmith.ipynb`                   | 📡 Observability                     | Track executions using LangSmith integration for LangGraph workflows.       |
| 4   | `Lab-4-Langsmith_Langgraph_Demo.ipynb`            | 📊 Evaluation + Tracing              | Poem critique demo with LangSmith, storing intermediate steps and scores.   |

---


## 🖼️ Visual Outputs

| File Name                         | Description                          |
|----------------------------------|--------------------------------------|
| `Lab-4-poem--AI-msg.png`         | AI-generated poem message screenshot |
| `Lab-4-poem-human-msg.png`       | Human critique message screenshot     |
| `Lab-4-poem_critique_attemps.png`| Iteration output with scoring         |
| `LG06_Weather_News_Agent_Output.png` | Multi-agent demo output visualization |

---
