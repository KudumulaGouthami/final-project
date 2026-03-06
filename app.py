




  import streamlit as st
import random
import time

st.set_page_config(page_title="Quiz Application", page_icon="🧠")

st.title("🧠 Online Quiz Application")

# ---------------- QUIZ DATA ---------------- #

quizzes = {
    "Python": [
        {"q": "What is the extension of Python file?", "options": [".py", ".java", ".html", ".cpp"], "answer": ".py"},
        {"q": "Which keyword is used to define a function?", "options": ["function", "define", "def", "fun"], "answer": "def"},
        {"q": "Python is a ____ language.", "options": ["Low level", "High level", "Machine", "Assembly"], "answer": "High level"},
        {"q": "Which symbol is used for comments?", "options": ["#", "//", "/*", "--"], "answer": "#"},
        {"q": "Which data type is used for numbers?", "options": ["int", "str", "bool", "list"], "answer": "int"}
    ],

    "Java": [
        {"q": "Java is a ___ language.", "options": ["Compiled", "Interpreted", "Both", "None"], "answer": "Both"},
        {"q": "Which keyword is used to create a class?", "options": ["class", "Class", "create", "define"], "answer": "class"},
        {"q": "Java was developed by?", "options": ["Microsoft", "Sun Microsystems", "Google", "IBM"], "answer": "Sun Microsystems"},
        {"q": "Which method is entry point of Java?", "options": ["start()", "main()", "run()", "init()"], "answer": "main()"},
        {"q": "Java is ___ independent.", "options": ["Platform", "Machine", "Device", "None"], "answer": "Platform"}
    ],

    "HTML": [
        {"q": "HTML stands for?", "options": ["Hyper Text Markup Language", "High Text Machine Language", "Hyperlink Text Markup Language", "None"], "answer": "Hyper Text Markup Language"},
        {"q": "Which tag is used for heading?", "options": ["<h1>", "<p>", "<a>", "<div>"], "answer": "<h1>"},
        {"q": "Which tag is used for paragraph?", "options": ["<p>", "<h1>", "<div>", "<span>"], "answer": "<p>"},
        {"q": "HTML files end with?", "options": [".html", ".ht", ".h", ".web"], "answer": ".html"},
        {"q": "Which tag creates hyperlink?", "options": ["<a>", "<link>", "<href>", "<url>"], "answer": "<a>"}
    ]
}

# ---------------- SESSION VARIABLES ---------------- #

if "quiz" not in st.session_state:
    st.session_state.quiz = None
    st.session_state.page = 0
    st.session_state.score = 0
    st.session_state.start_time = None
    st.session_state.cat = None


# ---------------- HOME PAGE ---------------- #

if st.session_state.quiz is None:

    st.subheader("Select Quiz Category")

    cat = st.selectbox("Choose Subject", list(quizzes.keys()))
    num_q = st.slider("Number of Questions", 1, len(quizzes[cat]), 3)

    if st.button("Start Quiz ▶️"):

        questions = quizzes[cat].copy()
        random.shuffle(questions)   # shuffle questions every attempt
        selected = questions[:num_q]

        st.session_state.quiz = selected
        st.session_state.page = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.cat = cat

        st.rerun()


# ---------------- QUIZ PAGE ---------------- #

else:

    quiz = st.session_state.quiz
    page = st.session_state.page

    if page < len(quiz):

        q = quiz[page]

        st.subheader(f"Question {page+1}")

        answer = st.radio(q["q"], q["options"], key=page)

        if st.button("Next ➡️"):

            if answer == q["answer"]:
                st.session_state.score += 1

            st.session_state.page += 1
            st.rerun()

    else:

        st.success("Quiz Completed 🎉")

        score = st.session_state.score
        total = len(quiz)

        st.write(f"### Your Score: {score} / {total}")

        if st.button("Restart Quiz 🔄"):

            st.session_state.quiz = None
            st.session_state.page = 0
            st.session_state.score = 0

            st.rerun()


# ---------------- FOOTER ---------------- #

st.markdown("---")
st.write("Developed using Streamlit")


