
import streamlit as st 
from pages.ats.helpers import extract_resume_text, analyze_resume

def main():
    # Streamlit initialize
    st.set_page_config(page_title="ATS Checker")
    st.header("ATS Checker for your Resume")

    # Inputs 
    job_description = st.text_area(label="Job Description", placeholder="Enter full Job Descrition here", key="input")
    resume_file = st.file_uploader(label="Upload Resume (PDF)", type=["pdf"])

    submit_btn = st.button("Analyze")

    if submit_btn:
        if not job_description:
            st.warning("Please enter Job description")
        elif not resume_file:
            st.warning("Please upload your resume")
        else:
            resume_text = extract_resume_text(resume_file)
            result = analyze_resume(job_description, resume_text)
            st.subheader("Report:")
            st.write(result)