from services.ai_evaluator import (
    evaluate_answer_with_ai
)


question = (
    "What is Object-Oriented Programming "
    "in Python?"
)


answer = """
Object-Oriented Programming is a programming
approach where we create classes and objects.

It supports concepts like encapsulation,
inheritance, polymorphism and abstraction.
"""


keywords = [

    "class",
    "object",
    "encapsulation",
    "inheritance",
    "polymorphism"

]


result = evaluate_answer_with_ai(

    question=question,

    answer=answer,

    keywords=keywords,

    difficulty="Medium"

)


print()

print("AI Evaluation:")

print(result)