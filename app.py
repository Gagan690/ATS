import base64
import io
import os
import re # Moved import re to the top
import time

import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai
import pdf2image 

load_dotenv()

POPPLER_PATH_MANUAL = r"C:\Program Files\poppler\poppler-24.02.0\Library\bin"


try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
except Exception as e:
    st.error(f"Failed to configure GenerativeAI API: {e}. Ensure GOOGLE_API_KEY is set.")
    # You might want to st.stop() here if the API is critical

# --- Page Configuration and Styling ---
APP_TITLE = "ATS Resume Analyzer"
APP_ICON = "📄"

st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
    <style>
    .main {
        padding: 2rem;
        background-color: #f8f9fa;
    }
    .stButton button {
        width: 100%;
        border-radius: 10px;
        height: 3rem;
        font-weight: 600;
        margin-top: 10px;
    }
    /* Example: .css-1d391kg refers to a Streamlit-generated class. */
    /* This might need adjustment if Streamlit updates its internal class names. */
    .css-1d391kg { /* This class might be specific to a Streamlit version */
        padding-top: 3rem;
    }
    .stTextArea textarea {
        border-radius: 10px;
    }
    .upload-section {
        border: 2px dashed #9CA3AF;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin: 1rem 0;
    }
    .result-section {
        background-color: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 1.5rem;
    }
    .stProgress > div > div {
        background-color: #6366F1; /* Custom progress bar color */
    }
    h1, h2, h3 {
        color: #1E40AF; /* Custom header colors */
    }
    </style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

COMPREHENSIVE_PROMPT = """
You are an experienced Technical Human Resource Manager with expertise in resume screening.
Please analyze the provided resume against the job description and provide a comprehensive evaluation.

Structure your response as follows:
1. Summary of the candidate's profile (2-3 sentences)
2. Key strengths that align with the job description (bullet points)
3. Notable gaps or weaknesses compared to requirements (bullet points)
4. Overall alignment assessment
5. Recommendations for the hiring manager

Use professional HR terminology and be objective in your assessment.
"""

MISSING_KEYWORDS_PROMPT = """
You are an ATS expert specializing in keyword optimization.
Analyze the resume against the job description and identify:

1. Important keywords from the job description that are missing in the resume
2. Technical skills mentioned in the job that aren't reflected in the resume
3. Recommended phrases to add to improve ATS ranking

Format your response as a structured list of missing keywords by category (technical skills, soft skills, experience, etc.)
"""

MATCH_PROMPT = """
You are an advanced ATS (Applicant Tracking System) with deep understanding of hiring algorithms.
Evaluate the resume against the job description and provide:

1. An overall match percentage (from 0-100%)
2. Category-specific scores for: Skills Match, Experience Match, Education Match
3. The most critical missing keywords
4. A brief explanation of the score

Start with the percentage match prominently displayed. Example: "Overall Match: 85%"
"""

IMPROVEMENT_PROMPT = """
You are a resume optimization consultant with expertise in ATS systems.
Analyze the resume against the job description and provide actionable suggestions on:

1. Specific content improvements (what to add, remove, or emphasize)
2. Section organization recommendations
3. How to better align achievements with job requirements
4. Language optimization for ATS scanning

Focus on practical, specific advice the candidate can implement immediately.
"""

def get_gemini_response(input_prompt: str, pdf_content_parts: list, job_description_text: str) -> str:
    """
    Generates content from the Gemini Pro Vision model based on the input prompt,
    PDF image parts, and job description.
    """
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content([input_prompt, pdf_content_parts[0], job_description_text])
        return response.text
    except Exception as e:
        st.error(f"Error generating response from AI: {e}")
        return "Error: Could not get response from AI. Please check API key and network."

def input_pdf_setup(uploaded_file_object):
    """
    Converts the first page of an uploaded PDF file to image parts suitable for Gemini Pro Vision.
    """
    if uploaded_file_object is not None:
        with st.spinner('Processing PDF (first page)...'):
            try:
                # Convert PDF to a list of images (PIL Image objects)
                # Pass the poppler_path argument HERE
                images = pdf2image.convert_from_bytes(
                    uploaded_file_object.read(),
                    poppler_path=POPPLER_PATH_MANUAL # <--- ADD THIS
                )

                if not images:
                    st.error("Could not extract any images from the PDF.")
                    return None

                first_page_image = images[0]

                img_byte_array = io.BytesIO()
                first_page_image.save(img_byte_array, format='PNG')
                img_byte_array_value = img_byte_array.getvalue()

                pdf_parts = [
                    {
                        "mime_type": "image/png",
                        "data": base64.b64encode(img_byte_array_value).decode()
                    }
                ]
                return pdf_parts
            except pdf2image.exceptions.PDFPopplerTimeoutError:
                st.error("PDF processing timed out. The PDF might be too complex or large.")
                return None
            except pdf2image.exceptions.PDFInfoNotInstalledError: # More specific error
                st.error("Poppler not found by pdf2image. Please ensure Poppler is installed and check the POPPLER_PATH_MANUAL variable in the script if you're using it.")
                st.error(f"Attempted Poppler path if manual: {POPPLER_PATH_MANUAL}")
                return None
            except Exception as e:
                st.error(f"Error processing PDF: {e}. Ensure it's a valid PDF and Poppler might be the issue.")
                return None
    else:
        raise FileNotFoundError("No file uploaded. Please upload a PDF resume.")


with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/resume.png", width=80)
    st.title(APP_TITLE)
    st.markdown("---")
    
    st.subheader("How it Works")
    st.write("""
    1. Upload your resume (PDF format).
    2. Paste the job description.
    3. Choose an analysis option.
    4. Get AI-powered feedback!
    """)
    
    st.markdown("---")
    st.subheader("Tips for ATS Optimization")
    st.write("""
    - Use relevant keywords from the job description.
    - Employ standard section headings (e.g., "Experience", "Education", "Skills").
    - Keep formatting simple; avoid tables, columns, and complex graphics in resumes.
    - Quantify achievements with numbers and data.
    - Customize your resume for each job application.
    """)
    
    st.markdown("---")
    st.caption("© 2025 ATS Resume Analyzer | All Rights Reserved") # Assuming 2025 is intentional

st.title(APP_TITLE)
st.write("Get AI-powered insights on how well your resume matches a job description.")

analysis_tab, about_tab = st.tabs(["Analysis", "About"])

with analysis_tab:
    col_jd, col_resume = st.columns([1, 1]) # Ratio for columns
    
    with col_jd:
        st.subheader("Job Description")
        job_description = st.text_area(
            "Paste the job description here:",
            height=300,
            key="job_desc_input", # Unique key for widget
            placeholder="Copy and paste the complete job description here..."
        )
    
    with col_resume:
        st.subheader("Resume Upload")
        # Using markdown for a styled upload box
        st.markdown('<div class="upload-section">', unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Upload your resume (PDF format only)",
            type="pdf",
            key="resume_uploader", # Unique key for widget
            help="Please ensure your resume is in PDF format."
        )
        
        if uploaded_file is not None:
            st.success(f"✅ PDF Successfully Uploaded: {uploaded_file.name}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.subheader("Choose Analysis Type")
    
    # Analysis buttons in two columns
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        analyze_button = st.button("📊 Comprehensive Analysis", use_container_width=True, key="analyze_btn")
        keywords_button = st.button("🔑 Missing Keywords Analysis", use_container_width=True, key="keywords_btn")
    
    with col_btn2:
        match_button = st.button("📈 Match Percentage", use_container_width=True, key="match_btn")
        improve_button = st.button("✨ Improvement Suggestions", use_container_width=True, key="improve_btn")

    # --- Response Area ---
    # Check if essential inputs are provided before processing
    if not job_description or not uploaded_file:
        if analyze_button or keywords_button or match_button or improve_button:
            st.warning("⚠️ Please upload your resume AND enter a job description to proceed.")
    else:
        # Determine which analysis to perform
        selected_prompt = None
        analysis_title = ""

        if analyze_button:
            selected_prompt = COMPREHENSIVE_PROMPT
            analysis_title = "🔍 Comprehensive Analysis"
        elif keywords_button:
            selected_prompt = MISSING_KEYWORDS_PROMPT
            analysis_title = "🔑 Missing Keywords Analysis"
        elif match_button:
            selected_prompt = MATCH_PROMPT
            analysis_title = "📈 Match Percentage"
        elif improve_button:
            selected_prompt = IMPROVEMENT_PROMPT
            analysis_title = "✨ Improvement Suggestions"

        if selected_prompt:
            st.markdown("---")
            st.subheader("Analysis Results")
            
            # Placeholder for results and progress bar
            result_placeholder = st.empty()
            
            with result_placeholder.container():
                # Cosmetic progress bar for user experience
                progress_bar = st.progress(0)
                progress_text_area = st.empty()
                
                progress_stages = {
                    0: "Initializing analysis...",
                    25: "Extracting resume content...",
                    50: "Analyzing against job description...",
                    75: "Generating insights with AI...",
                    100: "Finalizing results..."
                }

                for percent_complete in range(101):
                    if percent_complete in progress_stages:
                        progress_text_area.text(progress_stages[percent_complete])
                    progress_bar.progress(percent_complete)
                    time.sleep(0.01) # Small delay for animation
                
                progress_text_area.text("Processing complete!")

            # Process the PDF and get AI response
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                
                if pdf_content: # Ensure PDF processing was successful
                    response_text = get_gemini_response(selected_prompt, pdf_content, job_description)
                    
                    # Display the results in a styled section
                    with result_placeholder.container(): # Replace progress with results
                        st.markdown('<div class="result-section">', unsafe_allow_html=True)
                        st.subheader(analysis_title)
                        
                        # Special handling for Match Percentage to show metric
                        if match_button:
                            try:
                                # Attempt to extract percentage for visual display
                                match_search = re.search(r'(\d{1,3})%', response_text)
                                if match_search:
                                    percentage = int(match_search.group(1))
                                    
                                    # Layout for metric and summary message
                                    metric_col, msg_col = st.columns([1, 3])
                                    with metric_col:
                                        st.metric(label="Match Score", value=f"{percentage}%")
                                    with msg_col:
                                        if percentage >= 80:
                                            st.success("Strong match! Your resume is well-aligned.")
                                        elif percentage >= 60:
                                            st.info("Good match. There's room for improvement.")
                                        else:
                                            st.warning("Significant gaps found. Review suggestions carefully.")
                                else:
                                    st.info("Could not extract a specific percentage score from the analysis.")
                            except Exception as e_regex:
                                st.error(f"Error parsing match percentage: {e_regex}")
                                # Fallback to showing the full response if regex fails
                        
                        st.markdown(response_text) # Display the full AI response
                        
                        # Add export option for the results
                        st.download_button(
                            label="📥 Export Results",
                            data=response_text,
                            file_name=f"{analysis_title.replace(' ', '_').lower()}_results.txt",
                            mime="text/plain"
                        )
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    # Error messages would have been shown by input_pdf_setup
                    result_placeholder.error("Could not process the PDF. Please try another file or check its format.")

            except FileNotFoundError as fnf_error:
                result_placeholder.error(str(fnf_error))
            except Exception as e:
                result_placeholder.error(f"An unexpected error occurred: {str(e)}")
                st.info("Please ensure your PDF is valid and the job description is provided.")

with about_tab:
    st.subheader(f"About {APP_TITLE}")
    st.write(f"""
    The {APP_TITLE} is an AI-powered tool designed to help job seekers optimize their resumes 
    for Applicant Tracking Systems (ATS) by leveraging Google's Gemini Pro Vision model.
    
    Our tool uses advanced AI to analyze how well your resume (as an image of its first page) 
    matches specific job descriptions, identifying strengths and areas for improvement.
    
    ### Key Features:
    - **Comprehensive Analysis**: Get detailed feedback on resume alignment.
    - **Keyword Matching**: Identify missing keywords to improve ATS score.
    - **Match Percentage**: See a quantitative assessment of compatibility.
    - **Improvement Suggestions**: Receive actionable advice to enhance your resume.
    
    ### How ATS Systems Work (Generally):
    Applicant Tracking Systems often parse text from resumes to scan for relevant keywords, 
    experience, and qualifications. Our tool simulates a part of this by visually analyzing 
    the resume's first page against the job description.
    Up to 75% of resumes can be rejected by ATS before reaching human reviewers. 
    Optimizing your resume is key!
    """)
    
    st.subheader("Frequently Asked Questions")
    
    with st.expander("What is an ATS?"):
        st.write("""
        An Applicant Tracking System (ATS) is software used by employers to collect, scan, 
        sort, and rank job applications. These systems often use algorithms to search for 
        keywords and phrases from the job description, helping employers filter through 
        large volumes of applications.
        """)
    
    with st.expander("How accurate is this analysis?"):
        st.write("""
        This tool provides an AI-driven estimation based on the visual content of your resume's 
        first page and the provided job description. Actual ATS systems vary widely in their 
        algorithms and how they process resumes (some parse text, some OCR, etc.). 
        Use this tool as a guide and for insights, but always tailor your resume carefully 
        for each specific job application.
        """)
    
    with st.expander("What format should my resume be in for this tool?"):
        st.write("""
        - **PDF format is required for upload.**
        - The tool currently analyzes the **first page** of the PDF.
        - For best results with actual ATS systems (and this tool):
            - Avoid complex formatting, tables, and multiple columns if possible, as these can sometimes confuse parsing systems.
            - Use standard, readable fonts.
            - Use standard section headings (e.g., "Professional Experience", "Education", "Skills").
            - Generally, avoid putting crucial information in headers/footers.
        """)
    
    with st.expander("Is my data secure?"):
        st.write("""
        We prioritize your privacy. 
        - Your resume and job description are sent to Google's Generative AI API for analysis during your session.
        - This application **does not store your resume or job description data** on its server after your session ends.
        - Please refer to Google's API data usage policies for how they handle data sent to their models.
        """)

HIDE_ST_STYLE = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;} /* Also hide header for a cleaner look */
</style>
"""
st.markdown(HIDE_ST_STYLE, unsafe_allow_html=True)


'''
    Commands to run this file:
    .venv\Scripts\activate
    pip install -r requirements.txt
    streamlit run app.py
'''