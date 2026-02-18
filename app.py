



    import streamlit as st
import json
import os
import time
import random
from datetime import datetime


# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Quiz Application", page_icon="🎯", layout="centered")


# ---------------- FILES ----------------
USER_FILE = "users.json"
LEADER_FILE = "leaderboard.json"


# ---------------- HELPERS ----------------
def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}


def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


users = load_data(USER_FILE)
leaderboard = load_data(LEADER_FILE)


# ---------------- SESSION DEFAULTS ----------------
defaults = {
    "stage": "welcome",
    "user": None,
    "quiz": None,
    "page": 0,
    "score": 0,
    "start_time": 0
}

for k in defaults:
    if k not in st.session_state:
        st.session_state[k] = defaults[k]


# ---------------- QUIZ QUESTIONS ----------------
quizzes = {
    "Programming": [
        {"question": "Python comment symbol?", "options": ["#", "//", "/* */", "--"], "answer": "#"},
        {"question": "HTML stands for?", "options": ["Hyper Text Markup Language", "None", "HighText ML", "Hyper Tool ML"], "answer": "Hyper Text Markup Language"},
        {"question": "CSS stands for?", "options": ["Cascading Style Sheets", "Coding Style System", "None", "Color Style"], "answer": "Cascading Style Sheets"},
        {"question": "Keyword to create function?", "options": ["def", "func", "lambda", "class"], "answer": "def"},
        {"question": "Java developed by?", "options": ["Microsoft", "Google", "Sun Microsystems", "IBM"], "answer": "Sun Microsystems"}
    ],
    "Maths": [
        {"question": "12 × 8 = ?", "options": ["96", "88", "108", "80"], "answer": "96"},
        {"question": "√144 = ?", "options": ["12", "10", "14", "16"], "answer": "12"},
        {"question": "15% of 200 = ?", "options": ["30", "40", "20", "25"], "answer": "30"},
        {"question": "10 + 5 × 2 = ?", "options": ["20", "30", "25", "15"], "answer": "20"},
        {"question": "50 ÷ 5 = ?", "options": ["10", "5", "8", "12"], "answer": "10"}
    ]
}


# ---------------- FUNCTIONS ----------------
def register_user(u, p):
    if u in users:
        return False
    users[u] = {"password": p, "scores": []}
    save_data(USER_FILE, users)
    return True


def login_user(u, p):
    return u in users and users[u]["password"] == p


# =================================================
# WELCOME PAGE
# =================================================
if st.session_state.stage == "welcome":
    st.title("🎯 Quiz Application")
    if st.button("Register"):
        st.session_state.stage = "register"
        st.rerun()
    if st.button("Login"):
        st.session_state.stage = "login"
        st.rerun()
    st.stop()


# =================================================
# REGISTER
# =================================================
if st.session_state.stage == "register":
    st.header("Register")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Create"):
        if register_user(u, p):
            st.success("Registered successfully")
            st.session_state.stage = "login"
            st.rerun()
        else:
            st.error("Username exists")

    st.stop()


# =================================================
# LOGIN
# =================================================
if st.session_state.stage == "login":
    st.header("Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(u, p):
            st.session_state.user = u
            st.session_state.stage = "quiz"
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()


# =================================================
# QUIZ
# =================================================
if st.session_state.stage == "quiz":

    # START QUIZ
    if st.session_state.quiz is None:
        cat = st.selectbox("Category", list(quizzes.keys()))

        if st.button("Start Quiz"):
            qlist = quizzes[cat][:]
            random.shuffle(qlist)   # ✅ shuffle every attempt
            st.session_state.quiz = qlist
            st.session_state.page = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.rerun()

        st.stop()

    quiz = st.session_state.quiz
    page = st.session_state.page

    # CONTINUOUS TIMER
    total_time = 15
    remaining = total_time - int(time.time() - st.session_state.start_time)

    st.write(f"Time left: {max(0, remaining)} sec")

    time.sleep(1)
    st.rerun()

    if remaining <= 0:
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()

    if page >= len(quiz):
        st.session_state.stage = "result"
        st.rerun()

    q = quiz[page]
    st.subheader(q["question"])

    ans = st.radio("Choose:", q["options"])

    if st.button("Next"):
        if ans == q["answer"]:
            st.session_state.score += 1
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()


# =================================================
# RESULT
# =================================================
if st.session_state.stage == "result":
    st.success(f"Score: {st.session_state.score}/{len(st.session_state.quiz)}")

    if st.button("Play Again"):
        st.session_state.quiz = None
        st.session_state.stage = "quiz"
        st.rerun()
