import streamlit as st
import json
import os
import time
import random
from datetime import datetime
import streamlit.components.v1 as components

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Smart Quiz App", page_icon="🎯", layout="centered")

# -------------------- CSS STYLES --------------------
st.markdown("""
<style>
body {
    background: linear-gradient(-45deg, #f9d423, #ff4e50, #a1c4fd, #c2e9fb);
    background-size: 400% 400%;
    animation: gradientShift 12s ease infinite;
    font-family: 'Poppins', sans-serif;
}
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
h1, h2, h3 {text-align: center; color: #333;}
.login-box {
    background: rgba(255,255,255,0.9);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0 6px 25px rgba(0,0,0,0.3);
    width: 90%;
    max-width: 400px;
    margin: auto;
}
.stButton>button {
    background: linear-gradient(to right, #667eea, #764ba2);
    color: white;
    border-radius: 8px;
}
.timer {
    color: #d32f2f;
    font-weight: bold;
    font-size: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATA --------------------
USER_FILE = "users.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_data(file):
    if os.path.exists(file):
        return json.load(open(file))
    return {}

def save_data(file, data):
    json.dump(data, open(file, "w"), indent=4)

users = load_data(USER_FILE)
leaderboard = load_data(LEADERBOARD_FILE)

# -------------------- QUIZ BANK --------------------
quizzes = {
    "Programming": [
        {"question": "Which company developed Java?", "options": ["Microsoft", "Oracle", "Sun Microsystems", "Google"], "answer": "Sun Microsystems"},
        {"question": "Which symbol is used for comments in Python?", "options": ["#", "//", "/* */", "<!-- -->"], "answer": "#"},
        {"question": "HTML stands for?", "options": ["Hyper Text Markup Language", "HighText Machine Language", "Hyperlinks and Text Markup Language", "None"], "answer": "Hyper Text Markup Language"},
        {"question": "CSS stands for?", "options": ["Cascading Style Sheets", "Color Style Syntax", "Coding Style System", "Central Sheet Style"], "answer": "Cascading Style Sheets"},
        {"question": "Which keyword is used to create a function in Python?", "options": ["def", "func", "lambda", "function"], "answer": "def"}
    ]
}

# -------------------- FEEDBACK FUNCTION --------------------
def auto_feedback(user_ans, correct_ans):
    if user_ans == correct_ans:
        return "✅ Correct! Great job!"
    else:
        return f"❌ Wrong! Correct answer: {correct_ans}"

# -------------------- LOGIN --------------------
if "user" not in st.session_state:
    st.session_state.user = None

def register_user(username, password):
    if username in users:
        return False, "Username exists"
    users[username] = {"password": password, "scores": []}
    save_data(USER_FILE, users)
    return True, "Registered"

def login_user(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state.user = username
        return True, "Login success"
    return False, "Invalid"

if st.session_state.user is None:
    choice = st.radio("Select", ["Login", "Register"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if choice == "Login":
        if st.button("Login"):
            ok, msg = login_user(username, password)
            st.info(msg)
            if ok:
                st.rerun()
    else:
        if st.button("Register"):
            ok, msg = register_user(username, password)
            st.info(msg)
    st.stop()

# -------------------- QUIZ SETUP --------------------
if "quiz" not in st.session_state:
    cat = st.selectbox("Category", list(quizzes.keys()))
    num_q = st.number_input("Questions", 1, len(quizzes[cat]), 3)

    if st.button("Start Quiz"):
        questions = quizzes[cat].copy()
        random.shuffle(questions)  # shuffle every attempt

        st.session_state.quiz = questions[:num_q]
        st.session_state.page = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.rerun()
    st.stop()

quiz = st.session_state.quiz
page = st.session_state.page

# -------------------- QUIZ END --------------------
if page >= len(quiz):
    st.success(f"Score: {st.session_state.score}/{len(quiz)}")
    if st.button("Restart"):
        del st.session_state.quiz
        st.rerun()
    st.stop()

# -------------------- QUESTION --------------------
q = quiz[page]

st.subheader(f"Q{page+1}: {q['question']}")

# TIMER (continuous)
remaining = 15
js = f"""
<div class='timer'>⏳ Time Left: <span id='t'>{remaining}</span></div>
<script>
let t={remaining};
setInterval(function(){{
    t--;
    document.getElementById('t').innerText = t;
}},1000);
</script>
"""
components.html(js, height=60)

choice = st.radio("Choose:", q["options"], key=page)

# -------------------- NEXT BUTTON --------------------
if st.button("Next"):
    feedback = auto_feedback(choice, q["answer"])

    if choice == q["answer"]:
        st.session_state.score += 1
        st.success(feedback)
    else:
        st.error(feedback)

    time.sleep(1.2)

    st.session_state.page += 1
    st.rerun()
