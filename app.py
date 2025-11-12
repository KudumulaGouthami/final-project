import streamlit as st
import json
import os
import time

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
            background: linear-gradient(135deg, #d6f0ff 0%, #ffffff 100%);
            padding: 2rem;
            border-radius: 15px;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 16px;
            transition: 0.3s;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        h1, h2, h3 {
            text-align: center;
            color: #333333;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- QUIZ QUESTIONS --------------------
quiz = [
    {
        "question": "Which language is known as the brain of the computer?",
        "options": ["Python", "C", "Java", "CPU"],
        "answer": "CPU"
    },
    {
        "question": "Which of these is a Python web framework?",
        "options": ["Django", "TensorFlow", "NumPy", "Pandas"],
        "answer": "Django"
    },
    {
        "question": "HTML stands for?",
        "options": [
            "Hyper Trainer Marking Language",
            "Hyper Text Markup Language",
            "Hyper Text Markdown Language",
            "None of these"
        ],
        "answer": "Hyper Text Markup Language"
    },
    {
        "question": "What does CSS stand for?",
        "options": [
            "Cascading Style Sheets",
            "Computer Style Sheet",
            "Creative Style System",
            "Colorful Style Sheet"
        ],
        "answer": "Cascading Style Sheets"
    },
    {
        "question": "Which of the following is a database?",
        "options": ["MySQL", "NumPy", "React", "Pandas"],
        "answer": "MySQL"
    }
]

# -------------------- USER DATA MANAGEMENT --------------------
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

# -------------------- LOGIN & REGISTRATION --------------------
users = load_users()

if "user" not in st.session_state:
    st.session_state.user = None

def register_user(username, password):
    if username in users:
        return False, "⚠️ Username already exists."
    users[username] = {"password": password}
    save_users(users)
    return True, "✅ Registration successful! Please login."

def login_user(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state.user = username
        return True, "✅ Login successful!"
    return False, "❌ Invalid username or password."

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
    # -------------------- QUIZ LOGIC --------------------
    st.sidebar.write(f"👤 Logged in as: **{st.session_state.user}**")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.page = 0
        st.session_state.score = 0
        st.session_state.answers = {}
        st.rerun()

    st.title("🎯 Welcome to the Quiz Application")
    st.markdown("### Test your knowledge and see your score instantly!")

    if "page" not in st.session_state:
        st.session_state.page = 0
    if "score" not in st.session_state:
        st.session_state.score = 0
    if "answers" not in st.session_state:
        st.session_state.answers = {}

    page = st.session_state.page
    total_questions = len(quiz)

    if page < total_questions:
        question = quiz[page]
        st.markdown(f"### Q{page+1}. {question['question']}")
        choice = st.radio("Choose an answer:", question["options"], key=page)

        if st.button("Next ➡️"):
            st.session_state.answers[page] = choice
            if choice == question["answer"]:
                st.session_state.score += 1
            st.session_state.page += 1
            st.rerun()
    else:
        st.balloons()
        st.success("🎉 Quiz Completed!")
        st.write(f"**Your Score: {st.session_state.score} / {total_questions}**")

        if st.session_state.score == total_questions:
            st.markdown("🌟 Perfect! You got all answers correct!")
        elif st.session_state.score >= total_questions / 2:
            st.markdown("👍 Great job! Keep it up!")
        else:
            st.markdown("💡 Keep practicing to improve your score!")

        if st.button("🔁 Restart Quiz"):
            st.session_state.page = 0
            st.session_state.score = 0
            st.session_state.answers = {}
            st.rerun()
