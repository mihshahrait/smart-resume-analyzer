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
