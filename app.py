



      import streamlit as st
import json, os, time, random
from datetime import datetime

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Quiz Application", page_icon="🎯", layout="centered")


# -------------------------------------------------
# FILE STORAGE
# -------------------------------------------------
USER_FILE = "users.json"
LEADER_FILE = "leaderboard.json"

def load_data(file):
    return json.load(open(file)) if os.path.exists(file) else {}

def save_data(file, data):
    json.dump(data, open(file, "w"), indent=4)

users = load_data(USER_FILE)
leaderboard = load_data(LEADER_FILE)


# -------------------------------------------------
# SESSION DEFAULTS (prevents ALL errors)
# -------------------------------------------------
defaults = {
    "stage": "welcome",
    "user": None,
    "quiz": None,
    "page": 0,
    "score": 0,
    "start_time": 0,
    "category": None
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# -------------------------------------------------
# QUIZ QUESTIONS
# -------------------------------------------------
quizzes = {
    "Programming": [
        {"question": "Which company developed Java?", "options": ["Microsoft","Oracle","Sun Microsystems","Google"], "answer": "Sun Microsystems"},
        {"question": "Python comment symbol?", "options": ["#","//","/* */","--"], "answer": "#"},
        {"question": "HTML stands for?", "options": ["Hyper Text Markup Language","None","HighText ML","Hyper Tool ML"], "answer": "Hyper Text Markup Language"},
        {"question": "CSS stands for?", "options": ["Cascading Style Sheets","Color Style Syntax","None","Coding Sheet Style"], "answer": "Cascading Style Sheets"},
        {"question": "Keyword to create function?", "options": ["def","func","function","lambda"], "answer": "def"}
    ],
    "Maths": [
        {"question": "12 × 8 = ?", "options": ["80","96","108","88"], "answer": "96"},
        {"question": "√144 = ?", "options": ["10","11","12","14"], "answer": "12"},
        {"question": "15% of 200?", "options": ["25","30","35","20"], "answer": "30"},
        {"question": "10 + 5 × 2 = ?", "options": ["20","30","25","15"], "answer": "20"},
        {"question": "50 ÷ 5 = ?", "options": ["5","8","10","15"], "answer": "10"}
    ]
}


# -------------------------------------------------
# FUNCTIONS
# -------------------------------------------------
def register_user(u, p):
    if u in users:
        return False, "Username already exists"
    users[u] = {"password": p, "scores": []}
    save_data(USER_FILE, users)
    return True, "Registration successful"

def login_user(u, p):
    if u in users and users[u]["password"] == p:
        st.session_state.user = u
        return True
    return False


# =================================================
# WELCOME PAGE
# =================================================
if st.session_state.stage == "welcome":

    st.title("🎯 Welcome to Quiz Application")
    st.write("Test your knowledge with fun quizzes!")

    col1, col2 = st.columns(2)

    if col1.button("Register"):
        st.session_state.stage = "register"
        st.rerun()

    if col2.button("Login"):
        st.session_state.stage = "login"
        st.rerun()

    st.stop()


# =================================================
# REGISTER PAGE
# =================================================
if st.session_state.stage == "register":

    st.header("📝 Register")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Create Account"):
        ok, msg = register_user(u, p)
        st.info(msg)
        if ok:
            st.session_state.stage = "login"
            st.rerun()

    st.stop()


# =================================================
# LOGIN PAGE
# =================================================
if st.session_state.stage == "login":

    st.header("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if login_user(u, p):
            st.session_state.stage = "quiz"
            st.rerun()
        else:
            st.error("Invalid credentials")

    st.stop()


# =================================================
# QUIZ PAGE
# =================================================
if st.session_state.stage == "quiz":

    st.sidebar.success(f"👤 {st.session_state.user}")

    if st.sidebar.button("Logout"):
        st.session_state.stage = "welcome"
        st.session_state.user = None
        st.session_state.quiz = None
        st.rerun()


    # ---------------- Start Quiz ----------------
    if st.session_state.quiz is None:

        cat = st.selectbox("Choose Category", list(quizzes.keys()))

        if st.button("Start Quiz"):

            selected = quizzes[cat][:]

            # ✅ Shuffle every attempt
            random.shuffle(selected)

            st.session_state.quiz = selected
            st.session_state.page = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()
            st.session_state.category = cat

            st.rerun()

        st.stop()


    quiz = st.session_state.quiz
    page = st.session_state.page
    total = len(quiz)


    # ---------------- Continuous Timer ----------------
    total_time = 15

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, total_time - elapsed)

    st.write(f"⏳ Time Left: {remaining} sec")

    time.sleep(1)
    st.rerun()


    if remaining <= 0:
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()


    # ---------------- Finish ----------------
    if page >= total:

        score = st.session_state.score

        users[st.session_state.user]["scores"].append(score)
        save_data(USER_FILE, users)

        leaderboard[st.session_state.user] = max(users[st.session_state.user]["scores"])
        save_data(LEADER_FILE, leaderboard)

        st.session_state.stage = "result"
        st.rerun()


    # ---------------- Question ----------------
    q = quiz[page]

    st.subheader(f"Q{page+1}: {q['question']}")

    choice = st.radio("Select answer:", q["options"])

    if st.button("Next"):

        if choice == q["answer"]:
            st.session_state.score += 1

        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()


# =================================================
# RESULT DASHBOARD
# =================================================
if st.session_state.stage == "result":

    st.title("📊 Result Dashboard")

    score = st.session_state.score
    total = len(st.session_state.quiz)

    st.success(f"Your Score: {score}/{total}")

    st.subheader("🏆 Leaderboard")

    for i, (u, sc) in enumerate(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True), 1):
        st.write(f"{i}. {u} — {sc}")

    if st.button("Play Again"):
        st.session_state.quiz = None
        st.session_state.stage = "quiz"
        st.rerun()


