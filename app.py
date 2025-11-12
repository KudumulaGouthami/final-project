
import streamlit as st
import json
import os
import time
from datetime import datetime

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Quiz Application",
    page_icon="🧩",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------- CUSTOM STYLES --------------------
st.markdown("""
    <style>
        .main {
            background: linear-gradient(135deg, #e0f7fa 0%, #ffffff 100%);
            padding: 2rem;
            border-radius: 15px;
        }
        .stButton>button {
            background-color: #007BFF;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #0056b3;
        }
        h1, h2, h3 {
            text-align: center;
            color: #333333;
        }
        .timer {
            color: red;
            font-weight: bold;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- QUIZ QUESTIONS --------------------
quiz = [
    {"question": "Which language is known as the brain of the computer?",
     "options": ["Python", "C", "Java", "CPU"], "answer": "CPU"},
    {"question": "Which of these is a Python web framework?",
     "options": ["Django", "TensorFlow", "NumPy", "Pandas"], "answer": "Django"},
    {"question": "HTML stands for?",
     "options": ["Hyper Trainer Marking Language", "Hyper Text Markup Language",
                 "Hyper Text Markdown Language", "None of these"], "answer": "Hyper Text Markup Language"},
    {"question": "What does CSS stand for?",
     "options": ["Cascading Style Sheets", "Computer Style Sheet",
                 "Creative Style System", "Colorful Style Sheet"], "answer": "Cascading Style Sheets"},
    {"question": "Which of the following is a database?",
     "options": ["MySQL", "NumPy", "React", "Pandas"], "answer": "MySQL"}
]

# -------------------- FILES --------------------
USER_FILE = "users.json"
LEADERBOARD_FILE = "leaderboard.json"


def load_data(file):
    if os.path.exists(file):
        with open(file, "r") as f:
            return json.load(f)
    return {}


def save_data(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4)


users = load_data(USER_FILE)
leaderboard = load_data(LEADERBOARD_FILE)

# -------------------- LOGIN / REGISTER --------------------
if "user" not in st.session_state:
    st.session_state.user = None


def register_user(username, password):
    if username in users:
        return False, "⚠️ Username already exists."
    users[username] = {"password": password, "scores": []}
    save_data(USER_FILE, users)
    return True, "✅ Registration successful! Please login."


def login_user(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state.user = username
        return True, "✅ Login successful!"
    return False, "❌ Invalid username or password."


# -------------------- BACKGROUND MUSIC --------------------
st.markdown("""
    <audio autoplay loop>
        <source src="https://cdn.pixabay.com/audio/2022/03/15/audio_7e7e77b1b0.mp3" type="audio/mpeg">
    </audio>
""", unsafe_allow_html=True)

# -------------------- LOGIN PAGE --------------------
if st.session_state.user is None:
    st.title("🧩 Welcome to the Quiz App")
    menu = st.radio("Select Option:", ["Login", "Register"])

    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            success, message = login_user(username, password)
            st.info(message)
            if success:
                time.sleep(1)
                st.rerun()

    elif menu == "Register":
        username = st.text_input("Choose Username")
        password = st.text_input("Choose Password", type="password")
        if st.button("Register"):
            success, message = register_user(username, password)
            st.info(message)

else:
    # -------------------- SIDEBAR --------------------
    st.sidebar.success(f"👤 Logged in as: {st.session_state.user}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        for key in ["page", "score", "answers", "timer", "start_time"]:
            if key in st.session_state:
                del st.session_state[key]
        st.rerun()

    # -------------------- QUIZ LOGIC --------------------
    st.title("🎯 Advanced Quiz Application")
    st.markdown("### Test your knowledge with timer, music & leaderboard!")

    if "page" not in st.session_state:
        st.session_state.page = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "timer" not in st.session_state:
        st.session_state.timer = 15
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()

    page = st.session_state.page
    total_questions = len(quiz)

    # -------------------- TIMER --------------------
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, 15 - elapsed)
    st.markdown(f"<p class='timer'>⏳ Time left: {remaining} seconds</p>", unsafe_allow_html=True)

    if remaining == 0:
        st.warning("⏰ Time's up! Moving to next question...")
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()

    if page < total_questions:
        question = quiz[page]
        st.markdown(f"### Q{page+1}. {question['question']}")
        choice = st.radio("Choose an answer:", question["options"], key=f"q{page}")

        if st.button("Next ➡️"):
            st.session_state.answers[page] = choice
            if choice == question["answer"]:
                st.session_state.score += 1
            st.session_state.page += 1
            st.session_state.start_time = time.time()
            st.rerun()

    else:
        # -------------------- RESULT --------------------
        st.balloons()
        st.success("🎉 Quiz Completed!")
        st.write(f"**Your Score: {st.session_state.score} / {total_questions}**")

        username = st.session_state.user

        # ✅ Prevent KeyError: ensure username exists in file
        if username not in users:
            users[username] = {"password": "", "scores": []}

        score_data = {
            "score": st.session_state.score,
            "total": total_questions,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save score safely
        users[username].setdefault("scores", []).append(score_data)
        save_data(USER_FILE, users)

        # Update leaderboard
        leaderboard[username] = max(s["score"] for s in users[username]["scores"])
        save_data(LEADERBOARD_FILE, leaderboard)

        # -------------------- LEADERBOARD --------------------
        st.subheader("🏆 Leaderboard (Top 5)")
        sorted_lb = sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)
        for rank, (user, score) in enumerate(sorted_lb[:5], 1):
            st.write(f"{rank}. **{user}** — {score} points")

        # -------------------- USER HISTORY --------------------
        st.markdown("### 📊 Your Past Scores:")
        for entry in users[username]["scores"]:
            st.write(f"🕒 {entry['date']} — **{entry['score']} / {entry['total']}**")

        if st.button("🔁 Restart Quiz"):
            for key in ["page", "score", "answers", "start_time"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

