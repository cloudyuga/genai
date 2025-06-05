# Working
import gradio as gr
from agents.sup import process_job, process_interview, SupervisorState
from utils import extract_text
import os

with gr.Blocks() as demo:
    gr.Markdown("### 🧠 Supervisor Agent — Resume Screening")

    api_key_input = gr.Textbox(label="🔑 Enter your API Key", type="password")

    with gr.Row():
        requirements = gr.Textbox(label="Job Requirement", lines=3)
        resume_upload = gr.File(label="Upload Resume (PDF, DOCX, or TXT)", file_types=[".pdf", ".docx", ".txt"])

    submit_btn = gr.Button("Evaluate Candidate")

    state_json = gr.State()

    output_log = gr.Textbox(label="JD Generation Status", lines=3)
    jd_out = gr.Textbox(label="Generated JD")
    match_result = gr.Textbox(label="Resume Match Result")
    interview_dropdown = gr.Radio(choices=["Selected", "Rejected"], label="Interview Result")
    interview_dropdown.visible = False
    interview_btn = gr.Button("Submit Interview Decision")
    interview_btn.visible = False

    final_output = gr.Textbox(label="Final Decision")

    def on_submit(api_key, requirements, resume_file):
        os.environ["OPENAI_API_KEY"] = api_key
        resume_text = extract_text(resume_file)
        state, logs = process_job(requirements, resume_text)
        #print("Match Percentage:", state["match_percent"])
        show_interview = state["match_percent"] >= 40

        return (
            state,
            state["jd_output"],
            state["match_result"],
            gr.update(visible=show_interview), #interview_dropdown visibility
            gr.update(visible=show_interview), #interview_btn visibility
            state["decision"],
            logs
        )

    def on_interview(state, decision):
        state = process_interview(state, decision)
        return state, state["decision"]

    submit_btn.click(
    fn=on_submit,
    inputs=[api_key_input, requirements, resume_upload],
    outputs=[state_json, jd_out, match_result, interview_dropdown, interview_btn, final_output,output_log]
    )

    interview_btn.click(
        fn=on_interview,
        inputs=[state_json, interview_dropdown],
        outputs=[state_json, final_output]
    )

#demo.launch()
demo.launch(server_name="0.0.0.0", server_port=7860)
