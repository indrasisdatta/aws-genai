from langchain_google_genai import GoogleGenerativeAIEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import google.generativeai as genai
from pages.multi_pdf_chat.helper import get_embedding, get_pdf_texts, get_text_chunks, user_input


from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

def main():
    # Initialize Gemini 
    genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))  

    # Streamlit initialize
    st.set_page_config(page_title="PDF Chat")
    st.header("PDF Chat")

    user_question = st.text_input("Ask your Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu")
        pdf_docs = st.file_uploader(
            "Upload your PDF files and click on the Submit and Process button below",
            type=["pdf"],
            accept_multiple_files=True
        )
        if st.button("Submit and Process"):
            with st.spinner("Processing..."):
                raw_text = get_pdf_texts(pdf_docs)
                chunks = get_text_chunks(raw_text)
                get_embedding(chunks)
                st.success('Done')

