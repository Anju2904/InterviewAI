import json
import ollama


def generate_ai_questions(
    role,
    difficulty="Medium",
    skills=None,
    limit=5
):

    # Only use skills that are relevant to the selected role
    role_skills = {
        "Python Developer": [
            "Python"
        ],

        "Frontend Developer": [
            "HTML",
            "CSS",
            "JavaScript"
        ]
    }

    allowed_skills = role_skills.get(
        role,
        []
    )

    # If skills are provided, keep only allowed skills
    if skills:

        selected_skills = [
            skill
            for skill in skills
            if skill.lower() in [
                x.lower()
                for x in allowed_skills
            ]
        ]

    else:

        selected_skills = allowed_skills

    skills_text = ", ".join(
        selected_skills
    ) if selected_skills else ", ".join(
        allowed_skills
    )

    # ==========================================
    # AI Prompt
    # ==========================================

    prompt = f"""
Generate exactly {limit} unique technical interview questions.

TARGET ROLE: {role}

DIFFICULTY: {difficulty}

ALLOWED TOPICS ONLY:
{skills_text}

IMPORTANT RULES:

1. Every question MUST be related to the target role.
2. Do NOT generate questions from technologies outside the allowed topics.
3. For Python Developer, ask ONLY Python questions.
4. Do NOT ask HTML questions.
5. Do NOT ask CSS questions.
6. Do NOT ask JavaScript questions.
7. Do NOT ask SQL questions.
8. Do NOT ask Pandas questions.
9. Do NOT ask NumPy questions.
10. Do NOT ask Power BI questions.
11. Do NOT ask Flask questions.
12. Generate exactly {limit} questions.
13. Questions must be unique.
14. Questions should be technical and interview-oriented.

Return ONLY valid JSON.

Format:

[
    {{
        "question": "Question here",
        "keywords": ["keyword1", "keyword2", "keyword3"]
    }}
]
"""

    try:

        response = ollama.chat(

            model="llama3.2:3b",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response[
            "message"
        ][
            "content"
        ].strip()

        # Remove markdown
        if content.startswith("```json"):
            content = content[7:].strip()

        if content.startswith("```"):
            content = content[3:].strip()

        if content.endswith("```"):
            content = content[:-3].strip()

        questions = json.loads(content)

        valid_questions = []

        for item in questions:

            if (
                isinstance(item, dict)
                and item.get("question")
            ):

                valid_questions.append({

                    "question": item.get(
                        "question"
                    ),

                    "keywords": item.get(
                        "keywords",
                        []
                    )
                })

        return valid_questions[:limit]

    except Exception as error:

        print(
            "\nAI Question Generation Error:"
        )

        print(error)

        return []