import os
import base64
import json
import datetime
import numpy as np
import faiss
import gradio as gr
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from sentence_transformers import SentenceTransformer
from googleapiclient.errors import HttpError
import pytz
from transformers import pipeline

# Load the pre-trained BERT-based NER model from Hugging Face
ner_pipeline = pipeline("ner", model="dslim/bert-base-NER", tokenizer="dslim/bert-base-NER")
#ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")

# Function to load skills from skills_list.txt
def load_skills(file_path="skills_list.txt"):
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            skills = [line.strip().lower() for line in file.readlines()]
        return set(skills)  # Convert to set for faster lookups
    return set()

# Load skills at the start
skills_set = load_skills("skills_list.txt")

# Function to extract named entities (like name, skills, etc.) from the resume using NER model
def extract_entities(resume_text):
    # Run NER pipeline
    entities = ner_pipeline(resume_text)
    
    # Structure to store extracted entities
    extracted_entities = {
        "names": [],
        "skills": [],
        "organizations": [],
        "dates": [],
        "locations": []
    }
    
    # Process the entities
    for entity in entities:
        entity_type = entity['entity']
        entity_text = entity['word']
        
        # Check and categorize the entities
        if entity_type == "B-PER":
            extracted_entities["names"].append(entity_text)
        elif entity_type in ["B-ORG", "I-ORG"]:
            extracted_entities["organizations"].append(entity_text)
        elif entity_type in ["B-LOC", "I-LOC"]:
            extracted_entities["locations"].append(entity_text)
        elif entity_type in ["B-DATE", "I-DATE"]:
            extracted_entities["dates"].append(entity_text)

    # Extract skills from text by checking word-by-word matches from skills_list.txt
    words_in_resume = set(resume_text.lower().split())  # Convert text into set of words
    matched_skills = [skill for skill in skills_set if skill in words_in_resume]
    
    extracted_entities["skills"] = matched_skills

    return extracted_entities

# authentication
def authenticate_google():
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            "credentials.json",
            scopes=["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/calendar.events"],
            redirect_uri="http://localhost:5000/"
        )
        creds = flow.run_local_server(port=5000)
        return creds
    except Exception as e:
        print(f"Error during authentication: {e}")

# Authenticate services
creds = authenticate_google()
calendar_service = build("calendar", "v3", credentials=creds)
gmail_service = build("gmail", "v1", credentials=creds)

# Job Descriptions
job_descriptions = {
    "Python Developer": "Looking for a Python Developer with experience in Machine Learning and Data Science.",
    "Data Analyst": "Seeking a Data Analyst with expertise in SQL, Python, and visualization tools.",
    "Web Developer": "Hiring a Web Developer skilled in JavaScript, React, and backend frameworks.",
}

# Load Sentence Transformer
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Convert job descriptions into embeddings
job_titles = list(job_descriptions.keys())
job_embeddings = embedding_model.encode(list(job_descriptions.values())).astype(np.float32)

# Store embeddings in FAISS
dimension = job_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(job_embeddings)

# Function to send email with Google Meet link and clickable button
def send_email_via_gmail(subject, body, to_email, meet_link):
    try:
        message = MIMEMultipart()
        message['to'] = to_email
        message['subject'] = subject

        # HTML for email with button to join the meeting
        button_html = f"""
        <html>
            <body>
                <p>{body}</p>
                <p>
                    <a href="{meet_link}" target="_blank" style="background-color:#4CAF50;color:white;padding:14px 20px;text-align:center;text-decoration:none;display:inline-block;font-size:16px;border-radius:5px;">
                        Join with Google Meet
                    </a>
                </p>
            </body>
        </html>
        """

        message.attach(MIMEText(button_html, 'html'))  # Use 'html' to include the button

        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        send_message = gmail_service.users().messages().send(userId="me", body={'raw': raw_message}).execute()
        print(f'Email sent to {to_email} Message Id: {send_message["id"]}')
    except HttpError as error:
        print(f'An error occurred: {error}')

# Function to schedule interview and send email
def schedule_interview(candidate_name, candidate_email, interviewer_email, job_title, resume_text):
    # Define time zones for UTC and IST
    utc_timezone = pytz.timezone('UTC')
    ist_timezone = pytz.timezone('Asia/Kolkata')
    
    # Interview time (2 days and 2 hours from current UTC time)
    start_time_utc = datetime.datetime.utcnow() + datetime.timedelta(days=1, hours=2)
    start_time_utc = utc_timezone.localize(start_time_utc)
    end_time_utc = start_time_utc + datetime.timedelta(hours=1)
    
    # Convert times to IST
    start_time_ist = start_time_utc.astimezone(ist_timezone)
    end_time_ist = end_time_utc.astimezone(ist_timezone)
    
    # Construct the body for both emails
    candidate_body = f"""
    <p>Dear {candidate_name},</p>
    
    <p>Congratulations!</p>
    
    <p>You have been shortlisted for the <b>{job_title}</b> position.</p>
    
    <p>Interview Details:</p>
    <ul>
        <li><b>Position:</b> {job_title}</li>
        <li><b>Date & Time:</b> {start_time_utc.strftime('%Y-%m-%d %H:%M UTC')} / {start_time_ist.strftime('%Y-%m-%d %H:%M IST')}</li>
        <li><b>Location:</b> Google Meet</li>
    </ul>
    
    <p>Please join the meeting at the scheduled time by clicking the link below:</p>
    """

    interviewer_body = f"""
    <p>Dear interviewer,</p>
    
    <p>You are scheduled to interview <b>{candidate_name}</b> for the <b>{job_title}</b> position.</p>
    
    <p>Interview Details:</p>
    <ul>
        <li><b>Candidate:</b> {candidate_name}</li>
        <li><b>Position:</b> {job_title}</li>
        <li><b>Date & Time:</b> {start_time_utc.strftime('%Y-%m-%d %H:%M UTC')} / {start_time_ist.strftime('%Y-%m-%d %H:%M IST')}</li>
        <li><b>Location:</b> Google Meet</li>
    </ul>
    
    <p>Please evaluate the candidate based on the following criteria:</p>
    <ul>
        <li><b>Technical Skills:</b> Assess their proficiency with relevant programming languages and tools.</li>
        <li><b>Problem-Solving Ability:</b> Evaluate their approach to solving coding problems and challenges.</li>
        <li><b>Communication Skills:</b> Pay attention to how effectively they explain their ideas and thoughts.</li>
        <li><b>Cultural Fit:</b> Consider how well their values align with the team and company culture.</li>
        <li><b>Experience:</b> Review the relevance of their experience in relation to the job role.</li>
    </ul>
    
    <p>Please join the meeting at the scheduled time by clicking the link below:</p>
    """
    
    # Create Google Meet event
    event = {
        "summary": f"Interview with {candidate_name} for {job_title}",
        "location": "Google Meet",
        "description": candidate_body,
        "start": {"dateTime": start_time_utc.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_time_utc.isoformat(), "timeZone": "UTC"},
        "attendees": [{"email": interviewer_email},{"email": candidate_email}],
        "conferenceData": {
            "createRequest": {
                "requestId": "meet"
            }
        }
    }

    try:
        # Insert event into Google Calendar
        event = calendar_service.events().insert(calendarId="primary", body=event, conferenceDataVersion=1).execute()
        meet_link = event['hangoutLink']  # Extracting the Google Meet link directly
        
        # Send emails to candidate and interviewer
        send_email_via_gmail("Interview Scheduled", interviewer_body, interviewer_email, meet_link)
        send_email_via_gmail("Interview Scheduled", candidate_body, candidate_email, meet_link)

        return f"✅ Interview Scheduled: {meet_link}"
    except Exception as e:
        return f"Error scheduling interview: {str(e)}"

# Function to find best job match (with entity extraction)
def find_best_match(resume_text):
    # Extract entities from resume
    entities = extract_entities(resume_text)
    print(f"Extracted Entities: {entities}")  # For debugging
    
    # Check if any skills are matched
    matched_skills = entities.get("skills", [])
    if not matched_skills:
        return "No skills match any job title", entities  # Return no match if no skills are found

    # Proceed with job matching (using embeddings as before)
    resume_embedding = embedding_model.encode([resume_text]).astype(np.float32)
    index_result = index.search(resume_embedding, 1)[1]
    best_job = job_titles[index_result[0][0]]
    
    return best_job, entities


# Gradio UI
with gr.Blocks() as demo:
    gr.Markdown("# 📝 AI-Powered Job Interview Scheduler")
    
    with gr.Row():
        resume_input = gr.Textbox(label="Paste Resume Text Here")
    
    with gr.Row():
        job_output = gr.Textbox(label="Best Job Match", interactive=False)
        entities_output = gr.JSON(label="Extracted Entities")

    with gr.Row():
        match_button = gr.Button("Get Best Job Match")

    with gr.Row():
        candidate_name = gr.Textbox(label="Candidate Name")
        candidate_email = gr.Textbox(label="Candidate Email")
        interviewer_email = gr.Textbox(label="Interviewer Email")
        schedule_button = gr.Button("Schedule Interview")
        result_output = gr.Textbox(label="Interview Confirmation", interactive=False)

    # Bind "Get Best Job Match" button to find_best_match function
    match_button.click(find_best_match, inputs=resume_input, outputs=[job_output, entities_output])

    # Bind "Schedule Interview" button to schedule_interview function
    schedule_button.click(schedule_interview, inputs=[candidate_name, candidate_email, interviewer_email, job_output, resume_input], outputs=result_output)

demo.launch()
