from reports.report_generator import generate_pdf_report
import streamlit as st
from PyPDF2 import PdfReader

st.set_page_config(page_title="ResumeIQ", layout="wide")

st.title("ResumeIQ")
st.subheader("AI-Powered Resume Analyzer")

uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

job_roles = {
    "Backend Developer": ["Python", "SQL", "API", "Database", "Git"],
    "Data Analyst": ["Python", "SQL", "Excel", "Statistics", "Visualization"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP", "Data Science"]
}


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text


if uploaded_file:
    resume_text = extract_text_from_pdf(uploaded_file)

    st.success("Resume analyzed successfully!")

    selected_role = st.selectbox("Choose Target Role", list(job_roles.keys()))

    required_skills = job_roles[selected_role]

    found_skills = [
        skill for skill in required_skills
        if skill.lower() in resume_text.lower()
    ]

    missing_skills = [
        skill for skill in required_skills
        if skill not in found_skills
    ]

    score = int((len(found_skills) / len(required_skills)) * 100)

    recommendations = []

    if missing_skills:
        for skill in missing_skills:
            recommendations.append(f"Learn {skill}")
    else:
        recommendations.append("Excellent profile match!")

    st.markdown("## Match Analysis")
    st.write(f"Target Role: **{selected_role}**")
    st.progress(score)
    st.write(f"Compatibility Score: {score}/100")

    st.markdown("## Skills Found")
    for skill in found_skills:
        st.write(f"✅ {skill}")

    st.markdown("## Missing Skills")
    for skill in missing_skills:
        st.write(f"❌ {skill}")

    st.markdown("## Recommendations")
    for rec in recommendations:
        st.write(f"• {rec}")

    st.markdown("---")

    if st.button("Generate PDF Report"):
        pdf_path = generate_pdf_report(
            "resume_analysis",
            score,
            found_skills,
            missing_skills,
            recommendations
        )

        with open(pdf_path, "rb") as pdf_file:
            st.download_button(
                label="Download PDF",
                data=pdf_file,
                file_name="ResumeIQ_Report.pdf",
                mime="application/pdf"
            )
