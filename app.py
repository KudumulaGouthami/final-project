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
