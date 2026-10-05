import os
import sys

import streamlit as st


# ============================================================
# PROJECT PATH
# ============================================================

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


# ============================================================
# IMPORTS
# ============================================================

from utils.resume_parser import extract_resume_text
from utils.resume_analyzer import analyze_resume
from utils.job_matcher import extract_job_skills, calculate_match
from utils.ats_scorer import (
    calculate_ats_score,
    get_score_message,
    get_improvement_suggestions
)
from utils.gemini_ai import get_ai_feedback


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Resume & Job Match Analyzer",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(
            135deg,
            #eef2ff 0%,
            #fdf2f8 50%,
            #ecfeff 100%
        );
    }

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 800;
        color: #4f46e5;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 17px;
        color: #64748b;
        margin-bottom: 30px;
    }

    .feature-box {
        text-align: center;
        background: white;
        padding: 20px;
        border-radius: 18px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.06);
        min-height: 150px;
    }

    .feature-icon {
        font-size: 32px;
    }

    .feature-title {
        font-weight: 700;
        color: #312e81;
        margin-top: 8px;
    }

    .match-box {
        background: #ecfdf5;
        padding: 12px;
        border-radius: 12px;
        border-left: 5px solid #10b981;
        margin-bottom: 8px;
        color: #065f46;
        font-weight: 600;
    }

    .missing-box {
        background: #fff1f2;
        padding: 12px;
        border-radius: 12px;
        border-left: 5px solid #f43f5e;
        margin-bottom: 8px;
        color: #9f1239;
        font-weight: 600;
    }

    .info-box {
        background: white;
        padding: 16px;
        border-radius: 14px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }

    [data-testid="stFileUploader"] {
        background: white;
        border-radius: 16px;
        padding: 10px;
        border: 2px dashed #a5b4fc;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">📄 AI Resume & Job Match Analyzer</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume • Match your dream job • Improve your ATS score 🚀'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.title("🎯 Resume Assistant")

    st.write(
        "Your AI-powered resume analysis tool."
    )

    st.markdown("---")

    st.subheader("✨ Features")

    st.write("📄 Resume Analysis")
    st.write("🎯 Job Matching")
    st.write("📊 ATS Score")
    st.write("✅ Matching Skills")
    st.write("❌ Missing Skills")
    st.write("🧠 Gemini AI")
    st.write("💡 Improvement Suggestions")

    st.markdown("---")

    st.caption(
        "Built with Python + Streamlit + Gemini AI"
    )


# ============================================================
# RESUME UPLOAD
# ============================================================

st.header("📤 Upload Your Resume")

uploaded_file = st.file_uploader(
    "Choose your resume",
    type=["pdf", "docx", "txt"],
    help="Supported formats: PDF, DOCX and TXT"
)


# ============================================================
# JOB DESCRIPTION
# ============================================================

st.header("📝 Job Description")

job_description = st.text_area(
    "Paste the job description here",
    height=220,
    placeholder=(
        "Example:\n\n"
        "We are looking for a Data Science Intern with knowledge "
        "of Python, SQL, Machine Learning, Pandas and NumPy..."
    )
)


# ============================================================
# WELCOME SCREEN
# ============================================================

if not uploaded_file:

    st.info(
        "👋 Welcome! Upload your resume above to get started."
    )

    st.subheader("🚀 What this application can do")

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(
            '<div class="feature-box">'
            '<div class="feature-icon">📄</div>'
            '<div class="feature-title">Resume Analysis</div>'
            '<p>Extract important resume details.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:

        st.markdown(
            '<div class="feature-box">'
            '<div class="feature-icon">🎯</div>'
            '<div class="feature-title">Job Matching</div>'
            '<p>Compare your skills with job requirements.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with col3:

        st.markdown(
            '<div class="feature-box">'
            '<div class="feature-icon">📊</div>'
            '<div class="feature-title">ATS Score</div>'
            '<p>Check your resume strength.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    with col4:

        st.markdown(
            '<div class="feature-box">'
            '<div class="feature-icon">🧠</div>'
            '<div class="feature-title">Gemini AI</div>'
            '<p>Get personalized AI feedback.</p>'
            '</div>',
            unsafe_allow_html=True
        )

    st.stop()


# ============================================================
# EXTRACT RESUME TEXT
# ============================================================

try:

    resume_text = extract_resume_text(
        uploaded_file
    )

except Exception as e:

    st.error(
        f"❌ Resume extraction failed: "
        f"{type(e).__name__}: {e}"
    )

    st.stop()


if not resume_text:

    st.error(
        "❌ Could not extract text from the uploaded resume."
    )

    st.stop()


# ============================================================
# ANALYZE RESUME
# ============================================================

try:

    resume_data = analyze_resume(
        resume_text
    )

except Exception as e:

    st.error(
        f"❌ Resume analysis failed: "
        f"{type(e).__name__}: {e}"
    )

    st.stop()


# ============================================================
# RESUME INFORMATION
# ============================================================

st.markdown("---")

st.header("👤 Resume Analysis")


col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "👤 Name",
        resume_data["name"]
    )


with col2:

    st.metric(
        "📧 Email",
        resume_data["email"]
    )


with col3:

    st.metric(
        "📱 Phone",
        resume_data["phone"]
    )


# ============================================================
# SKILLS
# ============================================================

st.subheader("🛠️ Detected Skills")


if resume_data["skills"]:

    skill_columns = st.columns(4)

    for index, skill in enumerate(
        resume_data["skills"]
    ):

        with skill_columns[index % 4]:

            st.success(
                f"✓ {skill}"
            )

else:

    st.warning(
        "No predefined technical skills detected."
    )


# ============================================================
# EDUCATION
# ============================================================

st.subheader("🎓 Education")


if resume_data["education"]:

    st.write(
        " • ".join(
            resume_data["education"]
        )
    )

else:

    st.info(
        "No education keywords detected."
    )


# ============================================================
# JOB DESCRIPTION CHECK
# ============================================================

if not job_description.strip():

    st.warning(
        "📝 Please paste a job description above "
        "to calculate Job Match and ATS Score."
    )

    st.stop()


# ============================================================
# EXTRACT JOB SKILLS
# ============================================================

job_skills = extract_job_skills(
    job_description
)


# ============================================================
# CALCULATE JOB MATCH
# ============================================================

match_percentage, matching_skills, missing_skills = calculate_match(
    resume_data["skills"],
    job_skills
)


# ============================================================
# JOB MATCH ANALYSIS
# ============================================================

st.markdown("---")

st.header("🎯 Job Match Analysis")


# IMPORTANT:
# Using Streamlit native components here.
# No HTML score-number / score-text code will be displayed.

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        label="🎯 Job Match",
        value=f"{match_percentage:.0f}%"
    )


with col2:

    st.metric(
        label="✅ Matching Skills",
        value=len(matching_skills)
    )


with col3:

    st.metric(
        label="❌ Missing Skills",
        value=len(missing_skills)
    )


# ============================================================
# MATCH PROGRESS
# ============================================================

st.write("### 📈 Match Progress")

st.progress(
    min(
        max(
            int(match_percentage),
            0
        ),
        100
    ) / 100
)


# ============================================================
# MATCHING / MISSING SKILLS
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("✅ Matching Skills")

    if matching_skills:

        for skill in matching_skills:

            st.markdown(
                f"""
                <div class="match-box">
                    ✅ {skill}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.warning(
            "No matching skills found."
        )


with col2:

    st.subheader("❌ Missing Skills")

    if missing_skills:

        for skill in missing_skills:

            st.markdown(
                f"""
                <div class="missing-box">
                    ❌ {skill}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.success(
            "🎉 No major missing skills detected!"
        )


# ============================================================
# ATS SCORE
# ============================================================

st.markdown("---")

st.header("📊 ATS Score")


ats_score = calculate_ats_score(
    resume_text,
    resume_data["skills"],
    job_skills,
    matching_skills,
    missing_skills
)


# Native Streamlit metric
# No HTML score-number here.

ats_col1, ats_col2, ats_col3 = st.columns(3)


with ats_col1:

    st.metric(
        "📊 ATS Resume Score",
        f"{ats_score}/100"
    )


with ats_col2:

    st.metric(
        "🛠️ Resume Skills",
        len(resume_data["skills"])
    )


with ats_col3:

    st.metric(
        "📋 Job Skills",
        len(job_skills)
    )


st.progress(
    max(
        0,
        min(
            ats_score,
            100
        )
    ) / 100
)


st.success(
    get_score_message(
        ats_score
    )
)


# ============================================================
# IMPROVEMENT SUGGESTIONS
# ============================================================

st.header("💡 Improvement Suggestions")


suggestions = get_improvement_suggestions(
    resume_text,
    resume_data["skills"],
    missing_skills
)


for suggestion in suggestions:

    st.info(
        f"💡 {suggestion}"
    )


# ============================================================
# GEMINI AI
# ============================================================

st.markdown("---")

st.header("🧠 Gemini AI Resume Analysis")


st.write(
    "Get personalized AI feedback by comparing "
    "your resume with the selected job description."
)


if st.button(
    "✨ Generate AI Feedback"
):

    with st.spinner(
        "🧠 Gemini is analyzing your resume..."
    ):

        ai_feedback = get_ai_feedback(
            resume_text,
            job_description
        )


    if ai_feedback:

        if ai_feedback.startswith(
            "❌ Gemini"
        ):

            st.error(
                ai_feedback
            )

        else:

            st.success(
                "🎉 AI analysis completed successfully!"
            )

            st.markdown(
                ai_feedback
            )

    else:

        st.warning(
            "No AI feedback was generated."
        )


# ============================================================
# EXTRACTED RESUME TEXT
# ============================================================

st.markdown("---")

with st.expander(
    "📄 View Extracted Resume Text"
):

    st.text(
        resume_text
    )