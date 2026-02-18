



import streamlit as st
import random
import time

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Quiz Application", page_icon="🎯")


# ---------------- SESSION DEFAULTS ----------------
if "stage" not in st.session_state:
    st.session_state.stage = "welcome"
if "user" not in st.session_state:
    st.session_state.user = None
if "quiz" not in st.session_state:
    st.session_state.quiz = None
if "page" not in st.session_state:
    st.session_state.page = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "start_time" not in st.session_state:
    st.session_state.start_time = 0


# ---------------- QUIZ DATA ----------------
questions = [
    {"q": "Python comment symbol?", "opt": ["#", "//", "/* */", "--"], "ans": "#"},
    {"q": "12 × 8 = ?", "opt": ["96", "88", "108", "80"], "ans": "96"},
    {"q": "HTML stands for?", "opt": ["Hyper Text Markup Language", "None", "HighText ML", "Hyper Tool"], "ans": "Hyper Text Markup Language"},
    {"q": "CSS stands for?", "opt": ["Cascading Style Sheets", "Color Style", "None", "Code Style"], "ans": "Cascading Style Sheets"},
    {"q": "5 + 7 = ?", "opt": ["10", "12", "15", "14"], "ans": "12"}
]


# =================================================
# WELCOME PAGE
# =================================================
if st.session_state.stage == "welcome":

    st.title("🎯 Welcome to Quiz Application")

    if st.button("Register"):
        st.session_state.stage = "register"
        st.rerun()

    if st.button("Login"):
        st.session_state.stage = "login"
        st.rerun()

    st.stop()


# =================================================
# REGISTER
# =================================================
if st.session_state.stage == "register":

    st.header("Register")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Create Account"):
        st.session_state.user = username
        st.session_state.stage = "quiz"
        st.rerun()

    st.stop()


# =================================================
# LOGIN
# =================================================
if st.session_state.stage == "login":

    st.header("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        st.session_state.user = username
        st.session_state.stage = "quiz"
        st.rerun()

    st.stop()


# =================================================
# QUIZ PAGE
# =================================================
if st.session_state.stage == "quiz":

    st.title("🧩 Quiz Time")

    # -------- Start Quiz --------
    if st.session_state.quiz is None:

        if st.button("Start Quiz"):

            shuffled = questions.copy()
            random.shuffle(shuffled)   # ✅ shuffle every attempt

            st.session_state.quiz = shuffled
            st.session_state.page = 0
            st.session_state.score = 0
            st.session_state.start_time = time.time()

            st.rerun()

        st.stop()

    quiz = st.session_state.quiz
    page = st.session_state.page

    # -------- Timer (continuous) --------
    total_time = 15
    remaining = total_time - int(time.time() - st.session_state.start_time)

    st.write(f"⏳ Time Left: {max(0, remaining)} sec")

    time.sleep(1)
    st.rerun()

    # -------- Time up --------
    if remaining <= 0:
        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()

    # -------- Quiz finished --------
    if page >= len(quiz):
        st.session_state.stage = "result"
        st.rerun()

    q = quiz[page]

    st.subheader(q["q"])

    choice = st.radio("Choose answer:", q["opt"])

    if st.button("Next"):
        if choice == q["ans"]:
            st.session_state.score += 1

        st.session_state.page += 1
        st.session_state.start_time = time.time()
        st.rerun()


# =================================================
# RESULT PAGE
# =================================================
if st.session_state.stage == "result":

    st.success(f"🎉 Score: {st.session_state.score}/{len(st.session_state.quiz)}")

    if st.button("Play Again"):
        st.session_state.quiz = None
        st.session_state.stage = "quiz"
        st.rerun()
