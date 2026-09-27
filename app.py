from services.ats_matcher import calculate_match
from services.performance import (
    get_performance_level
)

from services.ai_evaluator import (
    evaluate_answer_with_ai
)

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from database.database import (
    get_db,
    init_db
)

from services.question_engine import (
    get_roles,
    get_questions,
    get_resume_questions
)

from services.ai_question_generator import (
    generate_ai_questions
)

from services.evaluator import (
    evaluate_answer,
    generate_feedback
)

from services.resume_analyzer import (
    analyze_resume
)

import os
import uuid


app = Flask(__name__)

app.secret_key = "INTERVIEW_AI_SECRET_KEY_CHANGE_THIS"

UPLOAD_FOLDER = "uploads"

app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_FOLDER


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

# --------------------------------
# Initialize Database
# --------------------------------

init_db()



# --------------------------------
# Performance Analytics
# --------------------------------

@app.route("/analytics")
def analytics():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    connection = get_db()

    # ======================================
    # Get all interviews
    # ======================================

    interviews = connection.execute(
        """
        SELECT *
        FROM interviews
        WHERE user_id = ?
        ORDER BY id ASC
        """,
        (session["user_id"],)
    ).fetchall()


    # ======================================
    # Basic Statistics
    # ======================================

    total_interviews = len(interviews)

    scores = []

    for interview in interviews:

        try:

            scores.append(
                float(interview["score"])
            )

        except (
            ValueError,
            TypeError
        ):

            pass


    if scores:

        average_score = round(
            sum(scores) / len(scores)
        )

        best_score = round(
            max(scores)
        )

        lowest_score = round(
            min(scores)
        )

    else:

        average_score = 0

        best_score = 0

        lowest_score = 0


    # ======================================
    # Role Performance
    # ======================================

    role_data = {}

    for interview in interviews:

        role = interview["role"]

        try:

            score = float(
                interview["score"]
            )

        except (
            ValueError,
            TypeError
        ):

            continue

        if role not in role_data:

            role_data[role] = []

        role_data[role].append(
            score
        )


    role_performance = {}

    for role, role_scores in role_data.items():

        role_performance[role] = round(
            sum(role_scores) /
            len(role_scores)
        )


    # ======================================
    # Difficulty Performance
    # ======================================

    difficulty_data = {}

    for interview in interviews:

        difficulty = interview["difficulty"]

        try:

            score = float(
                interview["score"]
            )

        except (
            ValueError,
            TypeError
        ):

            continue

        if difficulty not in difficulty_data:

            difficulty_data[difficulty] = []

        difficulty_data[difficulty].append(
            score
        )


    difficulty_performance = {}

    for difficulty, difficulty_scores in difficulty_data.items():

        difficulty_performance[difficulty] = round(
            sum(difficulty_scores) /
            len(difficulty_scores)
        )


    # ======================================
    # Recent Score Trend
    # ======================================

    score_trend = []

    for interview in interviews:

        try:

            score_trend.append(
                float(interview["score"])
            )

        except (
            ValueError,
            TypeError
        ):

            pass


    # ======================================
    # Performance Level
    # ======================================

    performance_level = (
        get_performance_level(
            average_score
        )
    )


    # ======================================
    # Improvement Needed
    # ======================================

    if average_score >= 90:

        improvement_message = (
            "Excellent performance! "
            "You are consistently performing "
            "at a strong interview level."
        )

    elif average_score >= 75:

        improvement_message = (
            "Strong performance. Focus on "
            "your weaker technical areas to "
            "reach the 90% target."
        )

    elif average_score >= 60:

        improvement_message = (
            "Good start. Continue practicing "
            "technical questions and improve "
            "answer accuracy."
        )

    else:

        improvement_message = (
            "More practice is recommended. "
            "Focus on fundamentals and "
            "complete additional mock interviews."
        )


    connection.close()


    return render_template(

        "analytics.html",

        total_interviews=total_interviews,

        average_score=average_score,

        best_score=best_score,

        lowest_score=lowest_score,

        role_performance=role_performance,

        difficulty_performance=difficulty_performance,

        score_trend=score_trend,

        performance_level=performance_level,

        improvement_message=improvement_message
    )

# --------------------------------
# Home
# --------------------------------

@app.route("/")
def index():

    return render_template(
        "index.html"
    )


# --------------------------------
# Register
# --------------------------------

@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register():

    if request.method == "POST":

        name = request.form.get(
            "name",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        confirm_password = request.form.get(
            "confirm_password",
            ""
        )

        if not name or not email or not password:

            flash(
                "All fields are required.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        if len(password) < 6:

            flash(
                "Password must contain at least 6 characters.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        connection = get_db()

        existing_user = connection.execute(
            """
            SELECT id
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        if existing_user:

            connection.close()

            flash(
                "Email already registered.",
                "error"
            )

            return redirect(
                url_for("register")
            )

        password_hash = generate_password_hash(
            password
        )

        connection.execute(
            """
            INSERT INTO users
            (name, email, password)
            VALUES (?, ?, ?)
            """,
            (
                name,
                email,
                password_hash
            )
        )

        connection.commit()
        connection.close()

        flash(
            "Account created successfully.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html"
    )


# --------------------------------
# Login
# --------------------------------

@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    if request.method == "POST":

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        password = request.form.get(
            "password",
            ""
        )

        connection = get_db()

        user = connection.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

        connection.close()

        if user and check_password_hash(
            user["password"],
            password
        ):

            session.clear()

            session["user_id"] = user["id"]
            session["user_name"] = user["name"]

            return redirect(
                url_for("dashboard")
            )

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template(
        "login.html"
    )


# --------------------------------
# Logout
# --------------------------------

@app.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("index")
    )


# --------------------------------
# Dashboard
# --------------------------------

@app.route("/dashboard")
def dashboard():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    connection = get_db()

    interviews = connection.execute(
        """
        SELECT *
        FROM interviews
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    connection.close()

    total_interviews = len(interviews)

    if total_interviews:

        average_score = int(
            sum(
                item["score"]
                for item in interviews
            ) / total_interviews
        )

        best_score = max(
            item["score"]
            for item in interviews
        )

    else:

        average_score = 0
        best_score = 0

    return render_template(
        "dashboard.html",
        interviews=interviews,
        total_interviews=total_interviews,
        average_score=average_score,
        best_score=best_score
    )


# --------------------------------
# Interview Setup
# --------------------------------

@app.route("/setup")
def setup():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "setup.html",
        roles=get_roles()
    )

# --------------------------------
# Start Interview
# --------------------------------

@app.route(
    "/start-interview",
    methods=["POST"]
)
def start_interview():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )


    # ==========================================
    # Get form data
    # ==========================================

    role = request.form.get(
        "role"
    )

    difficulty = request.form.get(
        "difficulty"
    )

    interview_type = request.form.get(
        "interview_type"
    )


    # ==========================================
    # Get resume skills if available
    # ==========================================

    skills = session.get(
        "resume_skills",
        []
    )


    # ==========================================
    # Generate questions using AI
    # ==========================================

    questions = generate_ai_questions(

        role=role,

        difficulty=difficulty,

        skills=None,

        limit=5
    )


    # ==========================================
    # Fallback if Ollama fails
    # ==========================================

    if not questions:
        questions = get_questions(
            role,
            difficulty
        )

    # ==========================================
    # Check questions
    # ==========================================

    if not questions:

        flash(

            "Unable to generate interview questions. Please try again.",

            "error"

        )

        return redirect(
            url_for("setup")
        )


    # ==========================================
    # Save interview information
    # ==========================================

    session["role"] = role

    session["difficulty"] = difficulty

    session["interview_type"] = interview_type

    session["questions"] = questions

    # IMPORTANT
    # Start from question 0
    session["current_question"] = 0

    # Store answers separately
    session["interview_answers"] = []

    return redirect(
        url_for("interview")
    )

# --------------------------------
# Interview
# --------------------------------

@app.route("/interview")
def interview():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    questions = session.get(
        "questions"
    )

    current_question = session.get(
        "current_question",
        0
    )

    if not questions:

        return redirect(
            url_for("setup")
        )

   # If all questions are completed
    if current_question >= len(questions):

        return redirect(
            url_for("result")
        )

    question = questions[current_question]

    return render_template(
        "interview.html",

        question=question,

        question_number=current_question + 1,

        total_questions=len(questions),

        role=session.get("role"),

        difficulty=session.get("difficulty")
    ) 

@app.route(
    "/evaluate-answer",
    methods=["POST"]
)
def evaluate_answer_route():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    questions = session.get(
        "questions",
        []
    )

    current_question = session.get(
        "current_question",
        0
    )

    if not questions:

        return redirect(
            url_for("setup")
        )
    
    # Safety check
    if current_question >= len(questions):

        return redirect(
            url_for("result")
        )

    question_data = questions[current_question]

    answer = request.form.get(
        "answer",
        ""
    ).strip()

    # Save answer
    answers = session.get(
        "interview_answers",
        []
    )

    answers.append({
        "question": question_data["question"],
        "answer": answer,
        "keywords": question_data.get(
            "keywords",
            []
        )
    })

    session["interview_answers"] = answers

    # Move to next question
    session["current_question"] = (
        current_question + 1
    )

    # If all questions completed
    if session["current_question"] >= len(questions):
        return redirect(
            url_for("submit_interview")
        )

    # Otherwise show next question
    return redirect(
        url_for("interview")
    )

# --------------------------------
# Submit Interview
# --------------------------------

@app.route(
    "/submit-interview",
    methods=["GET", "POST"]
)
def submit_interview():

    if "user_id" not in session:
        return redirect(
            url_for("login")
        )

    questions = session.get(
        "questions",
        []
    )

    answers = session.get(
        "interview_answers",
        []
    )

    if not questions:
        return redirect(
            url_for("setup")
        )

    # Make sure all questions were answered
    if len(answers) < len(questions):
        return redirect(
            url_for("interview")
        )

    results = []
    total_score = 0

    # ==========================================
    # Evaluate each answer
    # ==========================================

    for question_data, answer_data in zip(
        questions,
        answers
    ):

        question = question_data["question"]

        answer = answer_data["answer"]

        keywords = question_data.get(
            "keywords",
            []
        )

        # ======================================
        # AI Evaluation
        # ======================================

        ai_result = evaluate_answer_with_ai(
            question=question,
            answer=answer,
            keywords=keywords,
            difficulty=session.get(
                "difficulty",
                "Medium"
            )
        )

        print("AI RESULT:", ai_result)

        # ======================================
        # AI result
        # ======================================

        if ai_result is not None:

            score = ai_result.get(
                "score",
                0
            )

            strengths = ai_result.get(
                "strengths",
                []
            )

            weaknesses = ai_result.get(
                "weaknesses",
                []
            )

            feedback = ai_result.get(
                "feedback",
                ""
            )

        # ======================================
        # Fallback evaluation
        # ======================================

        else:

            fallback_result = evaluate_answer(
                answer,
                keywords
            )

            score = fallback_result.get(
                "score",
                0
            )

            matched_keywords = fallback_result.get(
                "matched_keywords",
                []
            )

            strengths = fallback_result.get(
                "strengths",
                []
            )

            weaknesses = fallback_result.get(
                "improvements",
                []
            )

            feedback = (
                "Your answer was evaluated "
                "using keyword matching."
            )

        # Make sure score is numeric
        try:
            score = float(score)
        except (
            ValueError,
            TypeError
        ):
            score = 0

        total_score += score

        # ======================================
        # Save result
        # ======================================

        results.append({

            "question": question,

            "answer": answer,

            "score": round(score),

            "strengths": strengths,

            "weaknesses": weaknesses,

            "feedback": feedback

        })

    # ==========================================
    # Final score
    # ==========================================

    if questions:

        final_score = int(
            total_score / len(questions)
        )

    else:

        final_score = 0

    # ==========================================
    # Save interview
    # ==========================================

    connection = get_db()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO interviews
        (
            user_id,
            role,
            difficulty,
            interview_type,
            score,
            total_questions
        )
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            session["user_id"],
            session["role"],
            session["difficulty"],
            session["interview_type"],
            final_score,
            len(questions)
        )
    )

    interview_id = cursor.lastrowid

    # ==========================================
    # Save answers
    # ==========================================

    for result in results:

        cursor.execute(
            """
            INSERT INTO answers
            (
                interview_id,
                question,
                answer,
                score
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                interview_id,
                result["question"],
                result["answer"],
                result["score"]
            )
        )

    connection.commit()

    connection.close()

    # ==========================================
    # Generate overall feedback
    # ==========================================

    feedback = generate_feedback(
        final_score
    )

    # ==========================================
    # Store result in session
    # ==========================================

    session["last_result"] = {

        "score": final_score,

        "feedback": feedback,

        "results": results,

        "role": session.get(
            "role",
            ""
        ),

        "difficulty": session.get(
            "difficulty",
            ""
        )

    }

    # ==========================================
    # Clear current interview
    # ==========================================

    session.pop(
        "questions",
        None
    )

    session.pop(
        "current_question",
        None
    )

    session.pop(
        "interview_answers",
        None
    )

    return redirect(
        url_for("result")
    )

    

# --------------------------------
# Result
# --------------------------------

@app.route("/result")
def result():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    result = session.get(
        "last_result"
    )

    if not result:

        return redirect(
            url_for("dashboard")
        )

    return render_template(
        "result.html",
        **result
    )

    # ==========================================
# Phase 6 - Detailed Interview Report
# ==========================================

@app.route("/interview-report/<int:interview_id>")
def interview_report(interview_id):

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    connection = get_db()

    # ======================================
    # Get Interview
    # ======================================

    interview = connection.execute(
        """
        SELECT *
        FROM interviews
        WHERE id = ?
        AND user_id = ?
        """,
        (
            interview_id,
            session["user_id"]
        )
    ).fetchone()


    if not interview:

        connection.close()

        flash(
            "Interview report not found.",
            "error"
        )

        return redirect(
            url_for("history")
        )


    # ======================================
    # Get Answers
    # ======================================

    answers = connection.execute(
        """
        SELECT *
        FROM answers
        WHERE interview_id = ?
        ORDER BY id ASC
        """,
        (interview_id,)
    ).fetchall()


    connection.close()


    # ======================================
    # Calculate Report Statistics
    # ======================================

    total_answers = len(answers)

    answer_scores = []

    for answer in answers:

        try:

            answer_scores.append(
                float(answer["score"])
            )

        except (
            ValueError,
            TypeError
        ):

            pass


    if answer_scores:

        average_answer_score = round(
            sum(answer_scores)
            / len(answer_scores)
        )

        highest_answer_score = round(
            max(answer_scores)
        )

        lowest_answer_score = round(
            min(answer_scores)
        )

    else:

        average_answer_score = 0

        highest_answer_score = 0

        lowest_answer_score = 0


    # ======================================
    # Performance Summary
    # ======================================

    if interview["score"] >= 90:

        performance_message = (
            "Excellent interview performance. "
            "Your answers demonstrate strong "
            "technical understanding."
        )

    elif interview["score"] >= 75:

        performance_message = (
            "Strong performance. Your fundamentals "
            "are good, but there is still room to "
            "improve technical depth."
        )

    elif interview["score"] >= 60:

        performance_message = (
            "Average performance. Focus on improving "
            "technical concepts and explaining your "
            "answers more clearly."
        )

    else:

        performance_message = (
            "More preparation is recommended. "
            "Review the fundamentals and practice "
            "technical interview questions."
        )


    return render_template(

        "interview_report.html",

        interview=interview,

        answers=answers,

        total_answers=total_answers,

        average_answer_score=average_answer_score,

        highest_answer_score=highest_answer_score,

        lowest_answer_score=lowest_answer_score,

        performance_message=performance_message
    )


# --------------------------------
# History
# --------------------------------

@app.route("/history")
def history():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    connection = get_db()

    interviews = connection.execute(
        """
        SELECT *
        FROM interviews
        WHERE user_id = ?
        ORDER BY id DESC
        """,
        (session["user_id"],)
    ).fetchall()

    # ======================================
    # Calculate Statistics
    # ======================================

    total_interviews = len(interviews)

    scores = []

    for interview in interviews:

        try:

            score = float(
                interview["score"]
            )

            scores.append(score)

        except (
            ValueError,
            TypeError
        ):

            pass


    if scores:

        average_score = round(
            sum(scores) / len(scores)
        )

        best_score = round(
            max(scores)
        )

    else:

        average_score = 0

        best_score = 0


    connection.close()


    return render_template(
        "history.html",

        interviews=interviews,

        total_interviews=total_interviews,

        average_score=average_score,

        best_score=best_score
    )


# --------------------------------
# Resume Analyzer
# --------------------------------

@app.route(
    "/resume",
    methods=["GET", "POST"]
)
def resume():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    analysis = None

    if request.method == "POST":

        file = request.files.get(
            "resume"
        )

        if not file:

            flash(
                "Please select a resume.",
                "error"
            )

            return redirect(
                url_for("resume")
            )

        if file.filename == "":

            flash(
                "Please select a resume.",
                "error"
            )

            return redirect(
                url_for("resume")
            )

        if not file.filename.lower().endswith(
            ".pdf"
        ):

            flash(
                "Only PDF resumes are supported.",
                "error"
            )

            return redirect(
                url_for("resume")
            )

        unique_name = (
            str(uuid.uuid4())
            + ".pdf"
        )

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            unique_name
        )

        file.save(
            file_path
        )

        analysis = analyze_resume(
            file_path
        )

        # Save detected skills
        session["resume_skills"] = (
            analysis["skills"]
        )

        # Save complete resume text
        session["resume_text"] = (
            analysis.get("text", "")
        )

        # Mark resume as uploaded
        session["resume_uploaded"] = True

        # Remove uploaded file
        try:

            os.remove(
                file_path
            )

        except Exception:

            pass

    return render_template(
        "resume.html",
        analysis=analysis
    )



# --------------------------------
# Resume Based Interview
# --------------------------------

@app.route("/resume-interview")
def resume_interview():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    skills = session.get(
        "resume_skills",
        []
    )

    if not skills:

        flash(
            "Please upload your resume first.",
            "error"
        )

        return redirect(
            url_for("resume")
        )

    role = "Python Developer"

    questions = get_resume_questions(
        role,
        skills,
        limit=8
    )

    if not questions:

        flash(
            "No questions found for the skills detected in your resume.",
            "error"
        )

        return redirect(
            url_for("resume")
        )

    session["questions"] = questions

    session["current_question"] = 0

    session["interview_answers"] = []

    session["role"] = role

    session["difficulty"] = "Resume Based"

    session["interview_type"] = "Resume Based"

    return redirect(
      url_for("interview")
) 


@app.route("/ats-matcher")
def ats_matcher():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    return render_template(
        "ats_match.html"
    )

@app.route(
    "/analyze-ats",
    methods=["POST"]
)
def analyze_ats():

    if "user_id" not in session:

        return redirect(
            url_for("login")
        )

    resume_text = session.get(
        "resume_text",
        ""
    )

    job_description = request.form.get(
        "job_description",
        ""
    )

    if not resume_text:

        flash(
            "Please upload your resume first.",
            "error"
        )

        return redirect(
            url_for("resume")
        )

    if not job_description.strip():

        flash(
            "Please enter a job description.",
            "error"
        )

        return redirect(
            url_for("ats_matcher")
        )

    result = calculate_match(
        resume_text,
        job_description
    )

    return render_template(
        "ats_result.html",
        result=result
    )


# --------------------------------
# Run
# --------------------------------

if __name__ == "__main__":

    app.run(
        debug=True
    )