# Applicatiins & Labs
## 🔍 Application Descriptions
### 1️⃣ BMI Calculator
📂 Apps/1-BMI-calculator

- A Gradio-based app that calculates Body Mass Index (BMI) based on height and weight input.

Tech stack: 
- Gradio
- Basic Python

### 2️⃣ Upload File and Process Data
📂 Apps/2-Upload-FIle-and-Process-Data

- Allows users to upload .csv files and processes the content (e.g., BMI calculation).

Use case: 
- Quick file exploration or preprocessing.

Tech stack: 
- Gradio 
- Pandas

### 3️⃣ Content Summary App
📂 Apps/3-Content-Summary-App

- Summarizes text using an OpenAI-powered model.

Use case: 
- Condense articles
- Blog posts
- Notes

Tech stack: 
- Gradio
- OpenAI API
  

### 4️⃣ Invoice Extractor
📂 Apps/4-Invoice-Extractor

- Upload an invoice image and extract key fields like date, invoice number, total etc.

Use case: 
- Automate invoice parsing.

Tech stack: 
- gradio
- PIL
- Google gemini API

### 5️⃣ Gradio Client Example
📂 Apps/5-gradio-client-example

- Demonstrates how to call a Gradio app using the gradio_client from another Python script.

Use case: 
- Programmatically interact with a deployed Gradio app.

### 6️⃣ Text to Image Generation
📂 Apps/6-Text-to-Image-Generation

- Converts user prompts into AI-generated images.

Use case: 
- Creative applications like posters, art, or storytelling.
  
Tech stack: 
- Diffusion models via Hugging Face
- gradio

### 7️⃣ MCQ Generator
📂 Apps/7-MCQGen

- Generate multiple-choice questions from a given paragraph or document.

Use case: 
- EdTech
- Quiz creation

Tech stack: 
- NLP (OpenAI or Hugging Face) 
- Gradio
- Panda (dataframe)

## 🧪 Gradio Labs Collection

### ✅ Lab-0: Prompt Execution

📄 Lab-0-Prompt_Execution.ipynb

Demo 1:
Directly call the model using Python code to understand how prompts and responses work with OpenAI's Chat API.

Demo 2:
Use Gradio to create a user-friendly interface that allows anyone to enter prompts without writing code.

👉 Behind the scenes, the prompt is still sent along with a system message to shape the assistant's behavior.

Goal: Understand how to send input to an LLM and display the response interactively with Gradio.

### 🏗️ Lab-1: Types of Gradio App

📄 Lab-1-Types_of_Gradio_App.ipynb

Description: Learn about different Gradio app interfaces: Interface, Blocks, and ChatInterface.

Goal: Understand Gradio's app structure and choose the right interface for your use case.

🎂 Lab-2: Birthday Message Apps
📄 Lab-2-Birthday_Message_Apps.ipynb

Description: Create fun birthday greeting generators with Gradio.

Goal: Generate personalized birthday messages using text input and model outputs.

🧑‍💼 Lab-3: HR Assistant
📄 Lab-3-HR_Assistant.ipynb

Description: Build an AI-powered assistant to answer HR-related queries.

Goal: Demonstrate use of prompt engineering, chat interaction, and data handling.

📄 Lab-4: Job Description Generator
📄 Lab-4-Job_Description_App.ipynb

Description: Automatically generate job descriptions based on input roles and responsibilities.

Goal: Explore practical use of LLMs in automating HR and recruitment tasks.



