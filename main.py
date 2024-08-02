import streamlit as st
from process_resume import process_resume_file



if __name__=="__main__":
    st.title("RESUME PARSER")
    file=st.file_uploader("**Upload Resume**",type='pdf')
    if file:
        response_json_data=process_resume_file(file)
        if response_json_data:
            
            work_experience_list=response_json_data["work_experience"]
            work_experience_len=len(work_experience_list)
            st.header("**Candidate Details**")
            candidate_name_input=st.text_input(label="**NAME**",value=response_json_data["name"])
            candidate_email_input=st.text_input(label="**EMAIL**",value=response_json_data["email"])
            candidate_phone_number_input=st.text_input(label="**PHONE NUMBER**",value=response_json_data["phone"])
            candidate_location_input=st.text_input(label="**LOCATION**",value=response_json_data["location"])
            candidate_summary_input=st.text_area(label="**SUMMARY**",value=response_json_data["summary"])
            candidate_skill_input=st.text_area(label="**SKILLS**",value=response_json_data["skills"])
            st.header("**Work Experience**")
            for i in range(0,work_experience_len):
                print(work_experience_list[i])
                work_experience=work_experience_list[i]

                company_name_input=st.text_input(label="**COMPANY NAME**",value=work_experience["company"])
                company_job_title_input=st.text_input(label="**JOB TITLE**",value=work_experience["job_title"])
                start_input=st.text_input(label="**START**",value=work_experience["start_date"])
                end_input=st.text_input(label="**END**",value=work_experience["end_date"])
                