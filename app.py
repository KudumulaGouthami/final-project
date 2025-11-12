


import streamlit as st
import json
import os
import time
import random
from datetime import datetime
import streamlit.components.v1 as components

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Advanced Quiz Application", page_icon="🎯", layout="centered")

# -------------------- CUSTOM STYLE --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(-45deg, #ff9a9e, #fad0c4, #fbc2eb, #a1c4fd);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
    font-family: 'Poppins', sans-serif;
}
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.main {
    background-color: rgba(255,255,255,0.92);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.2);
    animation: floatUp 1s ease-in-out;
}
h1, h2, h3 {
    text-align: center;
    color: #333;
    font-weight: 600;
}
.stButton>button {
    background: linear-gradient(to right, #667eea, #764ba2);
    color: white;
    border-radius: 10px;
    font-size: 16px;
    padding: 8px 18px;
    transition: 0.3s;
    border: none;
}
.stButton>button:hover {
    background: linear-gradient(to right, #764ba2, #667eea);
    transform: scale(1.05);
}
.timer {
    color: #d32f2f;
    font-weight: bold;
    font-size: 20px;
    text-align: center;
}
.login-box {
    background: rgba(255,255,255,0.85);
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 6px 20px rgba(0,0,0,0.2);
    width: 90%;
    max-width: 420px;
    margin: auto;
    animation: fadeIn 1s ease-in;
}
@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}
.quiz-logo {
    display: block;
    margin: 0 auto 15px auto;
    width: 100px;
    border-radius: 50%;
    animation: spin 10s linear infinite;
}
@keyframes spin {
    from {transform: rotate(0deg);}
    to {transform: rotate(360deg);}
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATA FILES --------------------
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

# -------------------- QUIZ BANK --------------------
quizzes = {
    "Programming": [
        {"question": "Which company developed Java?", "options": ["Microsoft", "Oracle", "Sun Microsystems", "Google"], "answer": "Sun Microsystems"},
        {"question": "Which symbol is used for comments in Python?", "options": ["#", "//", "/* */", "<!-- -->"], "answer": "#"},
        {"question": "HTML stands for?", "options": ["Hyper Text Markup Language", "HighText Machine Language", "Hyperlinks and Text Markup Language", "None"], "answer": "Hyper Text Markup Language"},
        {"question": "CSS stands for?", "options": ["Cascading Style Sheets", "Color Style Syntax", "Coding Style System", "Central Sheet Style"], "answer": "Cascading Style Sheets"},
        {"question": "Which keyword is used to create a function in Python?", "options": ["def", "func", "lambda", "function"], "answer": "def"},
        {"question": "Which tag is used to link CSS in HTML?", "options": ["<css>", "<style>", "<link>", "<script>"], "answer": "<link>"}
    ],
    "Maths": [
        {"question": "What is 12 × 8?", "options": ["80", "96", "88", "108"], "answer": "96"},
        {"question": "The square root of 144 is?", "options": ["10", "11", "12", "13"], "answer": "12"},
        {"question": "What is 15% of 200?", "options": ["25", "30", "35", "20"], "answer": "30"},
        {"question": "Solve: (10 + 2) × 3", "options": ["30", "36", "25", "40"], "answer": "36"},
        {"question": "What is 7 + 6 × 5?", "options": ["65", "37", "35", "47"], "answer": "37"}
    ],
    "General Knowledge": [
        {"question": "Who was the first President of India?", "options": ["Dr. Rajendra Prasad", "Jawaharlal Nehru", "Indira Gandhi", "APJ Abdul Kalam"], "answer": "Dr. Rajendra Prasad"},
        {"question": "Which is the national bird of India?", "options": ["Sparrow", "Peacock", "Crow", "Parrot"], "answer": "Peacock"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
        {"question": "Who wrote the National Anthem?", "options": ["Rabindranath Tagore", "Bankim Chandra", "Sarojini Naidu", "Mahatma Gandhi"], "answer": "Rabindranath Tagore"},
        {"question": "Which is the largest ocean on Earth?", "options": ["Atlantic", "Indian", "Arctic", "Pacific"], "answer": "Pacific"}
    ]
}

# -------------------- LOGIN SYSTEM --------------------
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "home"

def register_user(username, password):
    if not username or not password:
        return False, "Please enter username and password."
    if username in users:
        return False, "⚠️ Username already exists!"
    users[username] = {"password": password, "scores": []}
    save_data(USER_FILE, users)
    return True, "✅ Registration successful!"

def login_user(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state.user = username
        st.session_state.page = "quiz"
        return True, "✅ Login successful!"
    return False, "❌ Invalid credentials."

# -------------------- LOGIN PAGE --------------------
if st.session_state.user is None and st.session_state.page == "home":
    st.markdown("<h1>🎓 Welcome to Smart Quiz App</h1>", unsafe_allow_html=True)
    st.image("https://i.pinimg.com/originals/f1/2a/6c/f12a6c56ed744fb6e06405df2eab9bcd.gif", width=300)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Login 🚪"):
            st.session_state.page = "login"
            st.rerun()
    with col2:
        if st.button("Register 📝"):
            st.session_state.page = "register"
            st.rerun()
    st.stop()

# -------------------- LOGIN FORM --------------------
if st.session_state.page == "login":
    st.image("https://i.pinimg.com/originals/2c/64/8e/2c648e2ed8a35123777c6ddf6f5a2b13.gif", width=300)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.subheader("🔐 Login to Continue")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login"):
        ok, msg = login_user(username, password)
        st.info(msg)
        if ok:
            st.rerun()
    if st.button("⬅️ Back"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# -------------------- REGISTER FORM --------------------
if st.session_state.page == "register":
    st.image("https://i.pinimg.com/originals/fe/f7/cc/fef7cc64d224d739671ebbbf76cfb6b8.gif", width=300)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    st.subheader("📝 Create an Account")
    username = st.text_input("Choose Username", key="reg_username")
    password = st.text_input("Choose Password", type="password", key="reg_password")
    if st.button("Register"):
        ok, msg = register_user(username, password)
        st.info(msg)
        if ok:
            st.session_state.page = "login"
            st.rerun()
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# -------------------- REST OF YOUR QUIZ CODE --------------------
# ✅ The rest of your quiz logic remains unchanged
# (category select, timer, leaderboard, etc.)
