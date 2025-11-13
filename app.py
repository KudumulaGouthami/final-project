import streamlit as st
import time
import random

# ---------------------- PAGE CONFIG ----------------------
st.set_page_config(page_title="Quiz Application", page_icon="🧠", layout="centered")

# ---------------------- CUSTOM CSS ----------------------
st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #e3ffe7, #d9e7ff);
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px 24px;
            border-radius: 10px;
        }
        .stButton>button:hover {
            background-color: #45a049;
            color: white;
        }
        .title {
            text-align: center;
            color: #1f4e79;
        }
        .score {
            text-align: center;
            font-size: 22px;
            color: #333;
        }
        .timer {
            font-size: 20px;
            text-align: right;
            color: red;
            font-weight: bold;
        }
        .feedback {
            text-align: center;
            font-size: 20px;
            color: #4A148C;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------------- QUIZ DATA ----------------------
quiz_data = {
    "General": [
        {"question": "What is the capital of India?", "options": ["Hyderabad", "Mumbai", "New Delhi", "Kolkata"], "answer": "New Delhi"},
        {"question": "Who wrote the Indian National Anthem?", "options": ["Rabindranath Tagore", "Gandhi", "Nehru", "Sarojini Naidu"], "answer": "Rabindranath Tagore"},
    ],
    "Science": [
        {"question": "What planet is known as the Red Planet?", "options": ["Mars", "Jupiter", "Earth", "Venus"], "answer": "Mars"},
        {"question": "Water freezes at what temperature (Celsius)?", "options": ["0", "100", "-10", "50"], "answer": "0"},
    ],
    "Technology": [
        {"question": "Which language is used for AI?", "options": ["Python", "C", "HTML", "SQL"], "answer": "Python"},
        {"question": "HTML stands for?", "options": ["Hyper Text Markup Language", "High Transfer Markup Language", "Home Tool Markup Language", "Hyperlink and Text Markup Language"], "answer": "Hyper Text Markup Language"},
    ]
}

# ---------------------- SESSION STATE ----------------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "category" not in st.session_state:
    st.session_state.category = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "current_q" not in st.session_state:
    st.session_state.current_q = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "leaderboard" not in st.session_state:
    st.session_state.leaderboard = []
if "player_name" not in st.session_state:
    st.session_state.player_name = ""

# ---------------------- FUNCTIONS ----------------------
def start_quiz():
    st.session_state.page = "quiz"
    st.session_state.questions = quiz_data[st.session_state.category]
    random.shuffle(st.session_state.questions)
    st.session_state.current_q = 0
    st.session_state.score = 0
    st.session_state.start_time = time.time()

def next_question(selected):
    q = st.session_state.questions[st.session_state.current_q]
    if selected == q["answer"]:
        st.session_state.score += 1

    st.session_state.current_q += 1
    st.session_state.start_time = time.time()  # reset timer

    if st.session_state.current_q >= len(st.session_state.questions):
        st.session_state.page = "result"
        st.session_state.leaderboard.append({
            "name": st.session_state.get("player_name", "Player"),
            "score": st.session_state.score
        })

def restart_quiz():
    st.session_state.page = "home"
    st.session_state.category = None
    st.session_state.current_q = 0
    st.session_state.score = 0

# ---------------------- FEEDBACK ----------------------
def get_feedback(score, total):
    percentage = (score / total) * 100
    if percentage == 100:
        return "🌟 Excellent! Perfect Score!"
    elif percentage >= 75:
        return "👏 Great Job! You did really well!"
    elif percentage >= 50:
        return "🙂 Nice Try! Keep improving!"
    else:
        return "💪 Don’t give up! Practice makes perfect!"

# ---------------------- HOME PAGE ----------------------
if st.session_state.page == "home":
    st.markdown("<h1 class='title'>🧠 Welcome to the Ultimate Quiz Challenge!</h1>", unsafe_allow_html=True)
    st.image("https://cdn.pixabay.com/photo/2016/11/29/02/24/question-mark-1869046_960_720.jpg", use_container_width=True)

    st.session_state.player_name = st.text_input("Enter your name:", "")
    st.session_state.category = st.selectbox("Select a Category:", ["General", "Science", "Technology"])

    if st.session_state.player_name and st.button("🚀 Start Quiz"):
        start_quiz()

    if st.session_state.leaderboard:
        st.markdown("### 🏆 Leaderboard")
        sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x['score'], reverse=True)
        for entry in sorted_board:
            st.write(f"👤 {entry['name']} — {entry['score']} points")

# ---------------------- QUIZ PAGE ----------------------
elif st.session_state.page == "quiz":
    q = st.session_state.questions[st.session_state.current_q]
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = 30 - elapsed

    if remaining <= 0:
        st.warning("⏰ Time's up for this question!")
        next_question(selected=None)
        st.experimental_rerun()
    else:
        st.markdown(f"<p class='timer'>⏱️ Time Left: {remaining}s</p>", unsafe_allow_html=True)
        st.markdown(f"### Question {st.session_state.current_q + 1}: {q['question']}")
        selected = st.radio("Choose an answer:", q["options"], index=None)
        if st.button("Next"):
            if selected:
                next_question(selected)
                st.experimental_rerun()
            else:
                st.warning("Please select an option before moving to the next question.")

# ---------------------- RESULT PAGE ----------------------
elif st.session_state.page == "result":
    st.markdown("<h2 class='title'>🏁 Quiz Completed!</h2>", unsafe_allow_html=True)
    st.markdown(f"<p class='score'>Your Final Score: {st.session_state.score} / {len(st.session_state.questions)}</p>", unsafe_allow_html=True)
    st.balloons()

    feedback = get_feedback(st.session_state.score, len(st.session_state.questions))
    st.markdown(f"<p class='feedback'>{feedback}</p>", unsafe_allow_html=True)

    if st.button("🔁 Restart Quiz"):
        restart_quiz()

    if st.session_state.leaderboard:
        st.markdown("### 🏆 Leaderboard")
        sorted_board = sorted(st.session_state.leaderboard, key=lambda x: x['score'], reverse=True)
        for entry in sorted_board:
            st.write(f"👤 {entry['name']} — {entry['score']} points")
