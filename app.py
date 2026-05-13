import streamlit as st
import pdfplumber
from docx import Document
from sentence_transformers import SentenceTransformer, util
import pandas as pd
import plotly.express as px
import torch
import re

# 1. Configuration & Model Loading (Optimized for RTX 4070)
st.set_page_config(page_title="Smart Resume Analyzer", layout="wide")

@st.cache_resource
def load_model():
    # Automatically uses CUDA if your RTX 4070 drivers are set up
    device = "cpu"
    return SentenceTransformer("all-MiniLM-L6-v2", device=device)

model = load_model()

SKILLS = [
    # Programming Languages
    "python", "java", "c", "c++", "c#", "javascript", "typescript", "php",
    "sql", "html", "css", "r",

    # Web Development
    "react", "node", "express", "flask", "django", "spring boot",
    "rest api", "api", "bootstrap", "tailwind", "jquery",

    # Databases
    "mysql", "postgresql", "mongodb", "sqlite", "oracle", "firebase",
    "snowflake", "dbms", "database management",

    # Machine Learning / AI
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "keras", "pytorch", "scikit-learn", "opencv",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "data preprocessing", "classification", "regression", "clustering",
    "cnn", "resnet", "random forest", "xgboost",

    # Cybersecurity
    "cybersecurity", "network security", "malware analysis", "malware detection",
    "incident response", "digital forensics", "vulnerability assessment",
    "penetration testing", "ethical hacking", "owasp", "wireshark",
    "nmap", "burp suite", "metasploit", "linux", "kali linux",
    "firewall", "ids", "ips", "siem", "soc", "threat intelligence",
    "cryptography", "hashing", "encryption",

    # Cloud / DevOps
    "aws", "azure", "gcp", "cloud", "docker", "kubernetes",
    "jenkins", "git", "github", "ci/cd", "linux", "bash",

    # Data / BI
    "data analysis", "data visualization", "power bi", "tableau",
    "excel", "etl", "data warehousing", "hadoop", "spark",

    # Soft / Professional
    "problem solving", "communication", "teamwork", "leadership",
    "documentation", "project management"
]
ALIASES = {
         "js": "javascript",
    "ts": "typescript",
    "ml": "machine learning",
    "dl": "deep learning",
    "cv": "computer vision",
    "tf": "tensorflow",
    "sklearn": "scikit-learn",
    "react.js": "react",
    "node.js": "node",
    "mongo": "mongodb",
    "postgres": "postgresql",
    "information security": "cybersecurity",
    "infosec": "cybersecurity",
    "pentesting": "penetration testing",
    "gen ai": "generative ai",
    "genai": "generative ai"
    }
# 2. Text Extraction & Cleaning Functions
def clean_text(text):
    text = text.lower()

    for alias, full_form in ALIASES.items():
        text = text.replace(alias, full_form)

    text = re.sub(r"[^a-zA-Z0-9+#./\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
def extract_text(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        with pdfplumber.open(uploaded_file) as pdf:
            return " ".join([page.extract_text() for page in pdf.pages if page.extract_text()])
    elif uploaded_file.name.endswith(".docx"):
        doc = Document(uploaded_file)
        return " ".join([para.text for para in doc.paragraphs])
    else:
        return uploaded_file.read().decode("utf-8", errors="ignore")

def find_skills(resume_text, job_text):
    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)
    matched, missing = [], []

    for skill in SKILLS:
        # Check if the skill is actually in the Job Description as a standalone word
        if re.search(rf"\b{re.escape(skill)}\b", job_text):
            # Check if it's also in the Resume
            if re.search(rf"\b{re.escape(skill)}\b", resume_text):
                matched.append(skill)
            else:
                missing.append(skill)
    return matched, missing

# 3. Main Streamlit UI
st.title("🚀 Smart Resume Analyzer")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Upload Document")
    resume_file = st.file_uploader("Upload Resume", type=["pdf", "docx", "txt"])

with col2:
    st.subheader("Target Job")
    job_description = st.text_area("Paste Job Description", height=200)

if st.button("Run Deep Analysis"):
    if resume_file and job_description:
        with st.spinner("Analyzing semantics using GPU..."):
            # Process text
            resume_raw = extract_text(resume_file)
            resume_cleaned = clean_text(resume_raw)
            jd_cleaned = clean_text(job_description)

            # Semantic Similarity Calculation
            embeddings = model.encode([resume_cleaned, jd_cleaned], convert_to_tensor=True)
            score = util.cos_sim(embeddings[0], embeddings[1])
            final_score = round(float(score) * 100, 2)

            # Skill matching
            matched, missing = find_skills(resume_raw, job_description)

            # Display Results
            st.markdown("---")
            res_col1, res_col2 = st.columns([1, 2])

            with res_col1:
                st.metric("Semantic Match Score", f"{final_score}%")
                
                # Visual Chart
                df = pd.DataFrame({
                    "Status": ["Matched"] * len(matched) + ["Missing"] * len(missing),
                    "Count": [1] * (len(matched) + len(missing))
                })
                if not df.empty:
                    fig = px.pie(df, names='Status', hole=0.4, 
                                 color='Status', color_discrete_map={'Matched':'#2ecc71', 'Missing':'#e74c3c'})
                    st.plotly_chart(fig, use_container_width=True)

            with res_col2:
                st.write("### Skill Breakdown")
                st.write("**Matched:**")
                st.success(", ".join(matched) if matched else "None identified.")
                st.write("**Missing (Recommended to add):**")
                st.error(", ".join(missing) if missing else "None identified.")

                st.write("### Strategic Advice")
                if final_score > 75:
                    st.balloons()
                    st.info("Excellent match! The AI understands your experience aligns well with the JD.")
                elif final_score > 50:
                    st.warning("Good match, but consider incorporating the missing keywords highlighted above.")
                else:
                    st.error("Low semantic match. You may need to rephrase your experience to better reflect the job requirements.")
    else:
        st.error("Please provide both a resume and a job description.")