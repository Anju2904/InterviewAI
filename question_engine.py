# ==========================================
# InterviewAI - Question Engine
# ==========================================

QUESTIONS = {

    "Python Developer": {

        "Python": [
            {
                "question": "Explain Object-Oriented Programming in Python.",
                "keywords": [
                    "class", "object", "inheritance",
                    "encapsulation", "polymorphism"
                ]
            },
            {
                "question": "Explain exception handling in Python.",
                "keywords": [
                    "try", "except", "finally",
                    "exception", "error"
                ]
            },
            {
                "question": "What are Python decorators?",
                "keywords": [
                    "function", "wrapper",
                    "decorator", "modify"
                ]
            },
            {
                "question": "Explain generators and the yield keyword.",
                "keywords": [
                    "generator", "yield",
                    "iterator", "memory"
                ]
            },
            {
                "question": "What is the difference between a list and a tuple in Python?",
                "keywords": [
                    "list", "tuple",
                    "mutable", "immutable"
                ]
            }
        ],

        "SQL": [
            {
                "question": "What is the difference between INNER JOIN and LEFT JOIN?",
                "keywords": [
                    "join", "inner", "left",
                    "table", "matching"
                ]
            },
            {
                "question": "What is database normalization?",
                "keywords": [
                    "normalization", "database",
                    "redundancy", "tables"
                ]
            }
        ],

        "Flask": [
            {
                "question": "What is Flask and why would you use it?",
                "keywords": [
                    "python", "web",
                    "framework", "application"
                ]
            },
            {
                "question": "Explain routing in Flask.",
                "keywords": [
                    "route", "url",
                    "flask", "request"
                ]
            }
        ],

        "HTML": [
            {
                "question": "What are semantic HTML elements?",
                "keywords": [
                    "semantic", "header",
                    "footer", "section",
                    "article"
                ]
            },
            {
        "question": "What are semantic HTML elements and why are they important?",
        "keywords": [
            "semantic",
            "header",
            "footer",
            "section",
            "article"
        ]
    },

    {
        "question": "What is the difference between HTML id and class attributes?",
        "keywords": [
            "id",
            "class",
            "unique",
            "element"
        ]
    }
        ],

        "CSS": [
            {
                "question": "Explain CSS Flexbox and Grid.",
                "keywords": [
                    "flexbox", "grid",
                    "layout", "container"
                ]
            },
            {
        "question": "Explain CSS Flexbox and when you would use it.",
        "keywords": [
            "flexbox",
            "container",
            "flex",
            "layout"
        ]
    },

    {
        "question": "What is the CSS box model?",
        "keywords": [
            "margin",
            "border",
            "padding",
            "content"
        ]
    }
            
        ],

        "JavaScript": [
            {
                "question": "Explain let, const and var in JavaScript.",
                "keywords": [
                    "let", "const",
                    "var", "scope"
                ]
            },
            {
                "question": "What is the DOM?",
                "keywords": [
                    "document", "object",
                    "model", "html",
                    "elements"
                ]
            }
        ],

        "Pandas": [
            {
                "question": "What is Pandas and what is a DataFrame?",
                "keywords": [
                    "pandas", "dataframe",
                    "data", "analysis"
                ]
            }
        ],

        "NumPy": [
            {
                "question": "Why is NumPy used in Python?",
                "keywords": [
                    "numpy", "array",
                    "numerical", "calculation"
                ]
            }
        ],

        "Power BI": [
            {
                "question": "What is Power BI and how is it used?",
                "keywords": [
                    "power", "bi",
                    "dashboard",
                    "visualization",
                    "data"
                ]
            }
        ]
    },

    "Frontend Developer": {

        "HTML": [
            {
                "question": "What are semantic HTML elements?",
                "keywords": [
                    "semantic", "header",
                    "footer", "section",
                    "article"
                ]
            }
        ],

        "CSS": [
            {
                "question": "Explain CSS Flexbox and Grid.",
                "keywords": [
                    "flexbox", "grid",
                    "layout", "container"
                ]
            }
        ],

        "JavaScript": [
            {
                "question": "Explain let, const and var in JavaScript.",
                "keywords": [
                    "let", "const",
                    "var", "scope"
                ]
            },
            {
                "question": "What is the DOM?",
                "keywords": [
                    "document", "object",
                    "model", "html",
                    "elements"
                ]
            }
        ]
    }
}


# ==========================================
# Get Available Roles
# ==========================================

def get_roles():

    return list(QUESTIONS.keys())


# ==========================================
# Get Questions for a Role
# ==========================================

def get_questions(role, difficulty=None):

    role_questions = QUESTIONS.get(
        role,
        {}
    )

    # Python Developer -> Python only
    if role == "Python Developer":

        return role_questions.get(
            "Python",
            []
        )

    # Frontend Developer -> HTML + CSS + JavaScript
    if role == "Frontend Developer":

        questions = []

        for skill in [
            "HTML",
            "CSS",
            "JavaScript"
        ]:

            questions.extend(
                role_questions.get(
                    skill,
                    []
                )
            )

        return questions

    return []


# ==========================================
# Get Questions by Skill
# ==========================================

def get_skill_questions(role, skill):

    role_questions = QUESTIONS.get(
        role,
        {}
    )

    return role_questions.get(
        skill,
        []
    )


# ==========================================
# Resume-Based Questions
# ==========================================

def get_resume_questions(
    role,
    skills,
    limit=8
):

    role_questions = QUESTIONS.get(
        role,
        {}
    )

    questions = []

    # Normalize resume skills
    resume_skills = [
        skill.strip().lower()
        for skill in skills
    ]

    # ------------------------------------------------
    # Get questions ONLY for skills detected
    # in the candidate's resume
    # ------------------------------------------------

    for skill_name, skill_questions in role_questions.items():

        if skill_name.lower() in resume_skills:

            for question in skill_questions:

                if question not in questions:

                    questions.append(
                        question
                    )

    # ------------------------------------------------
    # Limit number of questions
    # ------------------------------------------------

    return questions[:limit]