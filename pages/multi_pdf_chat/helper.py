from langchain.text_splitter import RecursiveCharacterTextSplitter
from PyPDF2 import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.prompts import PromptTemplate
from langchain.chains.question_answering import load_qa_chain
from langchain_groq import ChatGroq
import streamlit as st
import os

def get_pdf_texts(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        # print(pdf)
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=1000)
    chunks = splitter.split_text(text)
    return chunks 

def get_embedding(chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") 
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    vector_store.save_local('faiss_index')

def get_conversational_chain():

    prompt_template = """
    Answer  the question as detailed as possible from the provided context. If answer is not within the provided content, just mention "Content not available".
    Context:\n{context}\n 
    Question:\n{question}\n

    Answer:\n
    """

    # model = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)

    model = ChatGroq(model="Gemma2-9b-It", groq_api_key=os.getenv('GROQ_API_KEY'))

    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

    # Build a ready-made question answering chain on top of your documents and LLM
    qa_chain = load_qa_chain(model, chain_type="stuff", prompt=prompt)

    return qa_chain


def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001") 
    vector_store = FAISS.load_local('faiss_index', embeddings, allow_dangerous_deserialization=True)
    docs = vector_store.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "question": user_question},
        return_only_outputs=True
    )
    print(response)

    st.write("Reply: ", response['output_text'])
