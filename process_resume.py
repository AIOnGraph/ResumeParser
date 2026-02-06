
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import List
import json
import streamlit as st
import PyPDF2
from langchain_groq import ChatGroq
from langchain_openai import OpenAI,ChatOpenAI

class WorkExperience(BaseModel):
    company: str = Field(description="This is the comapny name")
    job_title:str = Field(description="This is the job title in this company.")
    start_date:str = Field(description="This is the start date in this company")
    end_date:str=Field(description="This is the end date in this company.")

class ResumeDetails(BaseModel):
    name: str = Field(description="Resume candidate name")
    email:str=Field(description="candidate email id")
    phone:str=Field(description="candidate phone number, or contact number")
    location:str=Field(description="candidate current location")
    summary:str=Field(description="This is the summary or objective data provided in resume extracted data")
    skills: list = Field(description="skills of candidate inside the resume")
    work_experience:List[WorkExperience]


class LangchainResponse:

    def __init__(self, openai_api_key: str):
        if not openai_api_key:
            raise ValueError("OpenAI API key must be provided via the UI")
        self.model = ChatOpenAI(openai_api_key=openai_api_key)
        self.parserforsampleinvoice = JsonOutputParser(pydantic_object=ResumeDetails)
        

    def genereate_response_for_sample_invoices(self, resume_extracted_data):
        prompt = PromptTemplate(
            template="User will give resume extracted data.\n you will give the details,\n{format_instructions}\n"
            "Resume_data:{resume_extracted_data}"
            "Note: only return the json data in json format",
            input_variables=["resume_extracted_data"],
            partial_variables={
                "format_instructions": self.parserforsampleinvoice.get_format_instructions()
            },
        )

        prompt_and_model = prompt | self.model
        output = prompt_and_model.invoke(
            {"resume_extracted_data": resume_extracted_data}
        )

        response = output.content
        # print(response)
        start_index = response.find("{")
        end_index = response.rfind("}") + 1
        json_str = response[start_index:end_index]

        data = json.loads(json_str)
        # print(data)
        return data
    

def extract_data_from_resume(pdf_file_path):
    read_pdf = PyPDF2.PdfReader(pdf_file_path)
    number_of_pages = len(read_pdf.pages)
    resume_text = ''
    for page in read_pdf.pages:
        page_content = page.extract_text()
        if page_content:
            resume_text += page_content
    return resume_text

def process_resume_file(path, openai_api_key: str):
    resume_extracted_data = extract_data_from_resume(path)
    response = LangchainResponse(openai_api_key).genereate_response_for_sample_invoices(resume_extracted_data)
    print(response)
    return response



# if __name__=="__main__":
#     path=input("enter path of resume pdf ")
#     resume_extracted_data=extract_data_from_resume(path)
#     response=LangchainResponse().genereate_response_for_sample_invoices(resume_extracted_data)
#     print(response)
