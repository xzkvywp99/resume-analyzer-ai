# ResumeIQ Pro 🚀

ResumeIQ Pro is an AI-powered resume analysis platform built with Python and Streamlit.  
It helps users evaluate resumes against target job roles, calculate ATS compatibility, identify missing skills, and generate professional PDF reports.

This project is designed as a portfolio-ready application that demonstrates software engineering, intelligent document analysis, and interactive dashboard development.

---

# Features

- PDF Resume Upload & Parsing
- ATS Score Calculation
- Skill Match Detection
- Missing Skills Recommendations
- Interactive Charts with Plotly
- Professional PDF Report Export
- Dark / Light Theme Support
- Session Persistence
- Modular Architecture

---

# Project Structure

ResumeIQ/
│
├── app.py
├── requirements.txt
├── README.md
│
├── reports/
│   └── report_generator.py
│
├── generated_reports/
│
└── assets/

---

# Installation Guide

## 1. Download Project

Click **Code → Download ZIP** from the GitHub repository page.

Extract the ZIP file and open the project folder.

---

## 2. Create Virtual Environment

### Windows

python -m venv venv  
venv\Scripts\activate

### Mac / Linux

python3 -m venv venv  
source venv/bin/activate

---

## 3. Install Dependencies

pip install -r requirements.txt

---

# Running the Application

streamlit run app.py

After running, open:

http://localhost:8501

---

# How to Use

## Resume Analysis

1. Open the application
2. Navigate to **Resume Analysis**
3. Upload a PDF resume
4. Select target job role
5. Review ATS score and recommendations

---

## Reports

1. Go to **Reports**
2. Click **Generate PDF Report**
3. Download the generated file

---

## Settings

Customize:

- Theme Mode
- Default Role
- Notifications

---

# Supported Roles

- Backend Developer
- Data Analyst
- AI Engineer

---

# Required Libraries

- streamlit
- plotly
- PyPDF2
- reportlab
- pandas

---

# Common Issues

## Streamlit Not Found

Install it manually:

pip install streamlit

---

## PDF Report Errors

Ensure reportlab is installed:

pip install reportlab

---

# Future Improvements

- AI Resume Rewriter
- Job Matching Engine
- Recruiter Dashboard
- Cloud Deployment

---

# License

For educational and portfolio purposes.

---

# Author

Developed as a software engineering portfolio project.