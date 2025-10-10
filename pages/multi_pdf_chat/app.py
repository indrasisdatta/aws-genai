from requests import session
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from pages.multi_pdf_chat.helper import generate_embedding, get_pdf_texts, get_text_chunks, user_input, getIPAddress, _get_session

from dotenv import load_dotenv
import streamlit as st
import os
import uuid

load_dotenv()

os.environ["HUGGINGFACEHUB_API_TOKEN"] = os.getenv("HUGGINGFACE_TOKEN")

def main():
    # Initialize Gemini 
    # genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))  

    # Streamlit initialize
    st.set_page_config(page_title="PDF Chat")
    st.header("PDF Chat")

    session_id = str(uuid.uuid4())

    user_question = st.text_input("Ask your Question from the PDF Files")
    submit_btn = st.button("Search from uploaded file")
    submit_btn2 = st.button("Search from previously uploaded files")

    if user_question and (submit_btn or submit_btn2):
        # if submit_btn:
        #     session_id = str(uuid.uuid4())
        # elif submit_btn2:
        if submit_btn2:
            session_id = "17decbd4-92e7-4d9d-9736-92841f367d8c"
        user_input(user_question, session_id)

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader(
            "Upload your PDF files and click on the Submit and Process button below",
            type=["pdf"],
            accept_multiple_files=True
        )
        # if st.button("Submit and Process"):
        if pdf_docs:
            with st.spinner("Uploading and Processing..."):
                raw_text = get_pdf_texts(pdf_docs)
                chunks = get_text_chunks(raw_text)
                generate_embedding(chunks, session_id)
                st.success('Done')

