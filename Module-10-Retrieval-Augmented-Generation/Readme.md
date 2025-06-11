# 🔍 Retrieval-Augmented Generation (RAG) Module

This module contains hands-on labs and mini-projects that demonstrate **RAG pipelines** using OpenAI LLMs and various vector databases (ChromaDB, Pinecone). The focus is on building question-answering systems over paragraph text, PDFs, and HR datasets.

---

## 📁 Contents

### 📦 Mini Projects

| Folder | Description |
|--------|-------------|
| `1-Chat-with-Paragraph` | Simple RAG example using static paragraph input, cosine similarity and OpenAI GPT. |
| `2-Chat-with-PDF` | Upload and query PDFs using text chunking, embeddings, cosine similarity and OpenAI GPT. |

---

### 📒 Labs

| Notebook | Description |
|----------|-------------|
| `Lab-0-Chat_with_Paragraph.ipynb` | RAG using a single paragraph (basic intro). |
| `Lab-1-Chat_with_Paragraphs.ipynb` | To generate a response, we embed a corpus of paragraphs and the question, retrieve the most relevant paragraph based on cosine similarity, provide it as context to the LLM, and generate the final response. |
| `Lab-2-Chat_with_PDF.ipynb` | RAG pipeline over PDFs with chunking and embedding, cosine similarity and response generation using LLM. |
| `Lab-3-Chroma_hrdataset_QA.ipynb` | Use **ChromaDB** to query HR policies and employee details. |
| `Lab-4-Pinecone_Gradio_HR_dataset_QA.ipynb` | Use **Pinecone** with **Gradio** UI for querying HR data. |
| `Lab-5-Hybrid_Search_with_Pinecone.ipynb` | Combine keyword and vector search (hybrid retrieval) using Pinecone. |

---

## 🧠 Concepts Covered

- 🔎 Text chunking and preprocessing
- 📚 Vector embedding with OpenAI
- 🧠 Similarity search using ChromaDB & Pinecone
- 💬 OpenAI chat completions for QA
- 🌐 Gradio-based frontends for interactive RAG
- 🔁 Hybrid search: keyword + semantic

---
