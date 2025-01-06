import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from utils import clean_text


def create_streamlit_app(llm, clean_text):
   st.title("📧 Resume Generator")
   c1, c2= st.columns(2)
   col1, col2, col3 = st.columns(3)
   
  
   with col1:
      name_input = st.text_input("Enter a Name:", value="Deepu")
   with col2:
      role_input = st.text_input("Enter a Role:", value="Software developer")
   with col3:
      exp_input = st.text_input("Enter a Experience:", value="3 year")
   with col1:
      skill_input = st.text_input("Enter a Skills:", value="Java, kotlin, Android development, LLM, ML")
   with col2:
      phone_input = st.text_input("Enter a phone:", value="123456789")
   with col3:
      email_input = st.text_input("Enter a email:", value="abc@gmail.com")
   with col1:
      proj_input = st.text_area("Projects:", value="IDBI \n Safaimitra")
   with col2:   
      edu_input = st.text_area("Education:", value="MCA \n Bsc IT")
   with col3:
      other_input = st.text_area("Other:", value="DSA, System design")
   with col1:
      url_input = st.text_input("Enter a Job URL:", value="https://www.metacareers.com/jobs/1283364266159062/")
   with col1:
      submit_button = st.button("Submit")
   
   if submit_button:
      try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            # portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
               skills = job.get('skills', [])
               # links = portfolio.query_links(skills)
               email = llm.write_resume(job,  name_input, role_input, exp_input, skill_input, phone_input,
                                       email_input,proj_input, edu_input, other_input )
               st.code(email, language='markdown')
      except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    st.set_page_config(layout="wide", page_title="Resume Generator", page_icon="💾")
    create_streamlit_app(chain, clean_text)

