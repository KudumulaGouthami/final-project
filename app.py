import streamlit as st
import time
import random

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Quiz App", page_icon="🧠", layout="centered")

# -------------------- STYLE --------------------
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #f0f9ff, #cbebff);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px 24px;
            border-radius: 10px;
            border: none;
        }
        .stButton>button:hover {
            background-color: #43a047;
            color: white;
        }
        .title {
            text-align: center;
            color: #1e3d59;
        }
        .score {
            text-align: center;
            font-size: 22px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- QUIZ DATA --------------------
quiz_data = {
    "General Knowledge": [
        {"question": "What is the capital of India?", "options": ["Mumbai", "New Delhi", "Kolkata", "Hyderabad"], "answer": "New Delhi"},
        {"question": "Which is the largest ocean?", "options": ["Atlantic", "Pacific", "Indian", "Arctic"], "answer": "Pacific"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
    ],
    "Python": [
        {"question": "Who developed Python?", "options": ["Guido van Rossum", "Dennis Ritchie", "Elon Musk", "James Gosling"], "answer": "Guido van Rossum"},
        {"question": "What symbol is used to comment in Python?", "options": ["//", "#", "/* */", "<!-- -->"], "answer": "#"},
        {"question": "Which function is used to display text?", "options": ["echo()", "print()", "write()", "display()"], "answer": "print()"},
    ]
}

# -------------------- SESSION VARIABLES --------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "category" not in st.session_state:
    st.session_state.category = None
if "question_index" not in st.session_state:
    st.session_state.question_index = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "timer_start" not in st.session_state:
    st.session_state.timer_start = None

# -------------------- FUNCTIONS --------------------
def start_quiz(category):
    st.session_state.category = category
    st.session_state.page = "quiz"
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.timer_start = time.time()

def reset_quiz():
    st.session_state.page = "home"
    st.session_state.category = None
    st.session_state.question_index = 0
    st.session_state.score = 0
    st.session_state.timer_start = None

def next_question(selected):
    category = st.session_state.category
    questions = quiz_data[category]
    correct = questions[st.session_state.question_index]["answer"]

    if selected == correct:
        st.session_state.score += 1

    st.session_state.question_index += 1
    st.session_state.timer_start = time.time()

    if st.session_state.question_index >= len(questions):
        st.session_state.page = "result"

# -------------------- TIMER --------------------
def get_time_left():
    total_time = 20  # seconds per question
    elapsed = int(time.time() - st.session_state.timer_start)
    remaining = total_time - elapsed
    return max(0, remaining)

# -------------------- HOME PAGE --------------------
if st.session_state.page == "home":
    st.markdown("<h1 class='title'>🧠 Welcome to the Smart Quiz App</h1>", unsafe_allow_html=True)
    st.image("https://cdn.pixabay.com/photo/2016/11/29/02/24/question-mark-1869046_960_720.jpg", use_container_width=True)
    category = st.selectbox("Choose a quiz category:", list(quiz_data.keys()))
    if st.button("🚀 Start Quiz"):
        start_quiz(category)

# -------------------- QUIZ PAGE --------------------
elif st.session_state.page == "quiz":
    category = st.session_state.category
    questions = quiz_data[category]
    q = questions[st.session_state.question_index]

    st.markdown(f"### {category} Quiz")
    st.progress((st.session_state.question_index + 1) / len(questions))

    remaining = get_time_left()
    st.info(f"⏱️ Time left: {remaining} seconds")

    if remaining <= 0:
        st.warning("⏰ Time’s up! Moving to next question...")
        next_question(None)
        st.experimental_rerun()

    st.markdown(f"**Question {st.session_state.question_index + 1}:** {q['question']}")
    selected = st.radio("Select your answer:", q["options"], index=None)

    if st.button("Next"):
        if selected:
            next_question(selected)
            st.experimental_rerun()
        else:
            st.warning("Please select an answer first!")

# -------------------- RESULT PAGE --------------------
elif st.session_state.page == "result":
    total = len(quiz_data[st.session_state.category])
    st.markdown("<h2 class='title'>🏁 Quiz Completed!</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='score'>Your Final Score: {st.session_state.score} / {total}</p>", unsafe_allow_html=True)

    if st.button("🔁 Play Again"):
        reset_quiz()
