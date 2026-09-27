import re
from PyPDF2 import PdfReader


# -----------------------------------------
# Skills Database
# -----------------------------------------

SKILLS = {

    "Python": [
        "python",
        "python programming"
    ],

    "JavaScript": [
        "javascript",
        "js"
    ],

    "HTML": [
        "html",
        "html5"
    ],

    "CSS": [
        "css",
        "css3"
    ],

    "SQL": [
        "sql",
        "mysql",
        "postgresql",
        "oracle",
        "sql server"
    ],

    "Flask": [
        "flask"
    ],

    "Django": [
        "django"
    ],

    "Streamlit": [
        "streamlit"
    ],

    "Pandas": [
        "pandas"
    ],

    "NumPy": [
        "numpy"
    ],

    "Matplotlib": [
        "matplotlib"
    ],

    "Power BI": [
        "power bi",
        "powerbi"
    ],

    "Tableau": [
        "tableau"
    ],

    "Git": [
        "git",
        "github"
    ],

    "REST API": [
        "rest api",
        "restful api",
        "api"
    ],

    "OOP": [
        "object oriented programming",
        "oop",
        "object-oriented programming"
    ],

    "Machine Learning": [
        "machine learning",
        "machine-learning",
        "ml"
    ],

    "React": [
        "react",
        "reactjs",
        "react.js"
    ],

    "Java": [
        "java"
    ],

    "C++": [
        "c++"
    ],

    "C": [
        "c programming"
    ]
}


# -----------------------------------------
# Extract PDF Text
# -----------------------------------------

def extract_pdf_text(file_path):

    text = ""

    try:

        reader = PdfReader(file_path)

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

    except Exception as error:

        print("PDF extraction error:", error)

    return text


# -----------------------------------------
# Clean Text
# -----------------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text


# -----------------------------------------
# Detect Skills
# -----------------------------------------

def extract_skills(text):

    cleaned_text = clean_text(text)

    detected_skills = []

    for skill, variations in SKILLS.items():

        for variation in variations:

            pattern = r"\b" + re.escape(
                variation.lower()
            ) + r"\b"

            if re.search(
                pattern,
                cleaned_text
            ):

                detected_skills.append(skill)

                break

    return sorted(
        list(set(detected_skills))
    )


# -----------------------------------------
# Skill Match Percentage
# -----------------------------------------

def calculate_skill_score(skills):

    total_skills = len(SKILLS)

    if total_skills == 0:

        return 0

    score = (
        len(skills) /
        total_skills
    ) * 100

    return round(score)


# -----------------------------------------
# Generate Profile
# -----------------------------------------

def analyze_resume(file_path):

    text = extract_pdf_text(
        file_path
    )

    skills = extract_skills(
        text
    )

    skill_score = calculate_skill_score(
        skills
    )

    return {

        "text": text,

        "skills": skills,

        "skill_score": skill_score,

        "word_count": len(
            text.split()
        )

    }