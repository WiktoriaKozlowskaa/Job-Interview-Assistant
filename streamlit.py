import streamlit as st
import openai
from crewai import Agent, Task, Crew
from crewai_tools import FileReadTool, ScrapeWebsiteTool, MDXSearchTool, SerperDevTool
import os
from openai import OpenAI

def get_interview_questions(resume, job_offer_url):
    try:
        # Set up Environment Keys
        serper_api_key = "93c9ce7bebb072181030261fe771a5b08c1675ea"  
        os.environ["SERPER_API_KEY"] = serper_api_key
        os.environ["OPENAI_API_KEY"] = openai.api_key

        # Write resume to file
        with open('my_resume.md', 'w') as f:
            f.write(resume)

        # Define tools
        search_tool = SerperDevTool()
        scrape_tool = ScrapeWebsiteTool()
        read_resume = FileReadTool(file_path='./my_resume.md')
        semantic_search_resume = MDXSearchTool(mdx='./my_resume.md')

        # Define agents
        researcher = Agent(
            role="Tech Job Researcher",
            goal="Make sure to do amazing analysis on job posting to help job applicants",
            tools=[scrape_tool, search_tool],
            verbose=True,
            backstory=(
                "As a Job Researcher, your prowess in navigating and extracting "
                "critical information from job postings is unmatched."
            )
        )
        profiler = Agent(
            role="Personal Profiler for Engineers",
            goal="Do incredible research on job applicants to help them stand out in the job market",
            tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
            verbose=True,
            backstory=(
                "Equipped with analytical prowess, you dissect and synthesize information "
                "from diverse sources to craft comprehensive personal profiles."
            )
        )
        interview_preparer = Agent(
            role="Engineering Interview Preparer",
            goal="Create interview questions and talking points based on the resume and job requirements",
            tools=[scrape_tool, search_tool, read_resume, semantic_search_resume],
            verbose=True,
            backstory=(
                "Your role is crucial in anticipating interview dynamics."
            )
        )

        # Define tasks
        research_task = Task(
            description="Analyze the job posting URL provided to extract key skills and qualifications required.",
            expected_output="A structured list of job requirements.",
            agent=researcher,
            async_execution=True
        )
        profile_task = Task(
            description="Compile a detailed personal and professional profile using the resume.",
            expected_output="A comprehensive profile document.",
            agent=profiler,
            async_execution=True,
        )
        interview_preparation_task = Task(
            description="Create a set of interview questions and talking points based on the resume and job requirements.",
            expected_output="A document containing key questions and talking points.",
            output_file="interview_materials.md",
            context=[research_task, profile_task],
            agent=interview_preparer
        )

        # Create job application crew
        job_application_crew = Crew(
            agents=[researcher, profiler, interview_preparer],
            tasks=[research_task, profile_task, interview_preparation_task],
            verbose=True
        )

        # Kick off tasks
        job_application_inputs = {'job_posting_url': job_offer_url}
        result = job_application_crew.kickoff(inputs=job_application_inputs)
        return result

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def generate_prompt(interview_data):
    return f"""
    You are an inquisitive and engaged recruiter conducting an interview. 
    Here is the interview data: {interview_data}
    Start the conversation by greeting the candidate and asking the first question.
    """

def chat_with_gpt(messages):
    response = client.chat.completions.create(model="gpt-4",
                                              messages=messages,
                                              max_tokens=150,
                                              temperature=0.7)
    return response.choices[0].message.content.strip()

# Streamlit Interface
st.title("Virtual Job Interview Assistant")

# Input for OpenAI API Key
api_key = st.text_input("Paste OpenAI API Key:", type="default")

if api_key:
    openai.api_key = api_key
    client = OpenAI(api_key=api_key)

    st.subheader("1. Paste your resume in the box below")
    resume = st.text_area("Resume:", height=150)

    st.subheader("2. Paste URL to job offer in the box below")
    job_offer_url = st.text_input("Job Offer URL:")

    st.subheader("3. Press start")
    if st.button("Start Conversation"):
        if resume and job_offer_url:
            with st.spinner('Generating interview questions and starting interview simulation, it can take up to two minutes. If you see this error, press start once again "An error occured: The model produced invalid content.'):
                interview_data = get_interview_questions(resume, job_offer_url)

                if interview_data:
                    st.session_state.messages = [
                        {"role": "system", "content": generate_prompt(interview_data)},
                        {"role": "assistant", "content": "Hello! Thank you for joining the interview today."}
                    ]
                    st.session_state.recruiter_text = "Hello! Thank you for joining the interview today."
                    st.text_area("Interviewer:", value=st.session_state.recruiter_text, height=200, key="interviewer")

    if 'recruiter_text' in st.session_state:
        user_response = st.text_area("Your Response:", height=100)
        if st.button("Send"):
            st.session_state.messages.append({"role": "user", "content": user_response})
            recruiter_response = chat_with_gpt(st.session_state.messages)
            st.session_state.messages.append({"role": "assistant", "content": recruiter_response})
            st.session_state.recruiter_text = recruiter_response
            st.text_area("Interviewer:", value=st.session_state.recruiter_text, height=200, key="interviewer")
else:
    st.warning("Please enter your OpenAI API Key to continue.")
