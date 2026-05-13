# Smart Resume Analyzer

## Overview

Smart Resume Analyzer is an AI-powered web application that compares a candidate's resume with a target job description and generates a semantic match score. The system extracts text from resumes, analyzes similarity using a pre-trained Sentence-BERT model, identifies matched and missing skills, and gives improvement suggestions.

This project is designed to help users understand how well their resume aligns with a specific job role.

## Features

- Upload resume in PDF, DOCX, or TXT format
- Paste any job description
- Extract resume text automatically
- Calculate semantic match score using Sentence-BERT
- Identify matched skills
- Identify missing skills
- Display skill breakdown with visual chart
- Provide improvement suggestions
- Streamlit-based interactive web interface

## Tech Stack

- Python
- Streamlit
- Sentence-Transformers
- PyTorch
- pdfplumber
- python-docx
- Pandas
- Plotly

## Model Used

This project uses the pre-trained `all-MiniLM-L6-v2` model from the Sentence-Transformers library.

The model converts the resume and job description into semantic embeddings and compares them using cosine similarity. No custom model training is required.

## Project Structure

```text
smart-resume-analyzer/
│
├── app.py
├── requirements.txt
├── README.md
└── .gitignore
```
🛠️ Installation
1. Clone the Repository
  git clone https://github.com/mihshahrait/smart-resume-analyzer.git
  cd smart-resume-analyzer
2. Set Up Environment

It is recommended to use a virtual environment to manage dependencies.

  # Windows
  python -m venv venv
  source venv/Scripts/activate

  # Linux/Mac
  python3 -m venv venv
  source venv/bin/activate

3. Install Dependencies

  pip install -r requirements.txt
🚀 How to Run
  Launch the interactive web dashboard using Streamlit:


    python -m streamlit run app.py
After running the command, open the Local URL (usually http://localhost:8501) shown in your terminal.

🧠 How It Works:-

1. The system follows a high-performance NLP pipeline to ensure accuracy:

2. Extraction: Extracts raw text from uploaded files using pdfplumber and python-docx.

3. Preprocessing: Cleans text by removing noise and normalizing formatting while preserving technical tokens (like C++ and C#).

4. Embedding: Sentence-BERT transforms both the resume and the job description into high-dimensional vectors.

5. Similarity: Calculates the Cosine Similarity between the vectors to determine the semantic match.

6. Skill Mapping: Runs a regex-based comparison against a professional skill bank to highlight specific matches and missing requirements.

📂 Supported File types:
.PDF	Portable Document Format (Standard)
.DOCX	Microsoft Word Documents
.TXT	Plain Text Files
🎯 Use Cases
Ideal for students and professionals targeting roles in:

Cybersecurity: (e.g., Analyst, Penetration Tester, SOC Engineer)

Data Science: (e.g., Machine Learning Intern, Data Analyst)

Software Development: (e.g., Full Stack, DevOps, Web Developer)

🔭 Future Scope
[ ] Section-wise Analysis: Breaking down scores by Experience, Education, and Projects.

[ ] ATS Scoring: Simulating Applicant Tracking System filters.

[ ] Role Recommendations: Suggesting specific job titles based on resume content.

[ ] Exportable Reports: Generating downloadable PDF summaries of the analysis.

⚠️ Disclaimer
This tool provides an estimated resume-job match score using NLP-based similarity and keyword matching. It is intended for guidance purposes only and should not be used as a final hiring or recruitment decision system.

👤 Author
Mihir Shah
