
from dotenv import load_dotenv
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from PyPDF2 import PdfReader

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)

# Extract text from PDF
def extract_resume_text(file):
    reader = PdfReader(file)
    resume_text = ''
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        print(page.extract_text())
        resume_text += page.extract_text()
    return resume_text

# Analyze resume based on Job description and extracted Resume text
def analyze_resume(job_description, resume_text):
    template_str = """You are an experienced HR with technical expertise in Web Development (Frontend + Backend), 
    Artificial Intelligence, Machine Learning, Data Science, DevOps, and Cloud.
    Compare the following job description and candidate resume. 
    Each section should be short and concise:
    - Percentage match
    - Key skills of Candidate
    - Strengths
    - Weaknesses
    - Keywords missing

    Job Description:
    {job_description}

    Candidate Resume:
    {resume_text}
    """
    prompt = ChatPromptTemplate.from_template(template_str)
    parser = StrOutputParser()

    chain = prompt | llm | parser

    result = chain.invoke({
        "job_description": job_description,
        "resume_text": resume_text
    })
    return result