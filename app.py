import streamlit as st
from streamlit_option_menu import option_menu
from resume_parser import extract_text
from gpt_engine import generate_questions, evaluate_answer
import pandas as pd
import plotly.express as px
from feedback import calculate_ats_score, get_feedback
import os

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

# ================= HOME =================
if selected == "Home":

    st.title("🧠 AI Interview Assistant")

    uploaded_file = st.file_uploader("📄 Upload Resume", type=["pdf"])

    if uploaded_file:

        with st.spinner("Analyzing Resume..."):
            resume_text = extract_text(uploaded_file)

        st.success("Resume Uploaded Successfully!")

        st.subheader("📄 Resume Preview")
        st.text_area("", resume_text[:2000], height=250)

        # Skills detection
        keywords = ["Python", "Machine Learning", "SQL", "Data Science", "Deep Learning", "Java"]
        skills = [k for k in keywords if k.lower() in resume_text.lower()]

        st.subheader("🛠️ Skills")
        st.write(skills)

        # ---------------- VOICE INPUT ----------------
        if "voice_answer" not in st.session_state:
            st.session_state.voice_answer = ""

        if st.button("🎤 Speak Answer"):
            with st.spinner("Listening... 🎤"):
                st.session_state.voice_answer = record_voice()

        st.write("Your Answer:")
        st.write(st.session_state.voice_answer)

        # ---------------- GPT QUESTIONS ----------------
        st.subheader("🎤 AI Interview Questions")

        questions = generate_questions(" ".join(skills))
        question_list = questions.split("\n")

        answers = []

        for i, q in enumerate(question_list):
            if q.strip():
                st.markdown(f"### {q}")
                ans = st.text_area("Your Answer", key=f"ans_{i}")
                answers.append((q, ans))

        # ---------------- FEEDBACK ----------------
        if st.button("🧠 Get AI Feedback"):
            for q, ans in answers:
                if ans.strip():
                    feedback = evaluate_answer(q, ans)
                    st.info(f"**Q:** {q}\n\n{feedback}")

        # ---------------- ATS SCORE ----------------
        st.subheader("📊 ATS Score")

        ats_score = calculate_ats_score(resume_text, skills)

        st.metric("Resume Match Score", f"{ats_score}/100")
        st.progress(int(ats_score))

# ================= DASHBOARD =================
elif selected == "Dashboard":

    st.title("📈 Performance Dashboard")

    df = pd.DataFrame({
        "Category": ["Technical", "Communication", "Confidence"],
        "Score": [85, 70, 80]
    })

    fig = px.bar(df, x="Category", y="Score")
    st.plotly_chart(fig, use_container_width=True)

# ================= ABOUT =================
# ================= ABOUT =================
elif selected == "About":

    st.title("ℹ️ About Project")

    st.write("AI Interview Assistant helps you practice AI-powered interviews.")

    # ---------------- SAFE LOGO IMAGE ----------------
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")

    if os.path.exists(logo_path):
        st.image(logo_path, width=150)
    else:
        st.warning("⚠️ Logo image not found in assets folder")

    # ---------------- DEBUG (SAFE) ----------------
    assets_path = os.path.join(os.path.dirname(__file__), "assets")

    if os.path.exists(assets_path):
        st.write("📁 Assets files:", os.listdir(assets_path))
    else:
        st.error("❌ Assets folder not found!")