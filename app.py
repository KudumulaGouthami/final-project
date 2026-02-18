



import streamlit as st
import json, os, time, random
from datetime import datetime

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="Smart Quiz App", page_icon="🎯")

# ------------------------------------------------
# SESSION DEFAULTS  (VERY IMPORTANT → prevents errors)
# ------------------------------------------------
defaults = {
    "stage": "home",
    "user": None,
    "quiz": None,
    "page": 0,
    "score": 0,
    "start_time": 0,
    "used_questions": []
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ------------------------------------------------
# FILE HELPERS
# ------------------------------------------------
USER_FILE = "users.json"

def load_users():
    return json.load(open(USER_FILE)) if os.path.exists(USER_FILE) else {}

def save_users(data):
    json.dump(data, open(USER_FILE, "w"), indent=4)

users = load_users()


# ------------------------------------------------
# QUIZ DATA
# ------------------------------------------------
quizzes = {
    "Programming": [
        {"question": "Which keyword creates a function in Python?", "options": ["def","func","lambda","function"], "answer": "def"},
        {"question": "Which company developed Java?", "options": ["Microsoft","Oracle","Sun Microsystems","Google"], "answer": "Sun Microsystems"},
        {"question": "HTML stands for?", "options": ["Hyper Text Markup Language","None","HighText","Hyperlinks"], "answer": "Hyper Text Markup Language"},
        {"question": "CSS stands for?", "options": ["Cascading Style Sheets","Color Sheet","None","Coding Style"], "answer": "Cascading Style Sheets"},
        {"question": "Python comment symbol?", "options": ["#","//","<!-- -->","/* */"], "answer": "#"},
    ]
}


# ------------------------------------------------
# AUTO TIMER (runs every second)
# ------------------------------------------------
st.experimental_autorefresh(interval=1000, key="timer")


# ------------------------------------------------
# HOME PAGE
# ------------------------------------------------
if st.session_state.stage == "home":

    st.title("🎯 Smart Quiz Application")

    username = st.text_input("Enter Username")

    if st.button("Start Quiz"):
        if username == "":
            st.warning("Enter username")
        else:
            st.session_state.user = username
            st.session_state.stage = "quiz"
            st.rerun()

    st.stop()


# ------------------------------------------------
# QUIZ PAGE
# ------------------------------------------------
if st.session_state.stage == "quiz":

    st.sidebar.write(f"👤 {st.session_state.user}")

    if st.sidebar.button("Logout"):
        for k in defaults:
            st.session_state[k] = defaults[k]
        st.rerun()

    category = "Programming"
    questions = quizzes[category]

    # ----------------------------------------
    # START QUIZ
    # ----------------------------------------
    if st.session_state.quiz is None:

        random.shuffle(questions)
        st.session_state.quiz = questions[:5]
        st.session_state.page = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()


    quiz = st.session_state.quiz
    page = st.session_state.page
    total = len(quiz)


    # ----------------------------------------
    # FINISH
    # ----------------------------------------
    if page >= total:

        st.success(f"🎉 Finished! Score: {st.session_state.score}/{total}")

        if st.button("Restart"):
            st.session_state.quiz = None
            st.rerun()

        st.stop()


    # ----------------------------------------
    # TIMER LOGIC (continuous)
    # ----------------------------------------
    total_time = 15
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, total_time - elapsed)

    st.markdown(f"⏳ Time Left: **{remaining} seconds**")

    if remaining == 0:
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()


    # ----------------------------------------
    # QUESTION
    # ----------------------------------------
    q = quiz[page]

    st.subheader(f"Q{page+1}. {q['question']}")

    choice = st.radio("Select answer:", q["options"], key=f"q{page}")

    if st.button("Next"):

        if choice == q["answer"]:
            st.session_state.score += 1

        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()


