



       import streamlit as st
import json, os, time, random
from datetime import datetime
import streamlit.components.v1 as components

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Quiz App", page_icon="🎯", layout="centered")

# ---------------- DATA FILES ----------------
USER_FILE = "users.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_data(file):
    return json.load(open(file)) if os.path.exists(file) else {}

def save_data(file, data):
    json.dump(data, open(file, "w"), indent=4)

users = load_data(USER_FILE)
leaderboard = load_data(LEADERBOARD_FILE)

# ---------------- QUIZ BANK ----------------
quizzes = {
    "Programming": [
        {"question": "Which company developed Java?", "options": ["Microsoft","Oracle","Sun Microsystems","Google"], "answer": "Sun Microsystems"},
        {"question": "Which symbol is used for comments in Python?", "options": ["#","//","/* */","<!-- -->"], "answer": "#"},
        {"question": "HTML stands for?", "options": ["Hyper Text Markup Language","HighText Machine Language","Hyperlinks and Text Markup Language","None"], "answer": "Hyper Text Markup Language"},
        {"question": "CSS stands for?", "options": ["Cascading Style Sheets","Color Style Syntax","Coding Style System","Central Sheet Style"], "answer": "Cascading Style Sheets"},
        {"question": "Which keyword is used to create a function in Python?", "options": ["def","func","lambda","function"], "answer": "def"}
    ]
}

# ---------------- SESSION SETUP ----------------
if "quiz" not in st.session_state:

    cat = st.selectbox("Category", list(quizzes.keys()))

    if st.button("Start Quiz ▶"):

        selected = random.sample(quizzes[cat], len(quizzes[cat]))

        # ✅ ADDED → shuffle questions every attempt
        random.shuffle(selected)

        st.session_state.quiz = selected
        st.session_state.page = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()

        st.rerun()

    st.stop()


quiz = st.session_state.quiz
page = st.session_state.page
total = len(quiz)

# ---------------- TIMER ----------------
total_time = 20
elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, total_time - elapsed)

st.write(f"⏳ Time Left: {remaining} seconds")

# ✅ ADDED → continuous running timer
time.sleep(1)
st.rerun()

# ---------------- TIME OVER ----------------
if remaining <= 0:
    st.session_state.page += 1
    st.session_state.start_time = time.time()
    st.rerun()

# ---------------- FINISH ----------------
if page >= total:
    st.success(f"Score: {st.session_state.score}/{total}")

    if st.button("Restart"):
        del st.session_state.quiz
        st.rerun()

    st.stop()

# ---------------- QUESTION ----------------
q = quiz[page]

st.write(f"### Q{page+1}. {q['question']}")

choice = st.radio("Choose:", q["options"])

if st.button("Next ➡"):

    if choice == q["answer"]:
        st.session_state.score += 1

    st.session_state.page += 1
    st.session_state.start_time = time.time()

    st.rerun()
