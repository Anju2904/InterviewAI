from services.ai_question_generator import (
    generate_ai_questions
)


questions = generate_ai_questions(

    role="Python Developer",

    difficulty="Medium",

    skills=[
        "Python",
        "SQL",
        "Flask",
        "Pandas",
        "NumPy"
    ],

    limit=5
)


for index, question in enumerate(
    questions,
    start=1
):

    print()

    print(
        f"Question {index}:"
    )

    print(
        question["question"]
    )

    print(
        "Keywords:",
        question["keywords"]
    )

    print(
        "-" * 50
    )