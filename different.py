import streamlit as st
import PyPDF2
from groq import Groq
import io

# Initialize Groq client with API key from secrets
client = Groq(api_key="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")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() or ""
    return text

# Function to get LLM response from Groq
def get_llm_response(prompt, model="mixtral-8x7b-32768"):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1000,
        temperature=0.7,
    )
    return response.choices[0].message.content

# Main Streamlit app
def main():
    st.title("Resume Analyzer")
    st.write("Upload your resume (PDF) and optionally a job description to get expert feedback and a suitability score.")

    # Tabs for different functionalities
    tab1, tab2 = st.tabs(["Resume Analysis", "Resume Score"])

    # --- Tab 1: Resume Analysis ---
    with tab1:
        st.header("Resume Analysis")
        resume_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"], key="resume")

        if resume_file:
            resume_text = extract_text_from_pdf(resume_file)
            st.write("### Extracted Resume Text")
            st.text_area("Resume Content", resume_text, height=200)

            if st.button("Analyze Resume"):
                with st.spinner("Analyzing your resume..."):
                    # Prompt for resume analysis
                    analysis_prompt = f"""
                    You are an expert resume reviewer. Analyze the following resume and provide detailed feedback:
                    - Strengths of the resume
                    - Areas of improvement
                    - Suggestions for formatting optimization
                    Here is the resume text:
                    {resume_text}
                    """
                    feedback = get_llm_response(analysis_prompt)
                    st.write("### Expert Feedback")
                    st.markdown(feedback)

    # --- Tab 2: Resume Score ---
    with tab2:
        st.header("Resume Score")
        resume_file_score = st.file_uploader("Upload your resume (PDF) again", type=["pdf"], key="resume_score")
        job_description = st.text_area("Paste the Job Description here", height=200)

        if resume_file_score and job_description:
            resume_text_score = extract_text_from_pdf(resume_file_score)
            if st.button("Calculate Resume Score"):
                with st.spinner("Calculating resume score..."):
                    # Prompt for resume score
                    score_prompt = f"""
                    You are an expert in hiring and resume evaluation. Compare the following resume with the job description provided:
                    - Resume: {resume_text_score}
                    - Job Description: {job_description}
                    Provide:
                    - A percentage score (0-100) indicating how well the resume matches the job description
                    - A brief explanation of the score
                    """
                    score_response = get_llm_response(score_prompt)
                    st.write("### Resume Score")
                    st.markdown(score_response)

if __name__ == "__main__":
    main()
