# AI-Powered Job Interview Scheduler

This application leverages AI and Natural Language Processing (NLP) to schedule job interviews. It uses Named Entity Recognition (NER) to extract relevant entities (skills, names, organizations, etc.) from resumes and finds the best job match. It then schedules the interview and sends confirmation emails with Google Meet links.

## Features
- **Job Matching**: Extracts skills from resumes and matches them to predefined job descriptions using Sentence Embeddings and FAISS.
- **Entity Extraction**: Uses BERT-based NER to extract important entities like names, organizations, dates, and skills from resumes.
- **Interview Scheduling**: Schedules an interview based on the job match and sends Google Meet invites to both the candidate and the interviewer.
- **Email Sending**: Sends emails with Google Meet links to the candidate and interviewer with relevant interview details.


## Required files to run the Application
- **app.py** is a gradio application file
- Dependencies are in **requirements.txt** file (install all dependencies)
- We need **skills_list.txt** to matck skills with resume
- We need **credentials.json** to use google API's (Please refer **How-to-get-credentials.MD** file to get credentials.json)
- If you don't have resume handy. you can use our **sample-resume.MD** file to get resume
- Check the screenshot of this app from **Images** folder
