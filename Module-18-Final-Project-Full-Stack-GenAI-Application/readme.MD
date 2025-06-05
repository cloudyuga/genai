
# 🧠 Full Stack AI-Powered Recruitment System

This is a full-stack AI application that evaluates candidate resumes against job requirements using LLMs and stores/generates job descriptions (JDs) with semantic search using **ChromaDB**. It integrates **LangChain agents** to simulate a full interview and onboarding process.

---

## 🚀 Features

- 🔍 **Hybrid RAG-based JD Retrieval**: Retrieves JDs via metadata matching and semantic search (ChromaDB).
- 📝 **JD Generation Agent**: Generates a job description if no similar JD is found.
- 📄 **Resume Matching Agent**: Evaluates resumes against the JD and calculates a match score.
- 👤 **Human-like Interview Process**: Simulates an interview and onboarding process.
- 💾 **Chroma Vector DB**: Used for storing and retrieving JDs with similarity search.
- 🎛️ **Gradio UI**: Simple interface for interacting with the system.

---

## 📁 Folder Structure

Full_Stack_App/
│

├── app.py # Main Gradio app entry point

├── db_utils.py # Chroma DB connection and utility methods

├── docker-compose.yaml # Compose file to run app with ChromaDB

├── Dockerfile # Dockerfile for the app

├── requirements.txt # Required Python packages

├── utils.py # Helper functions (We have use gpt-4o-mini, you can change the model to gpt-4.1)

│

├─────agents/

│ ├──────── jd_gen.py # JD Generator agent

│ ├──────── rs.py # Resume match agent

│ ├──────── sup.py # Supervisor agent orchestrating the flow

│ └──────── on_board_process.py # Onboarding agent

---
##### Note: You can remove Sample Resumes and Output folder from your actual folder structure. They are just for reference. 

## ⚙️ Installation

### **Clone the repository**

```bash
git clone https://github.com/cloudyuga/mastering-genai-w-python.git
cd mastering-genai-w-python/Module-18-Final-Project-Full-Stack-GenAI-Application/Recruitment_Automation_System
```

## Run the Application

### **Run the app locally with persist directory** 

**Step 1:** Install dependencies
```
pip install -r requirements.txt
```
**Step 2:** Remove the existing db_utils.py file.

**Step 3:** Rename persist_db_utils.py to db_utils.py.

**Step 4:** To run the application locally with a persistent directory for ChromaDB, use the following command:
```
python app.py
```
**Step 5:** Open URL http://localhost:7860 for Gradio UI

---

## **OR**

---
### **Run this application using Docker:**

**Step 1:** Remove persist_db_utils.py

**Step 2:** Run the following command,
```
docker-compose up
```
**Step 3:** Open URL http://localhost:7860 for Gradio UI

## 🧪 How it Works?
- User provides OpeanAI API key, a job requirement and uploads a resume.

- App checks ChromaDB for a similar JD using metadata → semantic search → fallback to generation.

- The resume_match_node compares the resume and JD using a LangChain agent.

- If match percent ≥ threshold, simulate interview → onboarding.

## 📝 Example
Input:

API key: ******

Requirement: Doctor	

Resume: atul-resume.txt	

Output:

JD Status, JD Generated or Retrieved

Match %: 90%, Decision: Selected OR 5% Decision: Rejected


