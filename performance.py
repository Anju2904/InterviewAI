# ==========================================
# InterviewAI - Performance Analytics
# Phase 5
# ==========================================


def calculate_statistics(interviews):

    if not interviews:

        return {
            "total": 0,
            "average": 0,
            "best": 0,
            "lowest": 0
        }

    scores = []

    for interview in interviews:

        try:

            score = float(
                interview.get("score", 0)
            )

            scores.append(score)

        except (ValueError, TypeError):

            pass

    if not scores:

        return {
            "total": len(interviews),
            "average": 0,
            "best": 0,
            "lowest": 0
        }

    return {

        "total": len(interviews),

        "average": round(
            sum(scores) / len(scores)
        ),

        "best": round(
            max(scores)
        ),

        "lowest": round(
            min(scores)
        )
    }


# ==========================================
# Skill Performance
# ==========================================

def calculate_skill_performance(interviews):

    skill_scores = {}

    for interview in interviews:

        skills = interview.get(
            "skills",
            {}
        )

        if not isinstance(skills, dict):

            continue

        for skill, score in skills.items():

            try:

                score = float(score)

            except (ValueError, TypeError):

                continue

            if skill not in skill_scores:

                skill_scores[skill] = []

            skill_scores[skill].append(
                score
            )

    result = {}

    for skill, scores in skill_scores.items():

        result[skill] = round(
            sum(scores) / len(scores)
        )

    return result


# ==========================================
# Weak Skills
# ==========================================

def get_weak_skills(
    skill_performance,
    threshold=60
):

    weak_skills = []

    for skill, score in skill_performance.items():

        if score < threshold:

            weak_skills.append({

                "skill": skill,

                "score": score

            })

    weak_skills.sort(
        key=lambda x: x["score"]
    )

    return weak_skills


# ==========================================
# Performance Level
# ==========================================

def get_performance_level(score):

    if score >= 90:

        return "Excellent"

    elif score >= 75:

        return "Strong"

    elif score >= 60:

        return "Good"

    elif score >= 40:

        return "Needs Improvement"

    else:

        return "Needs Significant Practice"