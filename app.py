

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
    background: linear-gradient(135deg, #b3e5fc, #ffccbc, #d1c4e9);
    background-size: 400% 400%;
    animation: gradientMove 10s ease infinite;
}
@keyframes gradientMove {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
.main {
    background-color: rgba(255,255,255,0.9);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}
h1, h2, h3 {
    text-align: center;
    color: #333;
}
.stButton>button {
    background-color: #007BFF;
    color: white;
    border-radius: 10px;
    font-size: 16px;
    padding: 8px 18px;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #004a99;
}
.timer {
    color: #d32f2f;
    font-weight: bold;
    font-size: 20px;
    text-align: center;
}
</style>
""", unsafe_allow_html=True)

# -------------------- BACKGROUND MUSIC --------------------
st.audio("https://cdn.pixabay.com/audio/2022/03/15/audio_7e7e77b1b0.mp3", format="audio/mp3", start_time=0)

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

# -------------------- QUIZ QUESTIONS --------------------
quizzes = {
    "Programming": [
        {"question": "Which company developed Java?", "options": ["Microsoft", "Oracle", "Sun Microsystems", "Google"], "answer": "Sun Microsystems"},
        {"question": "Which symbol is used for comments in Python?", "options": ["#", "//", "/* */", "<!-- -->"], "answer": "#"},
        {"question": "HTML stands for?", "options": ["Hyper Text Markup Language", "HighText Machine Language", "Hyperlinks and Text Markup Language", "None"], "answer": "Hyper Text Markup Language"},
        {"question": "CSS stands for?", "options": ["Cascading Style Sheets", "Color Style Syntax", "Coding Style System", "Central Sheet Style"], "answer": "Cascading Style Sheets"}
    ],
    "Maths": [
        {"question": "What is 12 × 8?", "options": ["80", "96", "88", "108"], "answer": "96"},
        {"question": "The square root of 144 is?", "options": ["10", "11", "12", "13"], "answer": "12"},
        {"question": "What is 15% of 200?", "options": ["25", "30", "35", "20"], "answer": "30"},
        {"question": "Solve: (10 + 2) × 3", "options": ["30", "36", "25", "40"], "answer": "36"}
    ],
    "General Knowledge": [
        {"question": "Who was the first President of India?", "options": ["Dr. Rajendra Prasad", "Jawaharlal Nehru", "Indira Gandhi", "APJ Abdul Kalam"], "answer": "Dr. Rajendra Prasad"},
        {"question": "Which is the national bird of India?", "options": ["Sparrow", "Peacock", "Crow", "Parrot"], "answer": "Peacock"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Earth", "Mars", "Jupiter", "Venus"], "answer": "Mars"},
        {"question": "Who wrote the National Anthem?", "options": ["Rabindranath Tagore", "Bankim Chandra", "Sarojini Naidu", "Mahatma Gandhi"], "answer": "Rabindranath Tagore"}
    ]
}

# -------------------- LOGIN SYSTEM --------------------
if "user" not in st.session_state:
    st.session_state.user = None

def register_user(username, password):
    if username in users:
        return False, "⚠️ Username already exists!"
    users[username] = {"password": password, "scores": []}
    save_data(USER_FILE, users)
    return True, "✅ Registration successful!"

def login_user(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state.user = username
        return True, "✅ Login successful!"
    return False, "❌ Invalid credentials."

# -------------------- LOGIN PAGE --------------------
if st.session_state.user is None:
    st.title("🎓 Welcome to Smart Quiz App")
    menu = st.radio("Select Option:", ["Login", "Register"])

    if menu == "Login":
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            ok, msg = login_user(username, password)
            st.info(msg)
            if ok: st.rerun()
    else:
        username = st.text_input("Choose Username")
        password = st.text_input("Choose Password", type="password")
        if st.button("Register"):
            ok, msg = register_user(username, password)
            st.info(msg)

else:
    # -------------------- LOGGED IN --------------------
    st.sidebar.success(f"👤 Logged in as: {st.session_state.user}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        for k in ["category", "difficulty", "page", "score", "quiz"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()

    st.title("🧩 Smart Quiz Application")
    st.markdown("Test your skills with fun and challenge!")

    # -------------------- QUIZ SETUP --------------------
    if "category" not in st.session_state:
        st.session_state.category = st.selectbox("📚 Select Category", list(quizzes.keys()))
        st.session_state.difficulty = st.selectbox("🎚️ Select Difficulty", ["Easy", "Medium", "Hard"])
        if st.button("Start Quiz ▶️"):
            questions = quizzes[st.session_state.category]
            random.shuffle(questions)
            st.session_state.quiz = questions
            st.session_state.page = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.rerun()
        st.stop()

    quiz = st.session_state.quiz
    page = st.session_state.page
    total = len(quiz)
    timer_limit = {"Easy": 20, "Medium": 15, "Hard": 10}[st.session_state.difficulty]

    # -------------------- END SCREEN --------------------
    if page >= total:
        st.balloons()
        st.success(f"🎉 Quiz Completed — Score: {st.session_state.score}/{total}")
        percent = (st.session_state.score / total) * 100
        if percent == 100:
            feedback = "🌟 Excellent! You're a true genius!"
        elif percent >= 75:
            feedback = "👏 Great job! You really know your stuff."
        elif percent >= 50:
            feedback = "🙂 Good attempt! Keep practicing."
        else:
            feedback = "😅 Keep learning — you'll get better next time!"

        st.info(feedback)

        username = st.session_state.user
        score_data = {"score": st.session_state.score, "total": total,
                      "category": st.session_state.category, "difficulty": st.session_state.difficulty,
                      "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        users[username]["scores"].append(score_data)
        save_data(USER_FILE, users)

        leaderboard[username] = max([s["score"] for s in users[username]["scores"]])
        save_data(LEADERBOARD_FILE, leaderboard)

        st.subheader("🏆 Leaderboard (Top 5)")
        for i, (user, scr) in enumerate(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:5], 1):
            st.write(f"{i}. **{user}** — {scr} points")

        if st.button("🔁 Restart Quiz"):
            for k in ["category", "difficulty", "page", "score", "quiz"]:
                if k in st.session_state: del st.session_state[k]
            st.rerun()
        st.stop()

    # -------------------- QUESTION DISPLAY --------------------
    q = quiz[page]
    st.markdown(f"### Q{page + 1}. {q['question']}")

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, timer_limit - elapsed)
    js_html = f"""
    <div class='timer'>⏳ Time Left: <span id='cd'>{remaining}</span> seconds</div>
    <script>
      let t={remaining};const e=document.getElementById('cd');
      const i=setInterval(()=>{{t--;if(t<=0){{clearInterval(i);window.location.search='auto_next=1';}}e.innerText=t;}},1000);
    </script>
    """
    components.html(js_html, height=60)

    choice = st.radio("Choose an answer:", q["options"], key=f"q{page}")
    if st.button("Next ➡️"):
        if choice == q["answer"]:
            st.session_state.score += 1
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()
