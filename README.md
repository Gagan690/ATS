# ATS Resume Analyzer

## Overview

The ATS Resume Analyzer is an AI-powered Streamlit application designed to help job seekers optimize their resumes for Applicant Tracking Systems (ATS). By leveraging Google's Gemini Pro Vision model, this tool analyzes how well a resume matches a specific job description, providing insights into strengths, weaknesses, and areas for improvement.

## Features

*   **Comprehensive Analysis**: Get detailed feedback on overall resume alignment with the job description.
*   **Missing Keywords Analysis**: Identify important keywords and technical skills from the job description that are absent from the resume.
*   **Match Percentage**: Receive a quantitative score indicating the compatibility between the resume and the job description.
*   **Improvement Suggestions**: Obtain actionable advice on content, organization, and language optimization to enhance ATS ranking.
*   **User-Friendly Interface**: An intuitive Streamlit interface for easy resume upload and job description input.

## How it Works

1.  **Upload Resume**: Users upload their resume in PDF format. The application processes the first page of the PDF.
2.  **Paste Job Description**: Users paste the relevant job description into a text area.
3.  **Choose Analysis Type**: Users select one of four analysis options: Comprehensive Analysis, Missing Keywords Analysis, Match Percentage, or Improvement Suggestions.
4.  **AI-Powered Feedback**: The application sends the resume content (as an image of the first page) and the job description to Google's Gemini Pro Vision model.
5.  **Display Results**: The AI-generated analysis is displayed, offering valuable insights and recommendations.

## Setup and Installation

To run this application locally, follow these steps:

### Prerequisites

*   Python 3.8+
*   `pip` (Python package installer)
*   A Google Cloud Project with the Gemini API enabled.
*   A Google API Key for the Gemini API.
*   Poppler installed on your system (required by `pdf2image`).

#### Installing Poppler

**Windows:**
1.  Download the latest Poppler for Windows from [here](https://github.com/oschwartz10612/poppler-windows/releases).
2.  Extract the downloaded archive (e.g., `poppler-24.02.0`).
3.  Note the path to the `bin` directory inside the extracted folder (e.g., `C:\Program Files\poppler\poppler-24.02.0\Library\bin`). You will need to update the `POPPLER_PATH_MANUAL` variable in `app.py` with this path.

**macOS (using Homebrew):**
```bash
brew install poppler
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt-get update
sudo apt-get install poppler-utils
```

### Steps

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/ATS-Resume-Analyzer.git # Replace with your actual repository URL
    cd ATS-Resume-Analyzer
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv .venv
    ```

3.  **Activate the virtual environment:**

    *   **Windows:**
        ```bash
        .venv\Scripts\activate
        ```
    *   **macOS/Linux:**
        ```bash
        source .venv/bin/activate
        ```

4.  **Install the required Python packages:**

    ```bash
    pip install -r requirements.txt
    ```
    *(Note: The `requirements.txt` file should contain `streamlit`, `python-dotenv`, `google-generativeai`, `pdf2image`.)*

5.  **Set up your Google API Key:**

    *   Create a `.env` file in the root directory of the project.
    *   Add your Google API key to this file:
        ```
        GOOGLE_API_KEY="YOUR_API_KEY_HERE"
        ```
    *   Replace `"YOUR_API_KEY_HERE"` with your actual Google API key.

6.  **Configure Poppler Path (Windows only, if not in system PATH):**

    *   Open `app.py`.
    *   Locate the line:
        ```python
        POPPLER_PATH_MANUAL = r"C:\Program Files\poppler\poppler-24.02.0\Library\bin"
        ```
    *   Update the path to match the `bin` directory of your Poppler installation.

7.  **Run the Streamlit application:**

    ```bash
    streamlit run app.py
    ```

    This command will open the application in your default web browser.

## Usage

1.  **Job Description Input**: Paste the complete job description into the "Job Description" text area.
2.  **Resume Upload**: Click the "Upload your resume (PDF format only)" button and select your PDF resume file.
3.  **Select Analysis Type**: Choose one of the four analysis buttons:
    *   `📊 Comprehensive Analysis`
    *   `🔑 Missing Keywords Analysis`
    *   `📈 Match Percentage`
    *   `✨ Improvement Suggestions`
4.  **View Results**: The analysis results will appear in the "Analysis Results" section. For "Match Percentage," a visual metric will also be displayed.
5.  **Export Results**: Use the "📥 Export Results" button to download the AI-generated feedback as a text file.

## Important Notes

*   **PDF Processing**: The tool currently analyzes only the **first page** of your PDF resume. Ensure critical information is on the first page for optimal analysis.
*   **Poppler Dependency**: `pdf2image` relies on Poppler. If you encounter errors related to PDF processing, verify that Poppler is correctly installed and its path is configured if necessary.
*   **AI Accuracy**: The analysis is an AI-driven estimation. Actual ATS systems vary. Use the insights as a guide to improve your resume, but always tailor it carefully for each specific job application.
*   **Data Privacy**: Your resume and job description are sent to Google's Generative AI API for analysis during your session. This application **does not store your resume or job description data** on its server after your session ends. Refer to Google's API data usage policies for more information.

## Contributing

Feel free to fork the repository, open issues, or submit pull requests to improve the application.

## License

© 2025 ATS Resume Analyzer | All Rights Reserved