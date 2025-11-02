from src.parser import parse_transcript
from src.advisor import generate_project_ideas, generate_career_pathways

df, info = parse_transcript()

print("Project Ideas")
print(generate_project_ideas(df, info))

print("Career Pathways")
print(generate_career_pathways(df, info))