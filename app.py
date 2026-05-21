import streamlit as st
from streamlit_option_menu import option_menu
from resume_parser import extract_text
from question_generator import generate_questions
import plotly.express as px
import pandas as pd

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Interview Assistant",
    page_icon="🧠",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stButton>button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    background-color: #4B8BBE;
    color: white;
    border: none;
}

.css-1d391kg {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
with st.sidebar:

    selected = option_menu(
        menu_title="AI Interview Assistant",
        options=["Home", "Dashboard", "About"],
        icons=["house", "bar-chart", "info-circle"],
        default_index=0
    )

# ---------------- HOME PAGE ----------------
if selected == "Home":

    st.title("🧠 AI Interview Assistant")

    st.write("Upload your resume and practice AI-generated interviews.")

    uploaded_file = st.file_uploader(
        "📄 Upload Resume",
        type=["pdf"]
    )

    if uploaded_file is not None:

        with st.spinner("Analyzing Resume..."):
            resume_text = extract_text(uploaded_file)

        st.success("Resume Uploaded Successfully!")

        # Resume Preview
        st.subheader("📄 Resume Preview")

        st.text_area(
            "Resume Content",
            resume_text[:2000],
            height=250
        )

        # Skills Extraction (simple)
        skills = []

        keywords = [
            "Python",
            "Machine Learning",
            "SQL",
            "Data Science",
            "Deep Learning",
            "Java"
        ]

        for word in keywords:
            if word.lower() in resume_text.lower():
                skills.append(word)

        st.subheader("🛠️ Extracted Skills")

        for skill in skills:
            st.success(skill)

        # Generate Questions
        questions = generate_questions(" ".join(skills))

        st.subheader("🎤 Interview Questions")

        for i, q in enumerate(questions, 1):

            st.markdown(f"### {i}. {q}")

            st.text_area(
                f"Your Answer {i}",
                height=120,
                key=i
            )

        # ATS SCORE
        st.subheader("📊 ATS Score")

        ats_score = min(len(skills) * 15, 100)

        st.metric(
            "Resume Match Score",
            f"{ats_score}/100"
        )

        st.progress(ats_score)

# ---------------- DASHBOARD ----------------
elif selected == "Dashboard":

    st.title("📈 Performance Dashboard")

    data = pd.DataFrame({
        "Category": ["Technical", "Communication", "Confidence"],
        "Score": [85, 70, 80]
    })

    fig = px.bar(
        data,
        x="Category",
        y="Score",
        title="Interview Performance"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- ABOUT ----------------
elif selected == "About":

    st.title("ℹ️ About Project")

    st.write("""
    AI Interview Assistant is an intelligent platform that:
    
    - Analyzes resumes
    - Generates interview questions
    - Evaluates candidate skills
    - Provides ATS-style scoring
    
    Built using Streamlit + AI + NLP.
    """)