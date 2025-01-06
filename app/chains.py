import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama3-8b-8192")

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_resume(self, job, name, role, exp, skill, phone, email,
                     proj, edu, other):
        prompt_email = PromptTemplate.from_template(
            """
           ### Instruction for Generating a Resume Response

            #### Objective:
            To create a well-structured and professional resume for a specific {role}, incorporating the individual's professional experience, skills, achievements, and other relevant details. The resume should align with industry standards and highlight the candidate's strengths.

            #### Input Information:
            1. Candidate's name {name} and current role {role}.
            2. Key technical skills and expertise.
            3. Summary of professional experience with company names, roles, and durations.
            4. List of significant projects {proj} completed, with brief descriptions.
            5. Personal interests relevant to the role or industry.
            6. Contact information ({email}, {phone}).

            #### Output Structure:
            The generated resume must include the following sections:
            1. **Header**: Candidate's name {name} and title {role}.
            2. **Contact Information**: Email, phone
            3. **Professional Summary**: A concise overview of the candidate's expertise and career highlights.
            4. **Professional Experience**: Detailed description of roles {role}, responsibilities, and accomplishments in reverse chronological order.
            5. **Skills**: Categorized list of technical and professional skills {skill}.
            6. **Projects**: Highlights of key projects, mentioning technologies used and outcomes {proj}.
            7. **Other details**: Relevant activities that showcase the candidate's engagement with the industry or technical community {other}.

            #### Formatting Guidelines:
            - Use professional language and avoid grammatical errors.
            - Present information concisely, ensuring clarity and readability.
            - Use bullet points for responsibilities, skills, and achievements.
            - Align the formatting to emphasize important details like roles, skills, and accomplishments.

            #### Example Output:
            The generated resume must look similar to the following format:

            **[Name]**

            **[Title/Role]**

            **Contact Information**  
            Email: [Candidate's Email Address]  
            Phone: [Candidate's Phone Number]  
            LinkedIn: [Candidate's LinkedIn Profile]  
            GitHub: [Candidate's GitHub Profile]  

            ---

            **Professional Summary**  
            [A brief paragraph summarizing the candidate's expertise, experience, and core competencies.]

            ---

            **Professional Experience**  
            **[Role]**  
            **[Company Name]**  
            *[Start Date – End Date]*  
            - [Responsibility/Accomplishment #1]  
            - [Responsibility/Accomplishment #2]  

            (Repeat for each role in reverse chronological order)

            ---

            **Skills**  
            [List of categorized technical and professional skills.]

            ---

            **Achievements**  
            [List of notable achievements or awards.]

            ---

            **Education**  
            **[Degree Name]**  
            [University Name], [Year of Graduation]  
            - Relevant Coursework: [Course #1], [Course #2]  

            ---

            **Projects**  
            - **[Project Name]:** [Brief description including technologies and outcomes.]

            ---

            #### Notes:
            - Personalize the resume for the specific role or industry.
            - Highlight achievements and skills most relevant to the job requirements.

            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "name":name, "role":role,
                    "exp":exp, "skill":skill, "phone":phone,"email": email,
                     "proj":proj, "edu":edu, "other":other})
        return res.content

if __name__ == "__main__":
    print(os.getenv("GROQ_API_KEY"))
