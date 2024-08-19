# output_structure.py

import os
import json
from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum
import fitz
import instructor
import anthropic
from dotenv import load_dotenv

load_dotenv()

class SeniorityLevel(str, Enum):
    junior = "Junior"
    mid = "Mid"
    senior = "Senior"
    lead = "Lead"

class WorkExperience(BaseModel):
    company_name: str = Field(..., description="Name of the company")
    position: str = Field(..., description="Position or title held at the company")
    duration_years: int = Field(..., description="Duration of employment in years")
    achievements: List[str] = Field(..., description="Key achievements in this role")

class Resume(BaseModel):
    name: str = Field(..., description="Full name of the individual")
    title: str = Field(..., description="Title of the individual")
    location: str = Field(..., description="Current location or address")
    linkedin: Optional[str] = Field(None, description="LinkedIn profile URL")
    github: Optional[str] = Field(None, description="GitHub profile URL")
    contact: Optional[str] = Field(None, description="Phone number or other contact information")
    email: str = Field(..., description="Email address")
    summary: str = Field(..., description="Brief professional summary or objective statement")
    years_of_experience: int = Field(..., description="Total years of professional experience")
    seniority: SeniorityLevel = Field(..., description="Seniority level of the individual")
    work_experience: List[WorkExperience] = Field(..., description="List of work experiences")
    education: str = Field(..., description="Education summary")
    skills: str = Field(..., description="Skills summary")
    certifications: str = Field(..., description="Certifications summary")
    projects: str = Field(..., description="Projects summary")

    def to_json(self, file_path: str):
        """Save the Resume data as a JSON file."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.model_dump(), f, indent=4, ensure_ascii=False)

def read_pdf(file_path: str) -> str:
    pdf_document = fitz.open(file_path)
    all_text = ""
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        text = page.get_text()
        all_text += f"\n{text}"
    return all_text

def process_resume(resume_path: str) -> Optional[Resume]:
    api_key = os.getenv('ANTHROPIC_API_KEY')
    resume_text = read_pdf(resume_path)
    
    client = instructor.from_anthropic(anthropic.Anthropic(api_key=api_key))

    try:
        reply = client.chat.completions.create(
            model="claude-3-5-sonnet-20240620",
            response_model=Resume,
            max_tokens=4096,
            max_retries=3,
            messages=[
                {"role": "system", "content": "Analyze the incoming resume and fill the values for the Resume structure."},
                {"role": "user", "content": resume_text}
            ]
        )
        return reply
    except Exception as e:
        print(f"Error processing resume: {e}")
        return None

def main():
    resume = process_resume('./resume.pdf')
    if resume:
        resume.to_json('./resume.json')
    else:
        print("Failed to process the resume.")

if __name__ == '__main__':
    main()
