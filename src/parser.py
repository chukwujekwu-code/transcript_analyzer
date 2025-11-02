import pdfplumber
import pandas as pd
import re
from typing import Tuple, Dict

def parse_transcript(pdf_path: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Parse transcript pdf and extract content

    args:
        pdf_path: Path to the transcript

    returns:
        Tuple of student records
    """
    with pdfplumber.open(pdf_path) as pdf:
        # Combine all pages
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

        student_info = {
            "Name": re.search(r"NAME:\s*(.+)", text),
            "Matric_No": re.search(r"MATRIC NO:\s*(.+)", text),
            "Faculty": re.search(r"FACULTY:\s*(.+)", text),
            "Department": re.search(r"DEPARTMENT:\s*(.+)", text),
            "Sex": re.search(r"SEX:/s*(.+)", text),
            "DOB": re.search(r"DATE OF BIRTH:\s*(.+)", text),
            "Year_of_Award": re.search(r"YEAR OF AWARD:\s*(.+)", text)  
        }

        student_info = {k: v.group(1).strip() if v else None for k, v in student_info.items()}

        # parse courses with proper tracking
        courses = []
        current_session = None
        current_year = None

        # Split into lines to track context
        lines = text.split("\n")
        for line in lines:
            session_match = re.search(r"SESSION:(\d{4}/\d{4}).*YEAR:\s*(\d+)", line)
            if session_match:
                current_session = session_match.group(1)
                current_year = int(session_match.group(2))
                continue

            course_match = re.search(r"([A-Z]{3}\d{3})\s+(.+?)\s+(\d+)\s+([A-F][+-]?)\s+([\d.]+)", line)
            if course_match:
                courses.append({
                    "Name": student_info["Name"],
                    "Matric_No": student_info['Matric_No'],
                    "Session": current_session,
                    "Year": current_year,
                    "Course_Code": course_match.group(1),
                    "Course_Title": course_match.group(2).strip(),
                    "Credit_Unit": int(course_match.group(3)),
                    "Grade": course_match.group(4),
                    "Grade_Point": float(course_match.group(5))
                })

        # Create Dataframe
        df = pd.DataFrame(courses)
        df['Credit_Value'] = df['Credit_Unit'] * df['Grade_Point']

        return df, student_info
    
def get_quick_stats(df: pd.DataFrame) -> Dict:

    stats = {
        "total_courses": len(df),
        "total_credits": df["Credit_Unit"].sum(),
        "overall_gpa": round(df["Credit_Value"].sum() / df["Credit_Unit"].sum(), 2),
        "courses_by_year": df['Year'].value_counts().sort_index().to_dict(),
        "avg_gpa_by_year": df.groupby("Year")["Grade_Point"].mean().round(2).to_dict(),
        "best_grade": df["Grade_Point"].max(),
        "worst_grade": df["Grade_Point"].min()
    }
    return stats
        

if __name__ == "__main__":
    pdf_path = "data/SUNDAY CHUKWUJEKWU ANAH- Transcript"
    try:
        df, info = parse_transcript(pdf_path)

        print("Student Info")
        for k, v in info.items():
            print(f"{k}: {v}")

               
        print(df.head(10))
    except FileNotFoundError:
        print("file not found")
