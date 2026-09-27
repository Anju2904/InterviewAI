# ==========================================
# InterviewAI - Answer Evaluation Engine
# Phase 3
# ==========================================

import re


# ==========================================
# Text Cleaning
# ==========================================

def clean_text(text):

    if not text:
        return ""

    text = text.lower()

    # Remove special characters
    text = re.sub(
        r"[^a-zA-Z0-9\s]",
        " ",
        text
    )

    # Remove extra spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# ==========================================
# Keyword Matching
# ==========================================

def calculate_keyword_score(
    answer,
    keywords
):

    if not keywords:
        return 100

    cleaned_answer = clean_text(
        answer
    )

    matched_keywords = []

    for keyword in keywords:

        keyword_clean = clean_text(
            keyword
        )

        if keyword_clean in cleaned_answer:

            matched_keywords.append(
                keyword
            )

    score = (
        len(matched_keywords)
        / len(keywords)
    ) * 100

    return round(score), matched_keywords


# ==========================================
# Answer Length Score
# ==========================================

def calculate_completeness_score(
    answer
):

    words = clean_text(
        answer
    ).split()

    word_count = len(words)

    if word_count == 0:

        return 0

    if word_count < 10:

        return 30

    elif word_count < 25:

        return 55

    elif word_count < 50:

        return 75

    elif word_count < 100:

        return 90

    else:

        return 100


# ==========================================
# Relevance Score
# ==========================================

def calculate_relevance_score(
    answer,
    keywords
):

    if not answer.strip():

        return 0

    cleaned_answer = clean_text(
        answer
    )

    words = cleaned_answer.split()

    if not words:

        return 0

    matched = 0

    for keyword in keywords:

        keyword_clean = clean_text(
            keyword
        )

        if keyword_clean in cleaned_answer:

            matched += 1

    if len(keywords) == 0:

        return 70

    keyword_ratio = (
        matched / len(keywords)
    )

    # Base relevance score

    score = 40 + (
        keyword_ratio * 60
    )

    return round(
        min(score, 100)
    )


# ==========================================
# Generate Strengths
# ==========================================

def generate_strengths(
    keyword_score,
    completeness_score,
    matched_keywords,
    answer
):

    strengths = []

    if keyword_score >= 80:

        strengths.append(
            "Excellent coverage of important technical concepts."
        )

    elif keyword_score >= 60:

        strengths.append(
            "Good coverage of the main technical concepts."
        )

    elif keyword_score >= 40:

        strengths.append(
            "You mentioned some relevant technical concepts."
        )

    if completeness_score >= 80:

        strengths.append(
            "Your answer provides sufficient explanation."
        )

    elif completeness_score >= 60:

        strengths.append(
            "Your answer contains a reasonable amount of detail."
        )

    if len(matched_keywords) >= 3:

        strengths.append(
            "Good use of relevant technical terminology."
        )

    if answer and len(answer.split()) >= 25:

        strengths.append(
            "The answer is reasonably detailed."
        )

    if not strengths:

        strengths.append(
            "You attempted the question and provided a relevant response."
        )

    return strengths


# ==========================================
# Generate Improvements
# ==========================================

def generate_improvements(
    keyword_score,
    completeness_score,
    keywords,
    matched_keywords,
    answer
):

    improvements = []

    missing_keywords = [
        keyword
        for keyword in keywords
        if keyword not in matched_keywords
    ]

    if keyword_score < 70:

        if missing_keywords:

            missing_text = ", ".join(
                missing_keywords[:4]
            )

            improvements.append(
                "Consider explaining these concepts: "
                + missing_text
                + "."
            )

        else:

            improvements.append(
                "Include more technical concepts related to the question."
            )

    if completeness_score < 60:

        improvements.append(
            "Provide a more detailed explanation instead of a very short answer."
        )

    if completeness_score < 80:

        improvements.append(
            "Add a practical example to demonstrate your understanding."
        )

    if answer:

        if "example" not in clean_text(answer):

            improvements.append(
                "Adding a real-world or coding example would strengthen the answer."
            )

    if not improvements:

        improvements.append(
            "Excellent answer. Try adding a practical example to make it even stronger."
        )

    return improvements


# ==========================================
# Final Evaluation
# ==========================================

def evaluate_answer(
    answer,
    keywords
):

    answer = (answer or "").strip()

    # ==========================================
    # Empty answer
    # ==========================================

    if not answer:

        return {

            "score": 0,

            "keyword_score": 0,

            "relevance_score": 0,

            "completeness_score": 0,

            "structure_score": 0,

            "matched_keywords": [],

            "strengths": [],

            "improvements": [
                "No answer was provided."
            ],

            "performance": "Weak"
        }

    # ==========================================
    # Detect meaningless answers
    # ==========================================

    letters = [
        char.lower()
        for char in answer
        if char.isalpha()
    ]

    unique_letters = set(
        letters
    )

    words = answer.split()

    # Very short answer
    if len(answer) < 4:

        return {

            "score": 0,

            "keyword_score": 0,

            "relevance_score": 0,

            "completeness_score": 0,

            "structure_score": 0,

            "matched_keywords": [],

            "strengths": [],

            "improvements": [
                "Answer is too short and does not demonstrate understanding."
            ],

            "performance": "Weak"
        }

    # ==========================================
    # Detect keyboard-smash / gibberish
    # ==========================================

    if len(letters) >= 5:

        vowel_count = sum(
            1
            for char in letters
            if char in "aeiou"
        )

        vowel_ratio = (
            vowel_count / len(letters)
        )

        if (
            len(unique_letters) <= 2
            or vowel_ratio < 0.08
        ):

            return {

                "score": 0,

                "keyword_score": 0,

                "relevance_score": 0,

                "completeness_score": 0,

                "structure_score": 0,

                "matched_keywords": [],

                "strengths": [],

                "improvements": [
                    "The answer appears to be meaningless or unrelated to the question."
                ],

                "performance": "Weak"
            }

    # ==========================================
    # Keyword matching
    # ==========================================

    answer_lower = answer.lower()

    matched_keywords = []

    for keyword in keywords:

        if keyword.lower() in answer_lower:

            matched_keywords.append(
                keyword
            )

    if keywords:

        keyword_score = (
            len(matched_keywords)
            / len(keywords)
        ) * 100

    else:

        keyword_score = 0

    # ==========================================
    # Completeness
    # ==========================================

    word_count = len(words)

    if word_count < 5:

        completeness_score = 20

    elif word_count < 15:

        completeness_score = 50

    elif word_count < 30:

        completeness_score = 75

    else:

        completeness_score = 90

    # ==========================================
    # Relevance
    # ==========================================

    if matched_keywords:

        relevance_score = min(
            100,
            len(matched_keywords)
            / max(len(keywords), 1)
            * 100
        )

    else:

        relevance_score = 0

    # ==========================================
    # Structure
    # ==========================================

    if word_count < 5:

        structure_score = 20

    elif word_count < 15:

        structure_score = 50

    elif word_count < 30:

        structure_score = 75

    else:

        structure_score = 90

    # ==========================================
    # Final Score
    # ==========================================

    final_score = (

        keyword_score * 0.40

        + relevance_score * 0.30

        + completeness_score * 0.20

        + structure_score * 0.10

    )

    final_score = round(
        final_score
    )

    # ==========================================
    # Performance
    # ==========================================

    if final_score >= 90:

        performance = "Excellent"

    elif final_score >= 75:

        performance = "Very Good"

    elif final_score >= 60:

        performance = "Good"

    elif final_score >= 40:

        performance = "Needs Improvement"

    else:

        performance = "Weak"

    # ==========================================
    # Strengths
    # ==========================================

    strengths = []

    if matched_keywords:

        strengths.append(
            "Matched keywords: "
            + ", ".join(
                matched_keywords
            )
        )

    # ==========================================
    # Improvements
    # ==========================================

    improvements = []

    if not matched_keywords:

        improvements.append(
            "Answer does not contain important concepts related to the question."
        )

    if word_count < 15:

        improvements.append(
            "Provide a more detailed explanation."
        )

    return {

        "score": final_score,

        "keyword_score": round(
            keyword_score
        ),

        "relevance_score": round(
            relevance_score
        ),

        "completeness_score": round(
            completeness_score
        ),

        "structure_score": round(
            structure_score
        ),

        "matched_keywords": matched_keywords,

        "strengths": strengths,

        "improvements": improvements,

        "performance": performance
    }

# ==========================================
# Overall Interview Evaluation
# ==========================================

def generate_feedback(score):

    if score >= 90:
        return (
            "Excellent performance! "
            "Your answers demonstrate strong "
            "technical knowledge and good understanding."
        )

    elif score >= 75:
        return (
            "Very good performance. "
            "Your answers show good technical understanding, "
            "but you can improve your depth and clarity."
        )

    elif score >= 60:
        return (
            "Good performance. "
            "You have a basic understanding, but "
            "you should practice explaining technical concepts "
            "more accurately."
        )

    elif score >= 40:
        return (
            "Needs improvement. "
            "Some answers lack technical accuracy or relevant details. "
            "Focus on understanding the concepts and practice more."
        )

    else:
        return (
            "Weak performance. "
            "Your answers did not contain enough relevant technical information. "
            "Review the fundamentals and practice interview questions."
        )