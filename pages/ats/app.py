
import streamlit as st 
from pages.ats.helpers import extract_resume_text, analyze_resume, upload_to_s3, getIPAddress, get_dynamodb_data
import uuid
import pandas as pd
import io

session_id = "ats_" + str(uuid.uuid4())
ip = getIPAddress()

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
            file_bytes = resume_file.read()
            s3_stream = io.BytesIO(file_bytes)
            pdf_stream = io.BytesIO(file_bytes)

            upload_to_s3(s3_stream, session_id, ip)

            resume_text = extract_resume_text(pdf_stream)
            json_data = analyze_resume(job_description, resume_text, session_id, ip)
            st.subheader("Report:")
            # st.write(result)
            if json_data is not None:
                st.write(f'Match Score: {json_data["match_score"]}')
                st.write(f'Name: {json_data["resume_metadata"]["name"]}')
                st.write(f'Experience: {json_data["resume_metadata"]["experience"]}')
                st.write(f'Skills: {json_data["resume_metadata"]["skills"]}')
                st.write(f'Summary: {json_data["summary"]}')

                # recs = {
                #     "match_score": json_data["match_score"],
                #     "name": json_data["resume_metadata"]["name"],
                #     "experience": json_data["resume_metadata"]["experience"],
                #     "skills": ", ".join(json_data["resume_metadata"]["skills"]),
                #     "summary": json_data["summary"]
                # }
                # df = pd.DataFrame([recs])
                # st.table(df)
            else:
                st.write("Failed to retrieve data")


    # Previous search results
    search_results = get_dynamodb_data(ip)
    if search_results is not None and len(search_results['Items']) > 0:
        st.write('Previous Search Results:')
        for item in search_results['Items']:
            st.markdown(f'Match Score: {item["match_score"]} {item["resume_metadata"]["name"]} {item["resume_metadata"]["experience"]} {"".join(item["resume_metadata"]["skills"])}')
            # st.write(f'Summary: {item["summary"]}')