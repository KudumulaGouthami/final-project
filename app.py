



import streamlit as st
import time
import random

# ------------------ PAGE SETUP ------------------
st.set_page_config(page_title="Quiz App", page_icon="🎯")

# ------------------ QUESTION BANK ------------------
questions_bank = [
    {"q": "Python is developed by?", "options": ["James", "Guido van Rossum", "Dennis", "Bjarne"], "ans": "Guido van Rossum"},
    {"q": "2 + 5 =", "options": ["5", "6", "7", "8"], "ans": "7"},
    {"q": "HTML stands for?", "options": ["Hyper Text Markup Language", "High Text Machine", "Home Tool", "None"], "ans": "Hyper Text Markup Language"},
    {"q": "CSS is used for?", "options": ["Logic", "Database", "Styling", "Backend"], "ans": "Styling"},
    {"q": "5 × 6 =", "options": ["25", "30", "35", "40"], "ans": "30"},
    {"q": "Sun rises in?", "options": ["West", "North", "East", "South"], "ans": "East"},
    {"q": "Which is a loop?", "options": ["if", "for", "print", "def"], "ans": "for"}
]

# ------------------ SESSION INIT ------------------
if "quiz" not in st.session_state:
    st.session_state.quiz = random.sample(questions_bank, len(questions_bank))
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()

# ------------------ FUNCTIONS ------------------
def restart_quiz():
    st.session_state.quiz = random.sample(questions_bank, len(questions_bank))  # shuffle
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()
    st.rerun()

# ------------------ TITLE ------------------
st.title("🎯 Smart Quiz Application")

# ------------------ FINISH SCREEN ------------------
if st.session_state.index >= len(st.session_state.quiz):
    st.success(f"✅ Quiz Completed!\n\nScore: {st.session_state.score}/{len(st.session_state.quiz)}")

    if st.button("🔁 Restart Quiz"):
        restart_quiz()

    st.stop()

# ------------------ CURRENT QUESTION ------------------
question = st.session_state.quiz[st.session_state.index]

st.subheader(f"Question {st.session_state.index + 1}")
st.write(question["q"])

# ------------------ TIMER ------------------
TOTAL_TIME = 15

elapsed = int(time.time() - st.session_state.start_time)
remaining = max(0, TOTAL_TIME - elapsed)

timer_placeholder = st.empty()
timer_placeholder.markdown(f"⏳ Time Left: **{remaining} seconds**")

# auto refresh every second
time.sleep(1)
st.rerun()

# ------------------ TIME UP ------------------
if remaining == 0:
    st.warning("⏰ Time Up!")
    st.session_state.index += 1
    st.session_state.start_time = time.time()
    st.rerun()

# ------------------ OPTIONS ------------------
choice = st.radio("Choose answer:", question["options"], key=f"q{st.session_state.index}")

if st.button("Next"):
    if choice == question["ans"]:
        st.session_state.score += 1

    st.session_state.index += 1
    st.session_state.start_time = time.time()
    st.rerun()
