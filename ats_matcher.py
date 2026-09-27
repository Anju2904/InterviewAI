# ==========================================
# InterviewAI - ATS Resume Matcher
# Phase 4
# ==========================================

import re


# ==========================================
# Supported Technical Skills
# ==========================================

SKILLS = [

    "Python",
    "Java",
    "C++",
    "C",
    "JavaScript",
    "HTML",
    "CSS",

    "Flask",
    "Django",
    "React",
    "Node.js",

    "SQL",
    "MySQL",
    "PostgreSQL",
    "MongoDB",
    "SQLite",

    "Pandas",
    "NumPy",
    "Matplotlib",

    "Power BI",
    "Tableau",

    "Git",
    "GitHub",

    "REST API",
    "API",

    "OOP",
    "Object Oriented Programming",

    "Machine Learning",
    "Data Analysis",

    "Excel",

    "AWS",
    "Azure",

]


# ==========================================
# Clean Text
# ==========================================

def clean_text(text):

    if not text:

        return ""

    text = text.lower()

    text = re.sub(
        r"[^a-zA-Z0-9+#.\s]",
        " ",
        text
    )

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================
# Extract Skills
# ==========================================

def extract_skills(text):

    cleaned_text = clean_text(
        text
    )

    detected_skills = []

    for skill in SKILLS:

        skill_clean = clean_text(
            skill
        )

        if skill_clean in cleaned_text:

            if skill not in detected_skills:

                detected_skills.append(
                    skill
                )

    return detected_skills


# ==========================================
# Compare Resume and Job Description
# ==========================================

def calculate_match(
    resume_text,
    job_description
):

    resume_skills = extract_skills(
        resume_text
    )

    job_skills = extract_skills(
        job_description
    )

    resume_skill_lower = {
        skill.lower(): skill
        for skill in resume_skills
    }

    matched_skills = []

    missing_skills = []

    for skill in job_skills:

        if skill.lower() in resume_skill_lower:

            matched_skills.append(
                skill
            )

        else:

            missing_skills.append(
                skill
            )

    # ======================================
    # Calculate ATS Score
    # ======================================

    if len(job_skills) == 0:

        match_score = 0

    else:

        match_score = (
            len(matched_skills)
            / len(job_skills)
        ) * 100

    match_score = round(
        match_score
    )

    # ======================================
    # Performance
    # ======================================

    if match_score >= 90:

        performance = "Excellent Match"

    elif match_score >= 75:

        performance = "Strong Match"

    elif match_score >= 60:

        performance = "Good Match"

    elif match_score >= 40:

        performance = "Partial Match"

    else:

        performance = "Low Match"

    # ======================================
    # Recommendations
    # ======================================

    recommendations = []

    if missing_skills:

        for skill in missing_skills[:5]:

            recommendations.append(
                "Consider adding or improving "
                + skill
                + " experience."
            )

    else:

        recommendations.append(
            "Your resume covers all detected technical skills."
        )

    if match_score < 60:

        recommendations.append(
            "Consider tailoring your resume "
            "more closely to the job description."
        )

    elif match_score < 80:

        recommendations.append(
            "Your resume is a reasonable match, "
            "but adding missing skills could improve it."
        )

    else:

        recommendations.append(
            "Your resume is well aligned with this job description."
        )

    return {

        "score": match_score,

        "performance": performance,

        "resume_skills": resume_skills,

        "job_skills": job_skills,

        "matched_skills": matched_skills,

        "missing_skills": missing_skills,

        "recommendations": recommendations

    }