

import streamlit as st
import json, os, time, random
from datetime import datetime
import streamlit.components.v1 as components

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Quiz App", page_icon="🎯", layout="centered")

# ---------------- CSS STYLES ----------------
st.markdown("""
import streamlit as st
import time
import random

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Quiz Application", page_icon="🎯", layout="centered")

# ---------------- CSS STYLES ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(-45deg, #ffecd2, #fcb69f, #a1c4fd, #c2e9fb);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
}
@keyframes gradientBG {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
div.stButton > button {
    background: linear-gradient(90deg, #667eea, #764ba2);
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    border: none;
    font-weight: bold;
}
div.stButton > button:hover {
    background: linear-gradient(90deg, #764ba2, #667eea);
}
h1 {
    text-align: center;
    color: #333333;
}
</style>
""", unsafe_allow_html=True)

# ---------------- QUIZ DATA ----------------
quiz_data = {
    "Python": [
        {"question": "What is the output of print(2 ** 3)?", "options": ["5", "6", "8", "9"], "answer": "8"},
        {"question": "Which keyword is used for function in Python?", "options": ["define", "def", "function", "fun"], "answer": "def"},
        {"question": "What data type is this? L = [1, 23, 'hello', 1]", "options": ["List", "Dictionary", "Tuple", "Array"], "answer": "List"},
    ],
    "Java": [
        {"question": "Which keyword is used to inherit a class in Java?", "options": ["super", "this", "extends", "implements"], "answer": "extends"},
        {"question": "Which of these is not a Java feature?", "options": ["Object-oriented", "Use of pointers", "Portable", "Dynamic"], "answer": "Use of pointers"},
        {"question": "Which method is the entry point for a Java program?", "options": ["start()", "main()", "run()", "init()"], "answer": "main()"},
    ]
}

# ---------------- SESSION STATE ----------------
if "page" not in st.session_state:
    st.session_state.page = "home"
if "score" not in st.session_state:
    st.session_state.score = 0
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "selected_category" not in st.session_state:
    st.session_state.selected_category = None
if "questions" not in st.session_state:
    st.session_state.questions = []
if "start_time" not in st.session_state:
    st.session_state.start_time = None
if "timer_duration" not in st.session_state:
    st.session_state.timer_duration = 60  # 1-minute timer


# ---------------- TIMER FUNCTION ----------------
def get_time_left():
    if st.session_state.start_time is None:
        return st.session_state.timer_duration
    elapsed = time.time() - st.session_state.start_time
    return max(0, int(st.session_state.timer_duration - elapsed))


# ---------------- HOME PAGE ----------------
if st.session_state.page == "home":
    st.markdown("<h1>🧠 Smart Quiz Application</h1>", unsafe_allow_html=True)
    st.write("Select a category and start your quiz!")

    category = st.selectbox("Select Category", ["Python", "Java"])
    num_questions = st.number_input("Number of questions", min_value=1, max_value=3, value=1)

    st.markdown(f"⏳ **Time Left: {get_time_left()} seconds**")

    if st.button("Start Quiz ▶"):
        st.session_state.selected_category = category
        all_questions = quiz_data[category]
        st.session_state.questions = random.sample(all_questions, num_questions)
        st.session_state.q_index = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.session_state.page = "quiz"
        st.rerun()

# ---------------- QUIZ PAGE ----------------
elif st.session_state.page == "quiz":
    remaining_time = get_time_left()

    if remaining_time <= 0:
        st.session_state.page = "result"
        st.rerun()

    st.markdown(f"⏰ **Time Left: {remaining_time} seconds**")

    current_q = st.session_state.questions[st.session_state.q_index]
    st.subheader(f"Q{st.session_state.q_index + 1}. {current_q['question']}")

    selected_option = st.radio("Choose your answer:", current_q["options"])

    if st.button("Next ➡"):
        if selected_option == current_q["answer"]:
            st.session_state.score += 1

        st.session_state.q_index += 1
        if st.session_state.q_index >= len(st.session_state.questions):
            st.session_state.page = "result"
        st.rerun()

# ---------------- RESULT PAGE ----------------
elif st.session_state.page == "result":
    st.markdown("<h1>🎉 Quiz Completed!</h1>", unsafe_allow_html=True)
    st.success(f"Your Score: **{st.session_state.score} / {len(st.session_state.questions)}**")

    if st.button("Play Again 🔁"):
        st.session_state.page = "home"
        st.rerun()

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
    ],
    "Maths": [
        {"question": "What is 12 × 8?", "options": ["80","96","88","108"], "answer": "96"},
        {"question": "The square root of 144 is?", "options": ["10","11","12","13"], "answer": "12"},
        {"question": "What is 15% of 200?", "options": ["25","30","35","20"], "answer": "30"},
        {"question": "Solve: (10 + 2) × 3", "options": ["30","36","25","40"], "answer": "36"},
        {"question": "What is 7 + 6 × 5?", "options": ["65","37","35","47"], "answer": "37"}
    ],
    "General Knowledge": [
        {"question": "Who was the first President of India?", "options": ["Dr. Rajendra Prasad","Jawaharlal Nehru","Indira Gandhi","APJ Abdul Kalam"], "answer": "Dr. Rajendra Prasad"},
        {"question": "Which is the national bird of India?", "options": ["Sparrow","Peacock","Crow","Parrot"], "answer": "Peacock"},
        {"question": "Which planet is known as the Red Planet?", "options": ["Earth","Mars","Jupiter","Venus"], "answer": "Mars"},
        {"question": "Who wrote the National Anthem?", "options": ["Rabindranath Tagore","Bankim Chandra","Sarojini Naidu","Mahatma Gandhi"], "answer": "Rabindranath Tagore"},
        {"question": "Which is the largest ocean on Earth?", "options": ["Atlantic","Indian","Arctic","Pacific"], "answer": "Pacific"}
    ]
}

# ---------------- SESSION SETUP ----------------
if "stage" not in st.session_state:
    st.session_state.stage = "home"
if "user" not in st.session_state:
    st.session_state.user = None

# ---------------- FUNCTIONS ----------------
def register_user(username, password):
    if not username or not password:
        return False, "Please enter username and password."
    if username in users:
        return False, "⚠ Username already exists!"
    users[username] = {"password": password, "scores": []}
    save_data(USER_FILE, users)
    return True, "✅ Registration successful!"

def login_user(username, password):
    if username in users and users[username]["password"] == password:
        st.session_state.user = username
        return True, "✅ Login successful!"
    return False, "❌ Invalid credentials."

def ai_feedback(question, user_ans, correct_ans):
    if user_ans == correct_ans:
        return "🌟 Excellent! You’ve mastered this question!"
    else:
        return f"🤔 Oops! The correct answer was *{correct_ans}*. Try revising this topic."

# ---------------- HOME PAGE ----------------
if st.session_state.stage == "home":
    st.markdown("<h1>🎯 Welcome to Smart Quiz Application 🎯</h1>", unsafe_allow_html=True)
    st.image("https://cdn.dribbble.com/users/166903/screenshots/2685205/quiz.gif", use_container_width=True)
    st.markdown("""
    <div class='content-box'>
        <h3>🧠 Test Your Knowledge!</h3>
        <p>Challenge yourself with quizzes from <b>Programming</b>, <b>Maths</b>, and <b>General Knowledge</b>.<br>
        Improve your skills while having fun! 💡</p>
    </div>
    """, unsafe_allow_html=True)
    st.image("https://cdn.dribbble.com/users/14268/screenshots/4107914/quiz-game.gif", use_container_width=True)
    st.write("🚀 Ready to start your quiz journey?")
    if st.button("Start ▶"):
        st.session_state.stage = "register"
        st.rerun()
    st.stop()

# ---------------- REGISTER PAGE ----------------
if st.session_state.stage == "register":
    st.image("https://i.pinimg.com/originals/d3/06/7e/d3067e2d7d2d6f9a12dfbd00b9985b07.gif", use_container_width=True)
    st.subheader("📝 Register Here")
    username = st.text_input("Create Username")
    password = st.text_input("Create Password", type="password")
    if st.button("Register"):
        ok, msg = register_user(username, password)
        st.info(msg)
        if ok:
            time.sleep(1)
            st.session_state.stage = "login"
            st.rerun()
    st.stop()

# ---------------- LOGIN PAGE ----------------
if st.session_state.stage == "login" and st.session_state.user is None:
    st.image("https://i.pinimg.com/originals/2f/d8/0b/2fd80b21c1ff8022a2b6c1e5de032eb5.gif", use_container_width=True)
    st.subheader("🔐 Login to Continue")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        ok, msg = login_user(username, password)
        st.info(msg)
        if ok:
            st.session_state.stage = "quiz"
            st.rerun()
    st.stop()

# ---------------- QUIZ PAGE ----------------
if st.session_state.stage == "quiz" and st.session_state.user:
    st.sidebar.success(f"👤 Logged in as: {st.session_state.user}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.stage = "home"
        st.rerun()

    st.title("🧩 Smart Quiz Application")
    st.markdown("Select a category and start your quiz!")

    if "quiz" not in st.session_state:
        cat = st.selectbox("📚 Category", list(quizzes.keys()))
        num_q = st.number_input("Number of questions", 1, len(quizzes[cat]), min(5, len(quizzes[cat])))
        if st.button("Start Quiz ▶"):
            selected = random.sample(quizzes[cat], num_q)
            st.session_state.quiz = selected
            st.session_state.page = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.cat = cat
            st.rerun()
        st.stop()

    quiz = st.session_state.quiz
    page = st.session_state.page
    total = len(quiz)

    # Timer
    total_time = 20
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, total_time - elapsed)
    st.markdown(f"<div class='timer'>⏳ Time Left: {remaining} seconds</div>", unsafe_allow_html=True)

    if remaining <= 0:
        st.warning("⏰ Time's up for this question!")
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()

    if page >= total:
        st.balloons()
        st.success(f"🎉 Quiz Completed — Score: {st.session_state.score}/{total}")
        username = st.session_state.user
        score_data = {"score": st.session_state.score, "total": total, "category": st.session_state.cat,
                      "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        users[username]["scores"].append(score_data)
        save_data(USER_FILE, users)
        leaderboard[username] = max(s["score"] for s in users[username]["scores"])
        save_data(LEADERBOARD_FILE, leaderboard)
        st.subheader("🏆 Leaderboard (Top 5)")
        for i, (u, sc) in enumerate(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:5], 1):
            st.write(f"{i}. *{u}* — {sc} points")
        if st.button("🔁 Restart"):
            for k in ["quiz", "page", "score", "cat"]:
                if k in st.session_state: del st.session_state[k]
            st.rerun()
        st.stop()

    q = quiz[page]
    st.markdown(f"### Q{page+1}. {q['question']}")
    choice = st.radio("Choose an answer:", q["options"], key=f"q{page}")

    if st.button("Next ➡"):
        feedback = ""
        if choice == q["answer"]:
            st.session_state.score += 1
            st.success("✅ Correct!")
        else:
            st.error(f"❌ Wrong! Correct: {q['answer']}")
        feedback = ai_feedback(q['question'], choice, q['answer'])
        st.markdown(f"<div class='feedback-box'>{feedback}</div>", unsafe_allow_html=True)
        time.sleep(1.5)
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()



