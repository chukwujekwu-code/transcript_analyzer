import streamlit as st
import pandas as pd
import plotly.express as px
from src.parser import parse_transcript, get_quick_stats
from src.advisor import (
    generate_project_ideas,
    generate_career_pathways,
    identify_skill_gaps,
    analyze_strengths_weaknesses
)

# Page config
st.set_page_config(
    page_title="UNILAG Transcript Advisor",
    page_icon="🎓",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        font-weight: bold;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<p class="main-header">🎓 UNILAG Transcript Advisor</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">AI-Powered Academic Guidance for UNILAG Students</p>', unsafe_allow_html=True)

# Initialize session state
if 'df' not in st.session_state:
    st.session_state['df'] = None
if 'student_info' not in st.session_state:
    st.session_state['student_info'] = None

# Sidebar
with st.sidebar:
    st.title("📋 Navigation")
    
    # File upload
    st.subheader("Upload Transcript")
    uploaded_file = st.file_uploader("Choose PDF file", type=['pdf'])
    
    if uploaded_file:
        # Save temporarily and parse
        with open("temp_transcript.pdf", "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        with st.spinner("Parsing transcript..."):
            try:
                df, student_info = parse_transcript("temp_transcript.pdf")
                st.session_state['df'] = df
                st.session_state['student_info'] = student_info
                st.success("✅ Transcript parsed successfully!")
            except Exception as e:
                st.error(f"Error parsing transcript: {e}")
    
    st.markdown("---")
    
    # Show stats if transcript loaded
    if st.session_state['df'] is not None:
        df = st.session_state['df']
        st.subheader("📊 Quick Stats")
        stats = get_quick_stats(df)
        st.metric("Total Courses", stats['total_courses'])
        st.metric("Overall GPA", stats['overall_gpa'])
        st.metric("Total Credits", stats['total_credits'])

# Main content
if st.session_state['df'] is None:
    # Welcome screen
    st.info("👆 Upload your UNILAG transcript PDF to get started")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📄 Upload")
        st.write("Upload your official UNILAG transcript in PDF format")
    
    with col2:
        st.subheader("🤖 AI Analysis")
        st.write("Get personalized project ideas and career recommendations")
    
    with col3:
        st.subheader("📊 Insights")
        st.write("Visualize your academic performance and trends")
    
    st.markdown("---")
    st.subheader("✨ Features")
    st.write("- 🎯 Personalized final year project ideas")
    st.write("- 💼 Career pathway recommendations")
    st.write("- 📈 Performance analysis and trends")
    st.write("- 🎓 Skill gap identification")
    st.write("- 💡 Actionable study recommendations")

else:
    # Main app with tabs
    df = st.session_state['df']
    student_info = st.session_state['student_info']
    
    # Display student info
    st.subheader("👤 Student Information")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Name", student_info.get('Name', 'N/A'))
    with col2:
        st.metric("Matric No", student_info.get('Matric_No', 'N/A'))
    with col3:
        st.metric("Department", student_info.get('Department', 'N/A'))
    with col4:
        st.metric("Faculty", student_info.get('Faculty', 'N/A'))
    
    st.markdown("---")
    
    # Tabs for different sections
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Performance Overview",
        "🤖 AI Project Ideas", 
        "💼 Career Pathways",
        "📚 Skill Gaps",
        "🎯 Detailed Analysis"
    ])
    
    with tab1:
        st.subheader("📊 Academic Performance Overview")
        
        stats = get_quick_stats(df)
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Courses", stats['total_courses'])
        with col2:
            st.metric("Overall GPA", stats['overall_gpa'])
        with col3:
            st.metric("Total Credits", stats['total_credits'])
        with col4:
            st.metric("Best Grade", stats['best_grade'])
        
        st.markdown("---")
        
        # Grade distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Grade Distribution")
            grade_counts = df['Grade'].value_counts().sort_index()
            fig = px.bar(
                x=grade_counts.index,
                y=grade_counts.values,
                labels={'x': 'Grade', 'y': 'Count'},
                title='Grades Distribution'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("GPA by Year")
            if 'Year' in df.columns and df['Year'].notna().any():
                gpa_by_year = df.groupby('Year')['Grade_Point'].mean().reset_index()
                fig = px.line(
                    gpa_by_year,
                    x='Year',
                    y='Grade_Point',
                    markers=True,
                    title='GPA Progression',
                    labels={'Grade_Point': 'Average GPA', 'Year': 'Year'}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("Year information not available")
        
        # Course table
        st.subheader("All Courses")
        st.dataframe(
            df[['Course_Code', 'Course_Title', 'Credit_Unit', 'Grade', 'Grade_Point', 'Year']],
            use_container_width=True
        )
    
    with tab2:
        st.subheader("AI-Generated Project Ideas")
        
        num_ideas = st.slider("Number of project ideas", 3, 10, 5)
        
        if st.button("Generate Project Ideas", type="primary"):
            with st.spinner("🤖 AI is analyzing your transcript and generating ideas..."):
                try:
                    ideas = generate_project_ideas(df, student_info, num_ideas)
                    st.markdown(ideas)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab3:
        st.subheader("💼 Career Pathway Recommendations")
        
        if st.button("🎯 Generate Career Pathways", type="primary"):
            with st.spinner("🤖 AI is analyzing career options..."):
                try:
                    careers = generate_career_pathways(df, student_info)
                    st.markdown(careers)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab4:
        st.subheader("📚 Skill Gap Analysis")
        
        target_role = st.text_input("Target Role (optional)", placeholder="e.g., Software Engineer, Data Analyst")
        
        if st.button("🔍 Identify Skill Gaps", type="primary"):
            with st.spinner("🤖 AI is analyzing skill gaps..."):
                try:
                    gaps = identify_skill_gaps(df, student_info, target_role if target_role else None)
                    st.markdown(gaps)
                except Exception as e:
                    st.error(f"Error: {e}")
    
    with tab5:
        st.subheader("🎯 Detailed Performance Analysis")
        
        if st.button("📊 Generate Detailed Analysis", type="primary"):
            with st.spinner("🤖 AI is analyzing your performance..."):
                try:
                    analysis = analyze_strengths_weaknesses(df, student_info)
                    st.markdown(analysis)
                except Exception as e:
                    st.error(f"Error: {e}")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #666;'>Built for UNILAG Students 🚀 | "
    "Powered by Cohere AI</p>",
    unsafe_allow_html=True
)