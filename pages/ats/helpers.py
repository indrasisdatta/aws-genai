
from dotenv import load_dotenv
import os 
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from PyPDF2 import PdfReader
import json 
import boto3
import botocore
import re

load_dotenv()

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)

def parse_json_response(response_text):
    print('JSON response: ', response_text)
    try:
        # Remove Markdown formatting like ```json ... ```
        cleaned = re.sub(r"```(json)?", "", response_text, flags=re.IGNORECASE).strip()

        # Optional: ensure it starts and ends properly
        start = cleaned.find("{")
        end = cleaned.rfind("}") + 1
        cleaned_json = cleaned[start:end]

        return json.loads(cleaned_json)
    except json.JSONDecodeError:
        print("Invalid JSON")
        return None
    
# Extract text from PDF
def extract_resume_text(file):
    file.seek(0)
    reader = PdfReader(file)
    resume_text = ''
    for i in range(len(reader.pages)):
        page = reader.pages[i]
        print(page.extract_text())
        resume_text += page.extract_text()
    return resume_text

'''Each section should be short and concise:
    - Percentage match
    - Key skills of Candidate
    - Strengths
    - Weaknesses
    - Keywords missing'''

# Analyze resume based on Job description and extracted Resume text
def analyze_resume(job_description, resume_text, session_id):
    template_str = """You are an experienced HR with technical expertise in Web Development (Frontend + Backend), 
    Artificial Intelligence, Machine Learning, Data Science, DevOps, and Cloud.
    Compare the following job description and candidate resume. 
    
    Respond only with a valid JSON object. Do not include any explanations or text outside the JSON. Use escape characters if it contains quotes within list. 
    Sample JSON response: 
    {{"match_score": 87, "resume_metadata": {{"experience": "5 years", "name": "John", "skills": "[\"Python\", \"AWS\"]"}}, "summary": "Strong backend developer with AWS experience"}}

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
    
    json_data = parse_json_response(result)

    if json_data is not None:
        json_data['session_id'] = session_id
        save_dynamodb_data(json_data)
    
    return json_data

def save_dynamodb_data(json_data):
    if json_data is not None:
        try:
            session = boto3.Session(profile_name=os.getenv('AWS_PROFILE'))
            dynamodb = session.resource('dynamodb', region_name="ap-south-1")
            table = dynamodb.Table('ResumeAnalysis')
            table.put_item(Item=json_data)
            return True
        except botocore.exceptions.ClientError as e:
            print(e)
            return None
        
def upload_to_s3(uploaded_file, session_id):
    bucket_name = os.getenv('AWS_S3_UPLOAD_BUCKET')
    session = boto3.Session(profile_name=os.getenv('AWS_PROFILE'))
    s3 = session.client('s3')

    try:
        s3_key = f"ats_pdf/{session_id}.pdf"
        s3.upload_fileobj(uploaded_file, bucket_name, s3_key)
        return True
    except botocore.exceptions.ClientError as e:
        print(e)
        return False   