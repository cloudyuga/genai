# 🧠 LangChain-Framework – Building LLM-Powered Apps

This module covers practical LangChain examples, ranging from basic chat models to advanced RAG (Retrieval-Augmented Generation) workflows. It helps learners build production-ready LLM apps using LangChain’s core components like prompt templates, chains, tools, retrievers, and more.

---

## 🧰 Langchain Core Component Demos

| Folder                | Description                                                                 |
|------------------------|-----------------------------------------------------------------------------|
| `01_Chat_Models`       | Basic usage of chat models in finance and hr-assistant applications. (`ChatOpenAI`, `init_chat_model)`, etc.).         |
| `02_PromptTemplates`   | Create reusable prompts using `PromptTemplate`.                             |
| `03_ChatPromptTemplate`| Extend prompt templates for chat applications with roles like system/user.(Multidomain chatbot)  |
| `04_Chains`            | Link multiple steps using chain (finance-chatbot, multidomain-chatbot)              |
| `05_Embedding_Vectorstore` | Generate embeddings and store/query them using chromadb and avoid duplication in chromadb for the same pdf |
| `06_Document_Loaders`  | Load data from PDFs, URLs, CSVs using built-in loaders.             |
| `07_Retrievers`        | Implement tavily search using TavilySearchAPIRetriever.                    |
| `08_Tools`             | Use tools like `SerpAPI`, `DuckDuckGoSearchResults` and custom tools in agent workflows.  |
| `09_Multiuser_Chatbot` | Build a chatbot that supports multiple user sessions using memory.          |
| `10_MCQ_Generator_URL` | Generate MCQs from URL content using LLMs + URL loaders.                |

---

## 🧪 Included Labs

| Lab | Folder / Notebook                     | Focus Area                      | Description                                                                 |
|-----|----------------------------------------|----------------------------------|-----------------------------------------------------------------------------|
| 1   | `Lab-1-Langchain_Basic.ipynb`         | 💬 Chat Models                   | Introduction to LangChain's `ChatOpenAI` and Ollama model's usage.              |
| 2   | `Lab-2-RAG_with_Langchain.ipynb`      | 📄 RAG Pipeline                  | Build a Retrieval-Augmented Generation app using vector stores and retrievers. |

---
