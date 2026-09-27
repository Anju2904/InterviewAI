import json
import ollama


def evaluate_answer_with_ai(
    question,
    answer,
    keywords,
    difficulty="Medium"
):

    # ==========================================
    # Basic validation
    # ==========================================

    answer = (answer or "").strip()

    if not answer:
        return {
            "score": 0,
            "strengths": [],
            "weaknesses": [
                "No answer was provided."
            ],
            "feedback": "Please provide an answer."
        }

    # ==========================================
    # AI Prompt
    # ==========================================

    prompt = f"""
You are a strict technical interview evaluator.

Evaluate the candidate's answer based on the QUESTION.

Question:
{question}

Candidate Answer:
{answer}

Expected Keywords:
{", ".join(keywords)}

Difficulty:
{difficulty}

IMPORTANT EVALUATION RULES:

1. Evaluate the actual meaning of the answer.
2. Do NOT give points simply because the answer is long.
3. Do NOT give points simply because the answer contains many words.
4. Check whether the answer is relevant to the question.
5. Check whether the answer demonstrates technical understanding.
6. Detect meaningless, random, gibberish, or keyboard-smash answers.
7. Answers such as "mmmm", "abc", "nhmjjjnmnkj", "hello", or random characters
   without technical meaning must receive 0.
8. If the answer is completely irrelevant, score it 0.
9. If the answer is partially correct, give an appropriate partial score.
10. A correct and technically detailed answer should receive a high score.
11. Do not assume that a long answer is a good answer.
12. Judge correctness, relevance, clarity and technical depth.

Scoring:

0-20   = Completely incorrect, meaningless, or irrelevant
21-40  = Very weak understanding
41-60  = Partially correct
61-75  = Good answer
76-90  = Very good answer
91-100 = Excellent technical answer

Return ONLY valid JSON.

Use exactly this format:

{{
    "score": 0,
    "strengths": [],
    "weaknesses": [],
    "feedback": ""
}}
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

        # ==========================================
        # Remove Markdown JSON
        # ==========================================

        if content.startswith("```json"):

            content = content[
                7:
            ].strip()

        elif content.startswith("```"):

            content = content[
                3:
            ].strip()

        if content.endswith("```"):

            content = content[
                :-3
            ].strip()

        # ==========================================
        # Convert JSON
        # ==========================================

        result = json.loads(
            content
        )

        # ==========================================
        # Validate score
        # ==========================================

        score = result.get(
            "score",
            0
        )

        try:

            score = int(score)

        except (
            ValueError,
            TypeError
        ):

            score = 0

        score = max(
            0,
            min(
                100,
                score
            )
        )

        return {

            "score": score,

            "strengths": result.get(
                "strengths",
                []
            ),

            "weaknesses": result.get(
                "weaknesses",
                []
            ),

            "feedback": result.get(
                "feedback",
                ""
            )
        }

    except Exception as error:

        print(
            "AI Evaluation Error:",
            error
        )

        return None