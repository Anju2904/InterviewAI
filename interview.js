let currentQuestion = 0;

const questions = document.querySelectorAll(
    ".question-screen"
);

const progressBar =
    document.getElementById("progressBar");


function showQuestion(index) {

    questions.forEach(
        question => {
            question.style.display = "none";
        }
    );

    if (questions[index]) {

        questions[index].style.display =
            "block";

        currentQuestion = index;

        updateProgress();

    }
}


function nextQuestion() {

    if (currentQuestion <
        questions.length - 1) {

        currentQuestion++;

        showQuestion(
            currentQuestion
        );

    }
}


function previousQuestion() {

    if (currentQuestion > 0) {

        currentQuestion--;

        showQuestion(
            currentQuestion
        );

    }
}


function updateProgress() {

    const percentage =
        ((currentQuestion + 1) /
        questions.length) * 100;

    if (progressBar) {

        progressBar.style.width =
            percentage + "%";

    }
}


/* Timer */

let timeRemaining = 600;

const timer =
    document.getElementById("timer");


function updateTimer() {

    let minutes =
        Math.floor(timeRemaining / 60);

    let seconds =
        timeRemaining % 60;

    seconds =
        seconds < 10
            ? "0" + seconds
            : seconds;

    if (timer) {

        timer.textContent =
            `${minutes}:${seconds}`;

    }

    if (timeRemaining <= 0) {

        document
            .getElementById("interviewForm")
            .submit();

    }

    timeRemaining--;

}


if (timer) {

    setInterval(
        updateTimer,
        1000
    );

}


showQuestion(0);