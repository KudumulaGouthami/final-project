import streamlit as st
import sqlite3
import time
import random

# -----------------------------
# Database setup
# -----------------------------
conn = sqlite3.connect('quiz_app.db', check_same_thread=False)
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password TEXT
            )''')

# -----------------------------
# Quiz questions by category
# -----------------------------
quizzes = {
    "Maths": [
        {"question": "What is 12 + 8?", "options": ["18", "20", "22", "24"], "answer": "20"},
        {"question": "Square root of 81?", "options": ["7", "8", "9", "10"], "answer": "9"},
        {"question": "What is 15 × 3?", "options": ["45", "30", "25", "60"], "answer": "45"},
    ],
    "Programming": [
        {"question": "Which language is used for web apps?", "options": ["Python", "C++", "JavaScript", "C"], "answer": "JavaScript"},
        {"question": "What does HTML stand for?", "options": ["HyperText Markup Language", "HighText Machine Language", "Hyper Tool Multi Language", "None"], "answer": "HyperText Markup Language"},
        {"question": "Which keyword is used to define a function in Python?", "options": ["def", "func", "define", "lambda"], "answer": "def"},
    ],
    "General Knowledge": [
        {"question": "Capital of France?", "options": ["Berlin", "Paris", "London", "Rome"], "answer": "Paris"},
        {"question": "Which planet is known as Red Planet?", "options": ["Mars", "Jupiter", "Venus", "Saturn"], "answer": "Mars"},
        {"question": "Who wrote ‘Harry Potter’?", "options": ["J.K. Rowling", "Tolstoy", "Shakespeare", "Charles Dickens"], "answer": "J.K. Rowling"},
    ]
}

# -----------------------------
# Page config & background
# -----------------------------
st.set_page_config(page_title="Smart Quiz Application", page_icon="🧠", layout="wide")

# Anime-style gradient background
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://i.pinimg.com/originals/62/50/7f/62507ffde96d05dbb8eddb255f81c6e4.gif');
    background-size: cover;
    background-position: center;
}
[data-testid="stHeader"] {
    background: rgba(0,0,0,0);
}
.stButton>button {
    background-color: #ff6b81;
    color: white;
    border-radius: 10px;
    padding: 8px 20px;
    font-size: 16px;
    border: none;
}
.stButton>button:hover {
    background-color: #ff4757;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -----------------------------
# Helper functions
# -----------------------------
def register_user(username, password):
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    if c.fetchone():
        return False
    c.execute("INSERT INTO users (username, password) VALUES (?,?)", (username, password))
    conn.commit()
    return True

def login_user(username, password):
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    return c.fetchone() is not None

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🎯 Smart Quiz Application")
st.markdown("### Welcome! Test your knowledge and challenge yourself 💡")

menu = ["Login", "Register", "Start Quiz"]
choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------
# Registration
# -----------------------------
if choice == "Register":
    st.subheader("📝 Create a New Account")
    new_user = st.text_input("Username")
    new_pass = st.text_input("Password", type="password")
    if st.button("Register"):
        if register_user(new_user, new_pass):
            st.success("✅ Registration successful! Please go to Login.")
        else:
            st.error("⚠️ Username already exists. Try a different one.")

# -----------------------------
# Login
# -----------------------------
elif choice == "Login":
    st.subheader("🔐 Login to Your Account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if login_user(username, password):
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success(f"Welcome {username}! Proceed to Start Quiz.")
        else:
            st.error("❌ Incorrect username or password.")

# -----------------------------
# Start Quiz
# -----------------------------
elif choice == "Start Quiz":
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        st.warning("⚠️ Please login first from the sidebar.")
    else:
        category = st.selectbox("Choose Quiz Category", list(quizzes.keys()))
        if st.button("Start Quiz"):
            st.session_state["quiz_category"] = category
            st.session_state["score"] = 0
            st.session_state["q_index"] = 0
            st.session_state["start_time"] = time.time()
            st.session_state["total_time"] = 30  # seconds
            st.session_state["quiz_started"] = True
            st.rerun()

# -----------------------------
# Quiz Questions
# -----------------------------
if "quiz_started" in st.session_state and st.session_state["quiz_started"]:
    remaining = int(st.session_state["total_time"] - (time.time() - st.session_state["start_time"]))
    if remaining <= 0:
        st.error("⏰ Time’s up!")
        st.session_state["quiz_started"] = False
        st.info(f"Your Final Score: {st.session_state['score']} / {len(quizzes[st.session_state['quiz_category']])}")
    else:
        st.markdown(f"### ⏳ Time Left: **{remaining} seconds**")
        category = st.session_state["quiz_category"]
        q_index = st.session_state["q_index"]
        question = quizzes[category][q_index]
        st.subheader(question["question"])
        answer = st.radio("Select your answer:", question["options"], key=q_index)
        if st.button("Next"):
            if answer == question["answer"]:
                st.session_state["score"] += 1
            st.session_state["q_index"] += 1
            if st.session_state["q_index"] >= len(quizzes[category]):
                st.session_state["quiz_started"] = False
                st.success("🎉 Quiz Completed!")
                st.info(f"✅ Your Score: {st.session_state['score']} / {len(quizzes[category])}")
            st.rerun()

        time.sleep(1)
        st.rerun()
