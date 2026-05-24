import streamlit as st
from streamlit_option_menu import option_menu
from resume_parser import extract_text
from gpt_engine import generate_questions, evaluate_answer
from feedback import calculate_ats_score
import pandas as pd
import plotly.express as px
import os

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="InterviewAI — Smart Interview Prep",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  GLOBAL CSS  (100 % light — zero dark surfaces)
# ─────────────────────────────────────────────
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&display=swap');

/* ── ROOT PALETTE ─────────────────────────── */
:root {
    --white:       #FFFFFF;
    --bg:          #F5F7FA;
    --surface:     #FFFFFF;
    --border:      #E4E9F0;
    --border-soft: #EEF2F7;
    --text:        #111827;
    --text-2:      #374151;
    --text-3:      #6B7280;
    --text-4:      #9CA3AF;
    --blue:        #3B82F6;
    --blue-light:  #EFF6FF;
    --blue-mid:    #BFDBFE;
    --green:       #10B981;
    --green-light: #ECFDF5;
    --amber:       #F59E0B;
    --amber-light: #FFFBEB;
    --violet:      #8B5CF6;
    --violet-light:#F5F3FF;
    --coral:       #F97316;
    --coral-light: #FFF7ED;
    --red-light:   #FEF2F2;
    --font:        'Plus Jakarta Sans', sans-serif;
    --mono:        'DM Mono', monospace;
    --radius:      14px;
    --radius-sm:   8px;
}

/* ── RESET / BASE ─────────────────────────── */
html, body, [class*="css"] {
    font-family: var(--font) !important;
    color: var(--text) !important;
}

/* ── STREAMLIT CHROME ─────────────────────── */
.stApp {
    background-color: var(--bg) !important;
}

.main .block-container {
    background-color: var(--bg) !important;
    padding: 2rem 2.5rem 3rem !important;
    max-width: 1120px !important;
}

/* hide streamlit top bar decoration */
header[data-testid="stHeader"] {
    background: var(--bg) !important;
    border-bottom: 1px solid var(--border) !important;
}

/* ── SIDEBAR — fully light ────────────────── */
[data-testid="stSidebar"] {
    background-color: var(--white) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    font-family: var(--font) !important;
}

/* nav-menu container inside sidebar */
[data-testid="stSidebar"] section {
    background: var(--white) !important;
}

/* ── HEADINGS ─────────────────────────────── */
h1 { color: var(--text)   !important; font-weight: 700 !important; font-size: 1.75rem !important; letter-spacing: -0.4px !important; }
h2 { color: var(--text-2) !important; font-weight: 600 !important; }
h3 { color: var(--text-2) !important; font-weight: 600 !important; }

/* ── BUTTONS ──────────────────────────────── */
.stButton > button {
    background: var(--blue)       !important;
    color: #fff                   !important;
    border: none                  !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font)      !important;
    font-weight: 600              !important;
    font-size: 13.5px             !important;
    padding: 0.55rem 1.3rem       !important;
    transition: all .18s ease     !important;
    box-shadow: 0 1px 4px rgba(59,130,246,.20) !important;
}
.stButton > button:hover {
    background: #2563EB           !important;
    box-shadow: 0 3px 10px rgba(59,130,246,.30) !important;
    transform: translateY(-1px)   !important;
}

/* ── FILE UPLOADER ────────────────────────── */
[data-testid="stFileUploader"] {
    background: var(--blue-light) !important;
    border: 2px dashed var(--blue-mid) !important;
    border-radius: var(--radius)  !important;
    padding: 1.25rem              !important;
}
[data-testid="stFileUploader"] label {
    color: var(--text-2) !important;
    font-weight: 500 !important;
}

/* ── SELECTBOX ────────────────────────────── */
.stSelectbox > div > div {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
}

/* ── TEXT AREAS ───────────────────────────── */
.stTextArea textarea {
    background:   var(--bg)     !important;
    border:       1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    font-family:  var(--font)   !important;
    font-size:    13px          !important;
    color:        var(--text)   !important;
}
.stTextArea textarea:focus {
    border-color: var(--blue)   !important;
    background:   var(--white)  !important;
    box-shadow:   0 0 0 3px rgba(59,130,246,.12) !important;
}

/* ── ALERTS ───────────────────────────────── */
.stSuccess {
    background: var(--green-light) !important;
    border: 1px solid #6EE7B7 !important;
    border-radius: var(--radius-sm) !important;
    color: #065F46 !important;
}
.stWarning {
    background: var(--amber-light) !important;
    border: 1px solid #FCD34D !important;
    border-radius: var(--radius-sm) !important;
    color: #78350F !important;
}

/* ── SPINNER ──────────────────────────────── */
.stSpinner > div { border-top-color: var(--blue) !important; }

/* ── METRICS ──────────────────────────────── */
[data-testid="metric-container"] {
    background: var(--white) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius) !important;
    padding: 1.1rem 1.4rem !important;
}
[data-testid="metric-container"] label {
    color: var(--text-3) !important;
    font-size: 12px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: .4px;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--blue) !important;
    font-size: 1.9rem !important;
    font-weight: 700 !important;
}

/* ── PROGRESS ─────────────────────────────── */
.stProgress > div {
    background: var(--border) !important;
    border-radius: 6px !important;
    height: 9px !important;
}
.stProgress > div > div {
    background: linear-gradient(90deg, var(--blue), var(--green)) !important;
    border-radius: 6px !important;
    height: 9px !important;
}

/* ── DIVIDER ──────────────────────────────── */
hr {
    border: none !important;
    border-top: 1px solid var(--border) !important;
    margin: 1.5rem 0 !important;
}

/* ══════════════════════════════════════════
   CUSTOM COMPONENT STYLES
   ══════════════════════════════════════════ */

/* Page header banner */
.page-header {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 26px 30px;
    margin-bottom: 22px;
    display: flex;
    align-items: center;
    gap: 16px;
}
.ph-icon  { font-size: 38px; line-height: 1; }
.ph-title { font-size: 22px; font-weight: 700; color: var(--text); margin: 0 0 3px; letter-spacing: -.4px; }
.ph-sub   { font-size: 13px; color: var(--text-3); margin: 0; }

/* Generic card */
.card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 22px 24px;
    margin-bottom: 16px;
}
.card-title { font-size: 15px; font-weight: 700; color: var(--text);   margin-bottom: 3px; }
.card-sub   { font-size: 13px; color: var(--text-3); margin-bottom: 15px; }

/* Skill chips */
.skill-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 5px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
    background: var(--blue-light);
    color: #1D4ED8;
    border: 1px solid var(--blue-mid);
    margin: 3px;
}
.skill-dot { width:6px; height:6px; border-radius:50%; background:var(--blue); display:inline-block; }

/* Question card */
.q-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-left: 4px solid var(--blue);
    border-radius: var(--radius);
    padding: 18px 22px;
    margin-bottom: 14px;
}
.q-num {
    display: inline-flex; align-items: center; justify-content: center;
    width: 26px; height: 26px;
    background: var(--blue); color: #fff;
    border-radius: var(--radius-sm);
    font-size: 12px; font-weight: 700;
    margin-bottom: 8px;
}
.q-text {
    font-size: 14px; font-weight: 500; color: var(--text-2);
    line-height: 1.7; margin-bottom: 4px;
}
.cat-badge { display:inline-block; font-size:11px; font-weight:600; padding:3px 9px; border-radius:6px; margin-bottom:10px; }
.cat-technical   { background:#EFF6FF; color:#1D4ED8; }
.cat-behavioral  { background:#FFFBEB; color:#92400E; }
.cat-situational { background:#ECFDF5; color:#065F46; }

/* Feedback card */
.fb-card {
    background: var(--green-light);
    border: 1px solid #A7F3D0;
    border-radius: var(--radius);
    padding: 18px 22px;
    margin: 10px 0 16px;
}
.fb-head  { font-size:13px; font-weight:700; color:#065F46; margin-bottom:8px; }
.fb-q     { font-size:13px; font-weight:600; color:#064E3B; margin-bottom:6px; }
.fb-text  { font-size:13px; line-height:1.8; color:#047857; }
.fb-badge {
    display:inline-block;
    background: var(--green); color:#fff;
    font-size:11px; font-weight:700;
    padding:2px 9px; border-radius:20px; margin-left:8px;
}

/* Section divider label */
.sec-div {
    display:flex; align-items:center; gap:12px;
    margin: 26px 0 18px;
}
.sec-div-line  { flex:1; height:1px; background:var(--border); }
.sec-div-label {
    font-size:11px; font-weight:700; color:var(--text-4);
    text-transform:uppercase; letter-spacing:1px; white-space:nowrap;
}

/* Resume preview mono box */
.mono-box {
    background: var(--bg);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 14px;
    font-family: var(--mono);
    font-size: 12px; line-height: 1.7;
    color: var(--text-3);
    max-height: 190px; overflow-y: auto;
    white-space: pre-wrap;
}

/* ATS breakdown bars */
.ats-grid   { display:flex; flex-direction:column; gap:9px; }
.ats-row    { display:flex; align-items:center; gap:10px; }
.ats-lbl    { font-size:12px; color:var(--text-3); width:125px; flex-shrink:0; }
.ats-track  { flex:1; background:var(--border-soft); border-radius:4px; height:7px; overflow:hidden; }
.ats-fill   { height:7px; border-radius:4px; }
.ats-pct    { font-size:11px; font-weight:700; color:var(--text-2); width:34px; text-align:right; font-family:var(--mono); }

/* Stat cards (dashboard) */
.stat-card {
    background: var(--white);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 18px 20px;
    text-align: center;
}
.stat-icon   { font-size:26px; margin-bottom:6px; }
.stat-lbl    { font-size:11px; font-weight:600; color:var(--text-4); text-transform:uppercase; letter-spacing:.5px; margin-bottom:5px; }
.stat-val    { font-size:24px; font-weight:700; letter-spacing:-1px; }
.stat-change { font-size:11px; color:var(--text-4); margin-top:3px; }
.c-blue   { color:var(--blue);   }
.c-green  { color:var(--green);  }
.c-amber  { color:var(--amber);  }
.c-violet { color:var(--violet); }

/* Session rows */
.sess-row {
    display:flex; align-items:center; gap:12px;
    padding:12px 14px; background:var(--bg);
    border-radius:var(--radius-sm); margin-bottom:9px;
}
.sess-icon  { font-size:20px; }
.sess-title { font-size:13px; font-weight:600; color:var(--text-2); }
.sess-meta  { font-size:12px; color:var(--text-4); }
.sess-badge {
    margin-left:auto; font-size:11px; font-weight:700;
    padding:3px 10px; border-radius:20px;
}
.s-high { background:var(--green-light);  color:#059669; }
.s-mid  { background:var(--blue-light);   color:#1D4ED8; }
.s-low  { background:var(--amber-light);  color:#B45309; }

/* Feature rows (about) */
.feat-row {
    display:flex; gap:14px; padding:15px 0;
    border-bottom:1px solid var(--border-soft);
    align-items:flex-start;
}
.feat-row:last-child { border-bottom:none; }
.feat-icon-box {
    width:40px; height:40px; border-radius:var(--radius-sm);
    display:flex; align-items:center; justify-content:center;
    font-size:19px; flex-shrink:0;
}
.feat-name { font-size:14px; font-weight:600; color:var(--text);   margin-bottom:3px; }
.feat-desc { font-size:12px; color:var(--text-3); line-height:1.65; }

/* Sidebar logo strip */
.sb-logo {
    padding: 0 6px 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 6px;
}
.sb-brand     { display:flex; align-items:center; gap:10px; }
.sb-icon      { width:36px; height:36px; background:linear-gradient(135deg,#3B82F6,#8B5CF6); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:18px; flex-shrink:0; }
.sb-name      { font-size:16px; font-weight:700; color:var(--text)  !important; letter-spacing:-.3px; }
.sb-sub       { font-size:11px; color:var(--text-4) !important; }
.sb-tip       { background:var(--blue-light); border:1px solid var(--blue-mid); border-radius:var(--radius-sm); padding:11px 13px; margin-top:16px; }
.sb-tip-text  { font-size:12px; color:#1D4ED8 !important; line-height:1.6; }
.sb-user      { display:flex; align-items:center; gap:9px; padding:9px 11px; background:var(--bg); border-radius:var(--radius-sm); margin-top:16px; }
.sb-avatar    { width:30px; height:30px; background:linear-gradient(135deg,#3B82F6,#8B5CF6); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:12px; font-weight:700; color:#fff; flex-shrink:0; }
.sb-uname     { font-size:13px; font-weight:600; color:var(--text)  !important; }
.sb-urole     { font-size:11px; color:var(--text-4) !important; }

</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:

    st.markdown("""
    <div class="sb-logo">
        <div class="sb-brand">
            <div class="sb-icon">🧠</div>
            <div>
                <div class="sb-name">InterviewAI</div>
                <div class="sb-sub">Powered by Gemini</div>
            </div>
        </div>
        <div class="sb-tip">
            <div class="sb-tip-text">💡 Upload your resume to get personalized questions and AI feedback.</div>
        </div>
        <div class="sb-user">
            <div class="sb-avatar">U</div>
            <div>
                <div class="sb-uname">User</div>
                <div class="sb-urole">Job Seeker</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    selected = option_menu(
        menu_title=None,
        options=["Home", "Practice", "Dashboard", "About"],
        icons=["house", "mic", "bar-chart-line", "info-circle"],
        default_index=0,
        styles={
            "container":         {"background-color": "#FFFFFF", "padding": "0"},
            "nav-link":          {
                "font-family": "'Plus Jakarta Sans', sans-serif",
                "font-size": "13.5px",
                "font-weight": "400",
                "color": "#6B7280",
                "border-radius": "8px",
                "margin-bottom": "2px",
            },
            "nav-link-selected": {
                "background-color": "#EFF6FF",
                "color": "#1D4ED8",
                "font-weight": "600",
            },
            "icon": {"font-size": "15px"},
        }
    )


# ─────────────────────────────────────────────
#  HOME
# ─────────────────────────────────────────────
if selected == "Home":

    st.markdown("""
    <div class="page-header">
        <div class="ph-icon">👋</div>
        <div>
            <div class="ph-title">Welcome to InterviewAI</div>
            <div class="ph-sub">Upload your resume to begin your AI-powered interview session</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">📄 Upload Your Resume</div>'
                '<div class="card-sub">We\'ll analyse your skills and generate tailored questions</div>',
                unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop your PDF resume here, or click to browse",
        type=["pdf"],
        label_visibility="visible"
    )
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file:

        with st.spinner("🔍 Analysing your resume..."):
            resume_text = extract_text(uploaded_file)

        st.success("✅ Resume uploaded and analysed successfully!")

        # Resume preview
        st.markdown('<div class="card"><div class="card-title">📄 Resume Preview</div>'
                    '<div class="card-sub">Extracted content from your document</div>',
                    unsafe_allow_html=True)
        preview = (resume_text[:2000] if resume_text else "Could not extract text.")
        st.markdown(f'<div class="mono-box">{preview}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        # Skills
        keywords = [
            "Python","Machine Learning","SQL","Data Science","Deep Learning",
            "Java","Streamlit","AI","NLP","TensorFlow","PyTorch","FastAPI","Docker","AWS"
        ]
        skills = [k for k in keywords if k.lower() in resume_text.lower()]

        st.markdown('<div class="card"><div class="card-title">🛠️ Detected Skills</div>'
                    '<div class="card-sub">Skills identified from your resume</div>',
                    unsafe_allow_html=True)
        if skills:
            chips = "".join(
                f'<span class="skill-chip"><span class="skill-dot"></span>{s}</span>'
                for s in skills
            )
            st.markdown(f'<div style="line-height:2.4;">{chips}</div>', unsafe_allow_html=True)
        else:
            st.warning("No common skills detected — please check your resume format.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Questions
        st.markdown("""
        <div class="sec-div">
            <div class="sec-div-line"></div>
            <div class="sec-div-label">AI Interview Questions</div>
            <div class="sec-div-line"></div>
        </div>
        """, unsafe_allow_html=True)

        with st.spinner("🤖 Generating personalised questions..."):
            questions = generate_questions(" ".join(skills))

        question_list = questions if isinstance(questions, list) else [
            q for q in questions.split("\n") if q.strip()
        ]

        cats = ["technical", "behavioral", "situational", "technical", "behavioral"]
        answers = []

        for i, q in enumerate(question_list):
            if not q.strip():
                continue
            cat = cats[i % len(cats)]
            st.markdown(f"""
            <div class="q-card">
                <div class="q-num">{i+1}</div>
                <span class="cat-badge cat-{cat}">{cat.capitalize()}</span>
                <div class="q-text">{q}</div>
            </div>
            """, unsafe_allow_html=True)
            ans = st.text_area(
                "Answer",
                placeholder="Type your answer here — be specific and use examples.",
                key=f"ans_{i}", height=95,
                label_visibility="collapsed"
            )
            answers.append((q, ans))

        st.markdown("<br>", unsafe_allow_html=True)

        # Feedback button
        _, col_mid, _ = st.columns([1, 2, 1])
        with col_mid:
            get_fb = st.button("🧠 Get AI Feedback on All Answers", use_container_width=True)

        if get_fb:
            st.markdown("""
            <div class="sec-div">
                <div class="sec-div-line"></div>
                <div class="sec-div-label">AI Evaluation</div>
                <div class="sec-div-line"></div>
            </div>
            """, unsafe_allow_html=True)

            answered = [(q, a) for q, a in answers if a.strip()]
            if not answered:
                st.warning("⚠️ Please answer at least one question before requesting feedback.")
            else:
                for q, ans in answered:
                    with st.spinner("Evaluating answer..."):
                        feedback = evaluate_answer(q, ans)
                    st.markdown(f"""
                    <div class="fb-card">
                        <div class="fb-head">✅ Feedback <span class="fb-badge">Evaluated</span></div>
                        <div class="fb-q">Q: {q[:100]}{"..." if len(q)>100 else ""}</div>
                        <div class="fb-text">{feedback}</div>
                    </div>
                    """, unsafe_allow_html=True)

        # ATS Score
        st.markdown("""
        <div class="sec-div">
            <div class="sec-div-line"></div>
            <div class="sec-div-label">ATS Resume Score</div>
            <div class="sec-div-line"></div>
        </div>
        """, unsafe_allow_html=True)

        ats_score = calculate_ats_score(resume_text, skills)

        st.markdown('<div class="card"><div class="card-title">📊 ATS Compatibility Score</div>'
                    '<div class="card-sub">How well your resume performs against Applicant Tracking Systems</div>',
                    unsafe_allow_html=True)

        col_a, col_b = st.columns([1, 2])
        with col_a:
            st.metric(
                "Resume Match Score",
                f"{ats_score}/100",
                delta=f"+{max(0, ats_score-70)} above baseline" if ats_score > 70 else "Needs improvement"
            )
        with col_b:
            st.markdown("<div style='margin-top:6px;'>", unsafe_allow_html=True)
            st.progress(int(ats_score) / 100)
            breakdown = {
                "Keyword Match":  min(100, int(ats_score * 1.05)),
                "Format Score":   min(100, int(ats_score * 0.90)),
                "Relevance":      min(100, int(ats_score * 1.10)),
                "Completeness":   min(100, int(ats_score * 0.85)),
            }
            colors = ["#3B82F6","#10B981","#F59E0B","#F97316"]
            html = '<div class="ats-grid" style="margin-top:10px;">'
            for (lbl, val), clr in zip(breakdown.items(), colors):
                html += f"""
                <div class="ats-row">
                    <div class="ats-lbl">{lbl}</div>
                    <div class="ats-track"><div class="ats-fill" style="width:{val}%;background:{clr};"></div></div>
                    <div class="ats-pct">{val}%</div>
                </div>"""
            html += '</div>'
            st.markdown(html, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  PRACTICE
# ─────────────────────────────────────────────
elif selected == "Practice":

    st.markdown("""
    <div class="page-header">
        <div class="ph-icon">🎤</div>
        <div>
            <div class="ph-title">Interview Practice</div>
            <div class="ph-sub">Configure a session and sharpen your answers</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">⚙️ Configure Your Session</div>'
                '<div class="card-sub">Choose mode, difficulty, and question count</div>',
                unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        mode = st.selectbox("Interview Mode", ["Technical", "Behavioral", "Mixed"])
    with col2:
        difficulty = st.selectbox("Difficulty", ["Easy 🌱", "Medium 🔥", "Hard ⚡"])
    with col3:
        num_q = st.selectbox("Number of Questions", [3, 5, 7, 10])
    st.markdown('</div>', unsafe_allow_html=True)

    col_btn, _ = st.columns([1, 2])
    with col_btn:
        start = st.button("▶ Start Practice Session", use_container_width=True)

    if start:
        pool = [
            "Explain the difference between supervised and unsupervised learning.",
            "Walk me through how you would design a scalable NLP pipeline.",
            "Describe a challenging project and how you overcame obstacles.",
            "How do you handle model performance issues in production?",
            "What is your approach to debugging complex data pipelines?",
            "Tell me about a time you had to learn a new technology quickly.",
            "How would you explain a technical concept to a non-technical stakeholder?",
            "Describe your experience with version control and CI/CD.",
            "What strategies do you use to prioritise competing tasks?",
            "Where do you see AI/ML evolving in the next 5 years?",
        ]
        st.session_state["prac_qs"] = pool[:num_q]

    if "prac_qs" in st.session_state:
        for i, q in enumerate(st.session_state["prac_qs"]):
            st.markdown(f"""
            <div class="q-card">
                <div class="q-num">{i+1}</div>
                <div class="q-text">{q}</div>
            </div>
            """, unsafe_allow_html=True)
            st.text_area("Answer", placeholder="Structure your answer clearly...",
                         key=f"prac_{i}", height=88, label_visibility="collapsed")


# ─────────────────────────────────────────────
#  DASHBOARD
# ─────────────────────────────────────────────
elif selected == "Dashboard":

    st.markdown("""
    <div class="page-header">
        <div class="ph-icon">📈</div>
        <div>
            <div class="ph-title">Performance Dashboard</div>
            <div class="ph-sub">Track your interview readiness over time</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Stat cards
    c1, c2, c3, c4 = st.columns(4)
    stats = [
        ("📝","Sessions Done",      "12",   "+3 this week",    "c-blue"),
        ("⭐","Average Score",      "82%",  "↑ 5% this week",  "c-green"),
        ("⏱️","Hours Practiced",    "6.5h", "Target: 10h/wk",  "c-amber"),
        ("🎯","Questions Answered", "84",   "All sessions",     "c-violet"),
    ]
    for col, (icon, lbl, val, chg, cls) in zip([c1,c2,c3,c4], stats):
        with col:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-icon">{icon}</div>
                <div class="stat-lbl">{lbl}</div>
                <div class="stat-val {cls}">{val}</div>
                <div class="stat-change">{chg}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_l, col_r = st.columns([3, 2])

    with col_l:
        st.markdown('<div class="card"><div class="card-title">Performance Breakdown</div>'
                    '<div class="card-sub">Average scores across interview categories</div>',
                    unsafe_allow_html=True)
        df = pd.DataFrame({
            "Category": ["Technical","Communication","Confidence","Problem Solving","Behavioral"],
            "Score":    [85, 70, 80, 90, 75],
        })
        fig = px.bar(df, x="Category", y="Score", text="Score",
                     color="Category",
                     color_discrete_sequence=["#3B82F6","#10B981","#F59E0B","#F97316","#8B5CF6"])
        fig.update_traces(textposition="outside", marker_line_width=0, width=0.5)
        fig.update_layout(
            template="plotly_white", height=300, showlegend=False,
            margin=dict(l=0,r=0,t=10,b=0),
            plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
            font=dict(family="Plus Jakarta Sans",size=12,color="#6B7280"),
            yaxis=dict(range=[0,105],gridcolor="#F5F7FA"),
            xaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="card"><div class="card-title">Score Trend</div>'
                    '<div class="card-sub">Last 6 sessions</div>',
                    unsafe_allow_html=True)
        tdf = pd.DataFrame({
            "Session": [f"S{i+1}" for i in range(6)],
            "Score":   [62,68,71,75,80,82]
        })
        fig2 = px.line(tdf, x="Session", y="Score", markers=True)
        fig2.update_traces(
            line_color="#3B82F6", line_width=2.5,
            marker=dict(size=7, color="#3B82F6", line=dict(color="white",width=2))
        )
        fig2.update_layout(
            template="plotly_white", height=300,
            margin=dict(l=0,r=0,t=10,b=0),
            plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
            font=dict(family="Plus Jakarta Sans",size=12,color="#6B7280"),
            yaxis=dict(range=[50,100],gridcolor="#F5F7FA"),
            xaxis=dict(showgrid=False),
        )
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Recent sessions
    st.markdown('<div class="card"><div class="card-title">Recent Sessions</div>'
                '<div class="card-sub">Your latest practice history</div>',
                unsafe_allow_html=True)
    sessions = [
        ("💻","Technical Round — Python + ML",  "7 questions · 28 min","88","s-high"),
        ("🤝","Behavioral Round — Leadership",   "5 questions · 18 min","74","s-mid"),
        ("🎯","Mixed Round — Full Stack",        "9 questions · 40 min","68","s-low"),
    ]
    for icon, title, meta, score, badge in sessions:
        st.markdown(f"""
        <div class="sess-row">
            <div class="sess-icon">{icon}</div>
            <div>
                <div class="sess-title">{title}</div>
                <div class="sess-meta">{meta}</div>
            </div>
            <span class="sess-badge {badge}">{score}%</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  ABOUT
# ─────────────────────────────────────────────
elif selected == "About":

    st.markdown("""
    <div class="page-header">
        <div class="ph-icon">ℹ️</div>
        <div>
            <div class="ph-title">About InterviewAI</div>
            <div class="ph-sub">Your AI-powered interview preparation platform</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("""
        <div class="card">
            <div style="font-size:30px;margin-bottom:8px;">🧠</div>
            <div class="card-title">What is InterviewAI?</div>
            <p style="font-size:13px;line-height:1.8;color:#6B7280;">
                InterviewAI analyses your resume, generates targeted questions with Gemini AI,
                and gives real-time feedback — so you walk into every interview prepared.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with col_r:
        st.markdown("""
        <div class="card">
            <div style="font-size:30px;margin-bottom:8px;">🚀</div>
            <div class="card-title">How It Works</div>
            <p style="font-size:13px;line-height:1.8;color:#6B7280;">
                Upload resume → AI detects skills → Questions generated →
                You answer → AI evaluates & scores → Track progress over time.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="card"><div class="card-title">✨ Platform Features</div>',
                unsafe_allow_html=True)
    features = [
        ("📄","#EFF6FF","Resume Analysis",        "Extracts key skills, roles, and experience from PDF resumes using NLP"),
        ("🤖","#F5F3FF","AI Question Generation", "Gemini AI crafts personalised technical and behavioural questions"),
        ("⭐","#ECFDF5","Answer Evaluation",       "Real-time scoring and detailed feedback on quality, depth, and clarity"),
        ("📊","#FFFBEB","ATS Score Check",         "Measures how well your resume performs against Applicant Tracking Systems"),
        ("📈","#FFF7ED","Performance Dashboard",   "Visual analytics to track improvement and session history over time"),
    ]
    for icon, bg, name, desc in features:
        st.markdown(f"""
        <div class="feat-row">
            <div class="feat-icon-box" style="background:{bg};">{icon}</div>
            <div>
                <div class="feat-name">{name}</div>
                <div class="feat-desc">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="text-align:center;padding:28px 24px;">
        <div style="font-size:12px;color:#9CA3AF;">Powered by</div>
        <div style="font-size:24px;font-weight:700;color:#3B82F6;letter-spacing:-.4px;margin:4px 0;">
            Google Gemini AI
        </div>
        <div style="font-size:12px;color:#9CA3AF;">Built with Streamlit · v2.0 · 2025</div>
    </div>
    """, unsafe_allow_html=True)

    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    if os.path.exists(logo_path):
        st.image(logo_path, width=150)
