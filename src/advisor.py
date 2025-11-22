from __future__ import annotations
import os
import cohere
import pandas as pd
from typing import Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_cohere_client():
    """Initialize Cohere client."""
    api_key = os.getenv('COHERE_API_KEY')
    if not api_key:
        raise ValueError(
            "COHERE_API_KEY not found in .env file.\n"
            "Get a free API key at: https://dashboard.cohere.com"
        )
    return cohere.Client(api_key)


def generate_project_ideas(df: pd.DataFrame, student_info: Dict, num_ideas: int = 5) -> str:
    """
    Generate personalized final year project ideas based on transcript.
    
    Args:
        df: DataFrame with course information
        student_info: Dictionary with student details
        num_ideas: Number of project ideas to generate
        
    Returns:
        String with AI-generated project ideas
    """
    co = get_cohere_client()
    
    # Analyze student's strengths
    strong_courses = df[df['Grade_Point'] >= 4.0]['Course_Title'].tolist()
    weak_courses = df[df['Grade_Point'] < 3.0]['Course_Title'].tolist()
    
    # Get subject areas (first 3 letters of course code)
    df_copy = df.copy()
    df_copy['Subject_Area'] = df_copy['Course_Code'].str[:3]
    strong_subjects = df_copy[df_copy['Grade_Point'] >= 4.0].groupby('Subject_Area').size().sort_values(ascending=False).head(3).index.tolist()
    
    # Calculate GPA
    overall_gpa = round(df['Credit_Value'].sum() / df['Credit_Unit'].sum(), 2)
    
    department = student_info.get('Department', 'Unknown')
    
    prompt = f"""You are an experienced academic advisor at University of Lagos (UNILAG), Nigeria.

STUDENT PROFILE:
- Department: {department}
- Overall GPA: {overall_gpa}/5.0
- Strong subject areas: {', '.join(strong_subjects)}
- Excellent performance in: {', '.join(strong_courses[:5])}
- Struggled with: {', '.join(weak_courses[:3]) if weak_courses else 'No major challenges'}
- Total courses completed: {len(df)}

TASK:
Generate {num_ideas} final year project ideas that:
1. Leverage their demonstrated strengths and high-performing courses
2. Are realistic for their skill level and GPA
3. Address real problems in Nigeria/Africa
4. Can be completed in 6-9 months
5. Have practical industry applications

For each project idea, provide:
- **Project Title**: Clear and specific
- **Description**: 2-3 sentences explaining what the project does
- **Why It Fits**: How it matches their strengths
- **Skills Developed**: Key technical skills they'll learn
- **Impact**: Real-world applications in Nigeria

Format as a numbered list with clear headings."""

    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0.7,
    )
    
    return response.text


def generate_career_pathways(df: pd.DataFrame, student_info: Dict) -> str:
    """
    Generate personalized career pathway recommendations.
    
    Args:
        df: DataFrame with course information
        student_info: Dictionary with student details
        
    Returns:
        String with career recommendations
    """
    co = get_cohere_client()
    
    # Analyze academic profile
    df_copy = df.copy()
    df_copy['Subject_Area'] = df_copy['Course_Code'].str[:3]
    strong_areas = df_copy[df_copy['Grade_Point'] >= 4.0].groupby('Subject_Area').size().sort_values(ascending=False).head(3).index.tolist()
    
    overall_gpa = round(df['Credit_Value'].sum() / df['Credit_Unit'].sum(), 2)
    department = student_info.get('Department', 'Unknown')
    
    prompt = f"""You are a career counselor specializing in Nigerian tech and engineering careers.

STUDENT PROFILE:
- Department: {department}
- GPA: {overall_gpa}/5.0
- Strong subject areas: {', '.join(strong_areas)}
- Courses completed: {len(df)}

TASK:
Suggest 3 career pathways that:
1. Match their academic strengths
2. Are in-demand in Nigeria's job market
3. Offer good growth potential
4. Include salary expectations

For each career path, provide:
- **Career Title**
- **Why It's a Good Fit**: Based on their transcript
- **Entry-Level Roles**: Specific job titles to apply for
- **Companies in Nigeria**: Real companies hiring (banks, tech firms, oil & gas, etc.)
- **Skills to Develop**: What they should learn now
- **Salary Range**: Expected starting salary in Nigeria (in Naira)
- **3-Year Progression**: How the career grows

Be specific about Nigerian companies like Andela, Flutterwave, Interswitch, banks, oil companies, etc."""

    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0.7,
    )
    
    return response.text


def identify_skill_gaps(
    df: pd.DataFrame,
    student_info: Dict,
    target_role: str | None = None,
) -> str:
    """
    Identify skill gaps and provide learning recommendations.
    
    Args:
        df: DataFrame with course information
        student_info: Dictionary with student details
        target_role: Optional specific career role to target
        
    Returns:
        String with skill gap analysis
    """
    co = get_cohere_client()
    
    department = student_info.get('Department', 'Unknown')
    overall_gpa = round(df['Credit_Value'].sum() / df['Credit_Unit'].sum(), 2)
    
    # Weak areas
    df_copy = df.copy()
    df_copy['Subject_Area'] = df_copy['Course_Code'].str[:3]
    weak_areas = df_copy[df_copy['Grade_Point'] < 3.0].groupby('Subject_Area').size().sort_values(ascending=False).head(3).index.tolist()
    
    role_text = f"for a {target_role} role" if target_role else "for the Nigerian job market"
    
    prompt = f"""You are a skills development coach for Nigerian graduates.

STUDENT PROFILE:
- Department: {department}
- GPA: {overall_gpa}/5.0
- Areas needing improvement: {', '.join(weak_areas) if weak_areas else 'None - strong overall'}
- Total courses: {len(df)}

TASK:
Analyze skill gaps {role_text} and provide actionable learning plan.

Provide:

**1. TECHNICAL SKILLS GAP**
- What's missing from their coursework for the job market
- Priority: High/Medium/Low for each

**2. SOFT SKILLS TO DEVELOP**
- Communication, teamwork, leadership, etc.
- Why each matters

**3. LEARNING ROADMAP**
- **Online Courses**: Specific Coursera/Udemy courses (with links if possible)
- **Certifications**: Worth pursuing (AWS, Google, Microsoft, etc.)
- **Books**: Must-read books
- **Projects**: Practical projects to build

**4. TIMELINE**
- **Next 3 Months**: Immediate priorities
- **Next 6 Months**: Medium-term goals
- **Next 12 Months**: Long-term development

Be specific and actionable for a Nigerian graduate looking for jobs."""

    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0.7,
    )
    
    return response.text


def analyze_strengths_weaknesses(df: pd.DataFrame, student_info: Dict) -> str:
    """
    Detailed analysis of academic strengths and weaknesses.
    
    Args:
        df: DataFrame with course information
        student_info: Dictionary with student details
        
    Returns:
        String with detailed analysis
    """
    co = get_cohere_client()
    
    # Prepare data
    overall_gpa = round(df['Credit_Value'].sum() / df['Credit_Unit'].sum(), 2)
    best_courses = df.nlargest(5, 'Grade_Point')[['Course_Title', 'Grade']].to_dict('records')
    worst_courses = df.nsmallest(5, 'Grade_Point')[['Course_Title', 'Grade']].to_dict('records')
    
    gpa_by_year = df.groupby('Year')['Grade_Point'].mean().round(2).to_dict()
    
    department = student_info.get('Department', 'Unknown')
    
    prompt = f"""You are an academic performance analyst for UNILAG students.

STUDENT PROFILE:
- Department: {department}
- Overall GPA: {overall_gpa}/5.0
- Best courses: {best_courses}
- Most challenging courses: {worst_courses}
- GPA by year: {gpa_by_year}

TASK:
Provide detailed academic analysis covering:

**1. OVERALL ASSESSMENT**
- Performance level (Excellent/Good/Fair/Needs Improvement)
- Key observations

**2. STRENGTHS**
- What they excel at
- Patterns in high-performing courses
- Natural aptitudes

**3. AREAS FOR IMPROVEMENT**
- Consistent weak areas
- Possible reasons for challenges
- Not just criticism - constructive insights

**4. PROGRESSION ANALYSIS**
- How performance changed over the years
- Improvement trends or decline
- Final year readiness

**5. ACTIONABLE RECOMMENDATIONS**
- Study strategies
- Focus areas
- How to leverage strengths

Be honest but encouraging. Tone should be supportive and motivating."""

    response = co.chat(
        model="command-a-03-2025",
        message=prompt,
        temperature=0.7,
    )
    
    return response.text