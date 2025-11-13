import streamlit as st
import json, os, time, random
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Smart Quiz App", page_icon="🎯", layout="centered")

# ---------------- CSS STYLES ----------------
st.markdown("""
<style>
body {
    background: linear-gradient(-45deg, #ffecd2, #fcb69f, #a1c4fd, #c2e9fb);
    background-size: 400% 400%;
    animation: gradientShift 10s ease infinite;
    font-family: 'Poppins', sans-serif;
}
@keyframes gradientShift {
    0% {background-position: 0% 50%;}
    50% {background-position: 100% 50%;}
    100% {background-position: 0% 50%;}
}
h1, h2, h3 {text-align:center; color:#333;}
p {text-align:center; font-size:16px;}
.login-box, .content-box {
    background: rgba(255, 255, 255, 0.88);
    padding: 30px; border-radius: 20px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
    width: 90%; max-width: 500px;
    margin: auto;
    animation: fadeIn 1s ease-in;
}
.stButton>button {
    background: linear-gradient(to right, #667eea, #764ba2);
    color:white; border-radius:8px;
    font-size:17px; font-weight:600;
    padding:10px 20px; border:none;
    transition:0.3s; box-shadow:0 4px 10px rgba(0,0,0,0.2);
}
.stButton>button:hover {
    background: linear-gradient(to right, #764ba2, #667eea);
    transform:scale(1.05);
}
.timer {
    color: #d32f2f; font-weight:bold;
    font-size:20px; text-align:center;
    margin-top:10px;
}
.feedback-box {
    background: rgba(255,255,255,0.85);
    border-radius:10px; padding:10px 15px;
    box-shadow:0 3px 8px rgba(0,0,0,0.15);
    margin-top:10px; text-align:center;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(25px);}
    to {opacity: 1; transform: translateY(0);}
}
</style>
""", unsafe_allow_html=True)

# ---------------- DATA FILES ----------------
USER_FILE = "users.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_data(file):
    return json.load(open(file)) if os.path.exists(file) else {}

def save_data(file, data):
    json.dump(data, open(file, "w"), indent=4)

users = load_data(USER_FILE)
leaderboard = load_data(LEADERBOARD_FILE)
if not isinstance(leaderboard, dict):
    leaderboard = {}

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
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "page" not in st.session_state:
    st.session_state.page = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = time.time()

# ---------------- FUNCTIONS ----------------
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
        return True, "✅ Login successful!"
    return False, "❌ Invalid credentials."

# ---------------- HOME ----------------
if st.session_state.stage == "home":
    st.markdown("<h1>🎯 Welcome to Smart Quiz Application 🎯</h1>", unsafe_allow_html=True)
    st.image("https://cdn.dribbble.com/users/166903/screenshots/2685205/quiz.gif", use_container_width=True)
    if st.button("Start ▶️"):
        st.session_state.stage = "register"
        st.rerun()

# ---------------- REGISTER ----------------
elif st.session_state.stage == "register":
    st.image("https://i.pinimg.com/originals/d3/06/7e/d3067e2d7d2d6f9a12dfbd00b9985b07.gif", use_container_width=True)
    st.subheader("📝 Register Here")
    username = st.text_input("Create Username", key="reg_user")
    password = st.text_input("Create Password", type="password", key="reg_pass")
    if st.button("Register"):
        ok, msg = register_user(username, password)
        st.info(msg)
        if ok:
            time.sleep(1)
            st.session_state.stage = "login"
            st.rerun()

# ---------------- LOGIN ----------------
elif st.session_state.stage == "login" and st.session_state.user is None:
    st.image("https://i.pinimg.com/originals/2f/d8/0b/2fd80b21c1ff8022a2b6c1e5de032eb5.gif", use_container_width=True)
    st.subheader("🔐 Login to Continue")
    username = st.text_input("Username", key="login_user")
    password = st.text_input("Password", type="password", key="login_pass")
    if st.button("Login"):
        ok, msg = login_user(username, password)
        st.info(msg)
        if ok:
            st.session_state.stage = "quiz"
            st.session_state.quiz = None
            st.session_state.page = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.rerun()

# ---------------- QUIZ ----------------
elif st.session_state.stage == "quiz" and st.session_state.user:
    st.sidebar.success(f"👤 Logged in as: {st.session_state.user}")
    if st.sidebar.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.stage = "home"
        st.session_state.quiz = None
        st.session_state.page = 0
        st.session_state.score = 0
        st.session_state.start_time = time.time()
        st.rerun()

    st.title("🧩 Smart Quiz Application")
    st.markdown("Select a category and start your quiz!")

    if not st.session_state.get("quiz"):
        cat = st.selectbox("📚 Category", list(quizzes.keys()))
        max_q = len(quizzes[cat])
        num_q = st.number_input("Number of questions", min_value=1, max_value=max_q, value=min(5, max_q), key="num_q")
        if st.button("Start Quiz ▶️"):
            st.session_state.quiz = random.sample(quizzes[cat], num_q)
            st.session_state.page = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.cat = cat
            st.rerun()
        st.stop()

    quiz = st.session_state.get("quiz", [])
    page = st.session_state.get("page", 0)
    total = len(quiz)

    if total == 0:
        st.warning("No questions available. Please restart the quiz.")
        if st.button("Restart Quiz Setup"):
            st.session_state.quiz = None
            st.rerun()
        st.stop()

    # ---------------- LIVE TIMER FIX ----------------
    total_time = 20
    timer_placeholder = st.empty()
    elapsed = int(time.time() - st.session_state.get("start_time", time.time()))
    remaining = max(0, total_time - elapsed)

    timer_placeholder.markdown(f"<div class='timer'>⏳ Time Left: {remaining} seconds</div>", unsafe_allow_html=True)

    if remaining > 0:
        time.sleep(1)
        st.rerun()
    else:
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()
