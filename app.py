import streamlit as st
import plotly.express as px
from PyPDF2 import PdfReader
from reports.report_generator import generate_pdf_report

st.set_page_config(page_title="ResumeIQ Pro", layout="wide")

# ---------- SESSION STATE ----------
defaults = {
    "analysis_done": False,
    "latest_result": {},
    "theme": "Dark",
    "default_role": "Backend Developer",
    "notifications": True,
    "resume_text": "",
    "resume_name": ""
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# ---------- DYNAMIC STYLE ----------
if st.session_state.theme == "Dark":
    bg_color = "#0d1117"
    text_color = "white"
    card_bg = "#161b22"
    input_bg = "#1f2430"
    chart_theme = "plotly_dark"
else:
    bg_color = "#f8fafc"
    text_color = "#111827"
    card_bg = "#ffffff"
    input_bg = "#ffffff"
    chart_theme = "plotly_white"

st.markdown(f"""
<style>
.stApp {{
    background-color: {bg_color};
    color: {text_color};
}}

.main {{
    background-color: {bg_color};
}}

section[data-testid="stSidebar"] {{
    background-color: {card_bg};
}}

h1, h2, h3, h4, h5, h6, p, label, span, div {{
    color: {text_color} !important;
}}

div[data-baseweb="select"] > div {{
    background-color: {input_bg} !important;
    color: {text_color} !important;
    border-radius: 12px;
}}

input, textarea {{
    background-color: {input_bg} !important;
    color: {text_color} !important;
}}

.stButton > button {{
    background-color: {card_bg};
    color: {text_color};
    border-radius: 12px;
    border: 1px solid #444;
}}

[data-testid="stMetric"] {{
    background: {card_bg};
    padding: 15px;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.15);
}}

.stSuccess, .stWarning, .stInfo {{
    border-radius: 14px;
}}
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR ----------
st.sidebar.title("🚀 ResumeIQ Pro")
menu = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Resume Analysis", "Reports", "Settings"]
)

# ---------- DATA ----------
job_roles = {
    "Backend Developer": ["Python", "SQL", "API", "Database", "Git"],
    "Data Analyst": ["Python", "SQL", "Excel", "Statistics", "Visualization"],
    "AI Engineer": ["Python", "Machine Learning", "Deep Learning", "NLP", "Data Science"]
}

# ---------- FUNCTIONS ----------
def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted
    return text


def generate_smart_recommendations(missing_skills):
    smart_map = {
        "Machine Learning": "Master ML fundamentals in 4 weeks.",
        "Deep Learning": "Build one Deep Learning project.",
        "NLP": "Create an NLP portfolio project.",
        "Data Science": "Improve statistics & storytelling.",
        "SQL": "Practice advanced SQL queries.",
        "Git": "Learn collaborative Git workflows."
    }

    return [smart_map.get(skill, f"Improve expertise in {skill}.") for skill in missing_skills]


# ---------- DASHBOARD ----------
if menu == "Dashboard":
    st.title("ResumeIQ Pro")
    st.subheader("Executive Dashboard")

    if st.session_state.analysis_done:
        result = st.session_state.latest_result

        col1, col2, col3 = st.columns(3)
        col1.metric("ATS Score", f"{result['score']}/100")
        col2.metric("Hiring Probability", result["probability"])
        col3.metric("Readiness", result["readiness"])

        st.success(f"Loaded: {st.session_state.resume_name}")
    else:
        st.info("No analysis yet. Please upload a resume in Resume Analysis.")


# ---------- RESUME ANALYSIS ----------
elif menu == "Resume Analysis":
    st.title("Resume Analysis")

    if st.session_state.analysis_done:
        st.success(f"Previous analysis loaded for: {st.session_state.resume_name}")

    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])

    if uploaded_file:
        st.session_state.resume_text = extract_text_from_pdf(uploaded_file)
        st.session_state.resume_name = uploaded_file.name

    if st.session_state.resume_text:
        resume_text = st.session_state.resume_text

        selected_role = st.selectbox(
            "Choose Target Role",
            list(job_roles.keys()),
            index=list(job_roles.keys()).index(st.session_state.default_role)
        )

        required_skills = job_roles[selected_role]
        found_skills = [s for s in required_skills if s.lower() in resume_text.lower()]
        missing_skills = [s for s in required_skills if s not in found_skills]

        score = int((len(found_skills) / len(required_skills)) * 100)

        if score >= 80:
            readiness = "Strong Candidate"
            probability = "78%"
        elif score >= 60:
            readiness = "Moderate Candidate"
            probability = "55%"
        else:
            readiness = "Needs Improvement"
            probability = "32%"

        recommendations = generate_smart_recommendations(missing_skills)

        st.session_state.analysis_done = True
        st.session_state.latest_result = {
            "score": score,
            "readiness": readiness,
            "probability": probability,
            "found_skills": found_skills,
            "missing_skills": missing_skills,
            "recommendations": recommendations
        }

        col1, col2, col3 = st.columns(3)
        col1.metric("ATS Score", f"{score}/100")
        col2.metric("Matched Skills", len(found_skills))
        col3.metric("Missing Skills", len(missing_skills))

        fig = px.pie(
            names=["Matched", "Missing"],
            values=[len(found_skills), len(missing_skills)],
            title="Skill Match Overview",
            template=chart_theme
        )
        st.plotly_chart(fig, use_container_width=True)

        left, right = st.columns(2)

        with left:
            st.markdown("## Skills Found")
            for skill in found_skills:
                st.success(skill)

        with right:
            st.markdown("## Missing Skills")
            for skill in missing_skills:
                st.error(skill)


# ---------- REPORTS ----------
elif menu == "Reports":
    st.title("Reports Center")

    if st.session_state.analysis_done:
        result = st.session_state.latest_result

        st.write("Generate professional report from latest analysis.")

        if st.button("Generate PDF Report"):
            pdf_path = generate_pdf_report(
                "resume_analysis",
                result["score"],
                result["found_skills"],
                result["missing_skills"],
                result["recommendations"]
            )

            with open(pdf_path, "rb") as pdf_file:
                st.download_button(
                    label="Download PDF",
                    data=pdf_file,
                    file_name="ResumeIQ_Pro_Report.pdf",
                    mime="application/pdf"
                )
    else:
        st.warning("No analysis data available.")


# ---------- SETTINGS ----------
elif menu == "Settings":
    st.title("Settings")

    theme = st.selectbox(
        "Theme",
        ["Dark", "Light"],
        index=0 if st.session_state.theme == "Dark" else 1
    )

    default_role = st.selectbox(
        "Default Role",
        list(job_roles.keys()),
        index=list(job_roles.keys()).index(st.session_state.default_role)
    )

    notifications = st.checkbox(
        "Enable Notifications",
        value=st.session_state.notifications
    )

    if st.button("Save Settings"):
        st.session_state.theme = theme
        st.session_state.default_role = default_role
        st.session_state.notifications = notifications
        st.rerun()
