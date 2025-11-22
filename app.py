import streamlit as st
import pandas as pd
import plotly.express as px

from src.parser import parse_transcript, get_quick_stats
from src.advisor import (
    generate_project_ideas,
    generate_career_pathways,
    identify_skill_gaps,
    analyze_strengths_weaknesses,
)

# -------------------------------------------------------------------
# Page config
# -------------------------------------------------------------------
st.set_page_config(
    page_title="UNILAG Transcript Advisor",
    page_icon="🎓",
    layout="wide",
)

# -------------------------------------------------------------------
# Global styling
# -------------------------------------------------------------------
CSS = """
<style>
:root {
    --primary: #2563eb;
    --primary-soft: #eff6ff;
    --accent: #f97316;
    --bg: #f3f4f6;
    --text-main: #0f172a;
    --text-muted: #6b7280;
    --card-bg: #ffffff;
    --border-subtle: #e5e7eb;
    --radius-lg: 1.25rem;
}

/* Bring everything closer to the top */
.block-container {
    padding-top: 3.5rem !important;
}

.stApp {
    background: radial-gradient(circle at top left, #f9fafb 0, var(--bg) 45%, #e5e7eb 100%);
}

/* Centered main container */
.app-container {
    max-width: 1100px;
    margin: 0 auto;
    padding-bottom: 3rem;
}

/* ---------- Modern compact header ---------- */

.app-header-shell {
    display: flex;
    justify-content: center;
    margin-top: 0.15rem;
    margin-bottom: 0.75rem;
}

.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1rem;
    padding: 0.6rem 1.1rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.92);
    border: 1px solid rgba(148, 163, 184, 0.45);
    box-shadow: 0 12px 30px rgba(15, 23, 42, 0.08);
    backdrop-filter: blur(18px);
}

.app-header-main {
    display: flex;
    align-items: center;
    gap: 0.6rem;
}

.app-logo-pill {
    width: 32px;
    height: 32px;
    border-radius: 999px;
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--primary-soft);
    font-size: 1.1rem;
}

.app-header-text {
    display: flex;
    flex-direction: column;
    gap: 0.05rem;
}

.app-header-title {
    font-size: 0.98rem;
    font-weight: 600;
    letter-spacing: -0.01em;
    color: var(--text-main);
}

.app-header-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.app-header-tag {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.2rem 0.7rem;
    border-radius: 999px;
    background: #ecfeff;
    color: #0e7490;
    border: 1px solid rgba(14, 116, 144, 0.35);
    white-space: nowrap;
}

/* Mobile tweaks */
@media (max-width: 768px) {
    .app-header {
        flex-direction: column;
        align-items: flex-start;
        padding: 0.55rem 0.9rem;
    }
}

/* ---------- Upload card ---------- */

.upload-shell {
    margin-bottom: 1.5rem;
}

.upload-card {
    border-radius: 1.25rem;
    padding: 1.2rem 1.4rem;
    background: rgba(255, 255, 255, 0.96);
    border: 1px solid rgba(148, 163, 184, 0.35);
    box-shadow: 0 16px 40px rgba(15, 23, 42, 0.12);
}

.upload-title {
    font-size: 1rem;
    font-weight: 600;
    color: var(--text-main);
    margin-bottom: 0.3rem;
}

.upload-body {
    font-size: 0.86rem;
    color: var(--text-muted);
}

/* Make the file uploader blend into the card */
.upload-card div[data-testid="stFileUploader"] {
    padding-top: 0.2rem;
}

.upload-card div[data-testid="stFileUploader"] label {
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-main);
}

.upload-card div[data-testid="stFileUploader"] section[data-testid="stFileUploadDropzone"] {
    border-radius: 0.9rem;
}

/* ---------- Hero + sections ---------- */

.main-header {
    font-size: 2.25rem;
    line-height: 1.2;
    color: var(--text-main);
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
}

.sub-header {
    font-size: 1rem;
    color: var(--text-muted);
    margin-bottom: 1.25rem;
}

.hero {
    margin-top: 0.6rem;
    padding: 2.0rem 2.3rem;
    border-radius: 1.5rem;
    background: radial-gradient(circle at top left, #eff6ff 0, #ffffff 50%, #f9fafb 100%);
    border: 1px solid var(--border-subtle);
    box-shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
    display: flex;
    flex-wrap: wrap;
    gap: 2.5rem;
    align-items: center;
}

.hero-left {
    flex: 1 1 280px;
    min-width: 260px;
}

.hero-right {
    flex: 1 1 260px;
    min-width: 260px;
}

.hero-list {
    list-style: none;
    padding-left: 0;
    margin: 0.75rem 0 0.75rem 0;
}

.hero-list li {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
    color: var(--text-muted);
    margin-bottom: 0.35rem;
}

.hero-dot {
    width: 0.5rem;
    height: 0.5rem;
    border-radius: 999px;
    background: var(--accent);
}

.hero-hint {
    font-size: 0.85rem;
    color: var(--text-muted);
    margin-top: 0.75rem;
}

.hero-card {
    background: var(--card-bg);
    border-radius: 1.25rem;
    padding: 1.5rem 1.25rem;
    border: 1px solid var(--border-subtle);
    box-shadow: 0 12px 35px rgba(15, 23, 42, 0.06);
}

.hero-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
    font-size: 0.9rem;
    color: var(--text-muted);
}

.hero-chip {
    font-size: 0.75rem;
    padding: 0.15rem 0.5rem;
    border-radius: 999px;
    background: var(--primary-soft);
    color: var(--primary);
}

.hero-stat-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.75rem;
    margin-bottom: 0.5rem;
}

.hero-stat {
    padding: 0.75rem 0.7rem;
    border-radius: 0.9rem;
    border: 1px dashed rgba(148, 163, 184, 0.6);
    background: #f9fafb;
}

.hero-stat-label {
    font-size: 0.7rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.06em;
}

.hero-stat-value {
    font-size: 1rem;
    font-weight: 700;
    color: var(--text-main);
}

.hero-caption {
    font-size: 0.8rem;
    color: var(--text-muted);
}

.section {
    margin-top: 2.5rem;
}

.section-title-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 1rem;
    margin-bottom: 1.1rem;
}

.section-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--text-main);
}

.section-subtitle {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
    gap: 1rem;
}

.feature-item {
    background: var(--card-bg);
    border-radius: var(--radius-lg);
    padding: 1rem 1rem;
    border: 1px solid var(--border-subtle);
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.03);
}

.feature-icon {
    font-size: 1.1rem;
    margin-bottom: 0.35rem;
}

.feature-title {
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 0.25rem;
    color: var(--text-main);
}

.feature-body {
    font-size: 0.85rem;
    color: var(--text-muted);
}

.footer-text {
    text-align: center;
    color: var(--text-muted);
    font-size: 0.82rem;
    padding: 1.5rem 0 0.8rem 0;
}

/* Make metrics look more card-like */
div[data-testid="metric-container"] {
    background: var(--card-bg);
    border-radius: 1rem;
    padding: 0.7rem 0.9rem;
    border: 1px solid var(--border-subtle);
    box-shadow: 0 8px 22px rgba(15, 23, 42, 0.04);
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)

# -------------------------------------------------------------------
# App header (top center)
# -------------------------------------------------------------------
HEADER_HTML = """
<div class="app-container">
<div class="app-header-shell">
<div class="app-header">
<div class="app-header-main">
<div class="app-logo-pill">🎓</div>
<div class="app-header-text">
<div class="app-header-title">UNILAG Transcript Advisor</div>
<div class="app-header-subtitle">
Turn your transcript into clear insights, project ideas &amp; career direction.
</div>
</div>
</div>
<div class="app-header-tag">AI-powered</div>
</div>
</div>
</div>
"""

st.markdown(HEADER_HTML, unsafe_allow_html=True)

# -------------------------------------------------------------------
# Session state
# -------------------------------------------------------------------
if "df" not in st.session_state:
    st.session_state["df"] = None
if "student_info" not in st.session_state:
    st.session_state["student_info"] = None

df = st.session_state["df"]
student_info = st.session_state["student_info"]

# -------------------------------------------------------------------
# Main content container
# -------------------------------------------------------------------
st.markdown('<div class="app-container">', unsafe_allow_html=True)

# -------------------------------------------------------------------
# Upload card (main screen)
# -------------------------------------------------------------------
with st.container():
    st.markdown('<div class="upload-shell"><div class="upload-card">', unsafe_allow_html=True)

    left, right = st.columns([2, 3])

    with left:
        UPLOAD_COPY = """
<div class="upload-title">Upload your UNILAG transcript</div>
<div class="upload-body">
Drop in your official PDF transcript. We’ll parse it automatically and build your dashboard
— no manual data entry.
</div>
"""
        st.markdown(UPLOAD_COPY, unsafe_allow_html=True)

    with right:
        uploaded_file = st.file_uploader(
            "Choose your transcript (PDF)",
            type=["pdf"],
            label_visibility="collapsed",
            key="transcript_uploader",
        )

        if uploaded_file is not None:
            with st.spinner("Parsing transcript…"):
                try:
                    with open("temp_transcript.pdf", "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    df, student_info = parse_transcript("temp_transcript.pdf")
                    st.session_state["df"] = df
                    st.session_state["student_info"] = student_info
                    st.success("✅ Transcript parsed successfully")
                except Exception as e:
                    st.error(f"Error parsing transcript: {e}")

    st.markdown("</div></div>", unsafe_allow_html=True)

df = st.session_state["df"]
student_info = st.session_state["student_info"]

# -------------------------------------------------------------------
# Quick snapshot under upload (if transcript loaded)
# -------------------------------------------------------------------
if df is not None:
    stats = get_quick_stats(df)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric("Total Courses", stats["total_courses"])
    with c2:
        st.metric("Overall GPA", stats["overall_gpa"])
    with c3:
        st.metric("Total Credits", stats["total_credits"])

# -------------------------------------------------------------------
# Empty state (no transcript yet)
# -------------------------------------------------------------------
if df is None:
    HERO_HTML = """
<div class="hero">
<div class="hero-left">
<h1 class="main-header">Understand your transcript in minutes.</h1>
<p class="sub-header">
Upload your official UNILAG transcript once and get an overview of your performance,
tailored project ideas, and career pathway suggestions.
</p>
<ul class="hero-list">
<li><span class="hero-dot"></span> See your GPA and credit progress at a glance</li>
<li><span class="hero-dot"></span> Get final-year project ideas that match your strengths</li>
<li><span class="hero-dot"></span> Discover realistic career paths based on your courses</li>
</ul>
<p class="hero-hint">
📎 Start by uploading your PDF above. No manual data entry required.
</p>
</div>
<div class="hero-right">
<div class="hero-card">
<div class="hero-card-header">
<span>Preview of your dashboard</span>
<span class="hero-chip">Sample</span>
</div>
<div class="hero-stat-grid">
<div class="hero-stat">
<div class="hero-stat-label">Total Courses</div>
<div class="hero-stat-value">52</div>
</div>
<div class="hero-stat">
<div class="hero-stat-label">Overall GPA</div>
<div class="hero-stat-value">4.21</div>
</div>
<div class="hero-stat">
<div class="hero-stat-label">Total Credits</div>
<div class="hero-stat-value">132</div>
</div>
</div>
<p class="hero-caption">
Once your transcript is uploaded, you’ll see your real numbers here – plus charts,
AI-generated project ideas, and more.
</p>
</div>
</div>
</div>
"""
    st.markdown(HERO_HTML, unsafe_allow_html=True)

    FEATURE_HTML = """
<div class="section">
<div class="section-title-row">
<div class="section-title">What you get</div>
<div class="section-subtitle">
Designed specifically for UNILAG students in their 200–500 level.
</div>
</div>
<div class="feature-grid">
<div class="feature-item">
<div class="feature-icon">🎯</div>
<div class="feature-title">Personalised project ideas</div>
<div class="feature-body">
AI suggests final-year project ideas that align with your courses, grades,
and interests.
</div>
</div>
<div class="feature-item">
<div class="feature-icon">💼</div>
<div class="feature-title">Career pathway explorer</div>
<div class="feature-body">
See realistic career paths you can grow into, plus how your current profile
already matches each one.
</div>
</div>
<div class="feature-item">
<div class="feature-icon">📈</div>
<div class="feature-title">Performance overview</div>
<div class="feature-body">
Visualize your best semesters, low points, and long-term GPA trend using clear,
interactive charts.
</div>
</div>
<div class="feature-item">
<div class="feature-icon">📚</div>
<div class="feature-title">Skill gaps &amp; next steps</div>
<div class="feature-body">
Identify missing skills and get recommendations on courses, topics, or projects
to close the gap.
</div>
</div>
</div>
</div>
"""
    st.markdown(FEATURE_HTML, unsafe_allow_html=True)

# -------------------------------------------------------------------
# Loaded state (transcript parsed)
# -------------------------------------------------------------------
else:
    TITLE_HTML = """
<div class="section-title-row" style="margin-top: 1.5rem;">
<div class="section-title">Student overview</div>
<div class="section-subtitle">Pulled automatically from your transcript.</div>
</div>
"""
    st.markdown(TITLE_HTML, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Name", student_info.get("Name", "N/A"))
    with col2:
        st.metric("Matric No", student_info.get("Matric_No", "N/A"))
    with col3:
        st.metric("Department", student_info.get("Department", "N/A"))
    with col4:
        st.metric("Faculty", student_info.get("Faculty", "N/A"))

    st.markdown("---")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "📊 Performance Overview",
            "🤖 AI Project Ideas",
            "💼 Career Pathways",
            "📚 Skill Gaps",
            "🎯 Detailed Analysis",
        ]
    )

    # Performance Overview tab
    with tab1:
        st.subheader("Academic Performance Overview")
        stats = get_quick_stats(df)

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Courses", stats["total_courses"])
        with c2:
            st.metric("Overall GPA", stats["overall_gpa"])
        with c3:
            st.metric("Total Credits", stats["total_credits"])
        with c4:
            st.metric("Best Grade", stats["best_grade"])

        st.markdown("---")

        col_left, col_right = st.columns(2)

        with col_left:
            st.subheader("Grade distribution")
            grade_counts = df["Grade"].value_counts().sort_index()
            fig = px.bar(
                x=grade_counts.index,
                y=grade_counts.values,
                labels={"x": "Grade", "y": "Count"},
                title="Grades distribution",
            )
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.subheader("GPA by year")
            if "Year" in df.columns and df["Year"].notna().any():
                gpa_by_year = df.groupby("Year")["Grade_Point"].mean().reset_index()
                fig = px.line(
                    gpa_by_year,
                    x="Year",
                    y="Grade_Point",
                    markers=True,
                    title="GPA progression",
                    labels={"Grade_Point": "Average GPA", "Year": "Year"},
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Year information not available in your transcript.")

        st.subheader("All courses")
        st.dataframe(
            df[
                [
                    "Course_Code",
                    "Course_Title",
                    "Credit_Unit",
                    "Grade",
                    "Grade_Point",
                    "Year",
                ]
            ],
            use_container_width=True,
        )

    # AI Project Ideas tab
    with tab2:
        st.subheader("AI-generated project ideas")
        num_ideas = st.slider("Number of project ideas", 3, 10, 5)

        if st.button("Generate project ideas", type="primary"):
            with st.spinner("Analyzing your transcript and generating ideas…"):
                try:
                    ideas = generate_project_ideas(df, student_info, num_ideas)
                    st.markdown(ideas)
                except Exception as e:
                    st.error(f"Error: {e}")

    # Career Pathways tab
    with tab3:
        st.subheader("Career pathway recommendations")

        if st.button("Generate career pathways", type="primary"):
            with st.spinner("Analyzing potential career fits…"):
                try:
                    careers = generate_career_pathways(df, student_info)
                    st.markdown(careers)
                except Exception as e:
                    st.error(f"Error: {e}")

    # Skill Gaps tab
    with tab4:
        st.subheader("Skill gap analysis")
        target_role = st.text_input(
            "Target role (optional)",
            placeholder="e.g., Software Engineer, Data Analyst",
        )

        if st.button("Identify skill gaps", type="primary"):
            with st.spinner("Comparing your profile to the target role…"):
                try:
                    gaps = identify_skill_gaps(
                        df,
                        student_info,
                        target_role if target_role else None,
                    )
                    st.markdown(gaps)
                except Exception as e:
                    st.error(f"Error: {e}")

    # Detailed Analysis tab
    with tab5:
        st.subheader("Detailed performance analysis")

        if st.button("Generate detailed analysis", type="primary"):
            with st.spinner("Analyzing your strengths and weaknesses…"):
                try:
                    analysis = analyze_strengths_weaknesses(df, student_info)
                    st.markdown(analysis)
                except Exception as e:
                    st.error(f"Error: {e}")

# -------------------------------------------------------------------
# Footer
# -------------------------------------------------------------------
st.markdown("---")
st.markdown(
    '<p class="footer-text">Built for UNILAG students 🚀 &nbsp;·&nbsp; Powered by Cohere AI</p>',
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)
