


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

# -------------------- QUIZ BANK (categorized) --------------------
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

# -------------------- AUTO-NEXT HANDLER --------------------
params = st.experimental_get_query_params()
if "auto_next" in params:
    # If quiz exists, record unanswered and advance; otherwise ignore
    if st.session_state.get("quiz") is not None:
        idx = st.session_state.get("page", 0)
        st.session_state.answers[idx] = None
        st.session_state.page = idx + 1
        st.session_state.start_time = time.time()
    # clear params and rerun
    st.experimental_set_query_params()
    st.rerun()

# -------------------- LOGIN / REGISTER PAGE --------------------
if st.session_state.user is None:
    st.title("🎓 Welcome to Smart Quiz App")
    menu = st.radio("Select Option:", ["Login", "Register"])

    if menu == "Login":
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            ok, msg = login_user(username, password)
            st.info(msg)
            if ok:
                st.rerun()
    else:
        username = st.text_input("Choose Username", key="reg_username")
        password = st.text_input("Choose Password", type="password", key="reg_password")
        if st.button("Register"):
            ok, msg = register_user(username, password)
            st.info(msg)
            if ok:
                # after registering, stay on page so user can login
                pass
    st.stop()

# -------------------- LOGGED-IN UI --------------------
st.sidebar.success(f"👤 Logged in as: {st.session_state.user}")
if st.sidebar.button("🚪 Logout"):
    st.session_state.user = None
    # clear quiz-related state
    for k in ["category", "difficulty", "page", "score", "quiz", "answers", "start_time"]:
        if k in st.session_state:
            del st.session_state[k]
    st.rerun()

st.title("🧩 Smart Quiz Application")
st.markdown("Test your skills — choose category and difficulty, then start!")

# -------------------- QUIZ SETUP --------------------
# If quiz not prepared yet, show setup controls
if st.session_state.get("quiz") is None:
    # choose category and difficulty
    cat = st.selectbox("📚 Select Category", list(quizzes.keys()), key="category_select")
    diff = st.selectbox("🎚️ Select Difficulty", ["Easy", "Medium", "Hard"], key="difficulty_select")

    # number of questions option: show up to available questions in category
    max_q = len(quizzes[cat])
    num_q = st.number_input(f"Number of questions (1 to {max_q})", min_value=1, max_value=max_q, value=min(5, max_q), step=1)

    if st.button("Start Quiz ▶️"):
        # prepare quiz: filter difficulty if you had difficulty-based selection; here we use same pool but adjust timer
        questions_pool = quizzes[cat].copy()
        random.shuffle(questions_pool)
        selected = questions_pool[:num_q]  # no repeats, random selection
        st.session_state.quiz = selected
        st.session_state.page = 0
        st.session_state.score = 0
        st.session_state.answers = {}
        st.session_state.category = cat
        st.session_state.difficulty = diff
        st.session_state.start_time = time.time()
        st.rerun()
    st.stop()

# -------------------- QUIZ PLAY --------------------
quiz = st.session_state.quiz
page = st.session_state.get("page", 0)
total = len(quiz)

# timer by difficulty
timer_limit = {"Easy": 25, "Medium": 15, "Hard": 10}.get(st.session_state.get("difficulty", "Medium"), 15)

# end of quiz
if page >= total:
    st.balloons()
    st.success(f"🎉 Quiz Completed — Score: {st.session_state.get('score',0)}/{total}")
    percent = (st.session_state.get('score',0) / total) * 100
    if percent == 100:
        feedback = "🌟 Excellent! Perfect score!"
    elif percent >= 75:
        feedback = "👏 Great job! You're very strong in this area."
    elif percent >= 50:
        feedback = "🙂 Good attempt — keep practicing!"
    else:
        feedback = "😅 Don't worry — practice more and you'll improve."

    st.info(feedback)

    # save result
    username = st.session_state.user
    users.setdefault(username, {"password": users.get(username, {}).get("password",""), "scores": []})
    score_data = {
        "score": st.session_state.get("score",0),
        "total": total,
        "category": st.session_state.get("category"),
        "difficulty": st.session_state.get("difficulty"),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    users[username]["scores"].append(score_data)
    save_data(USER_FILE, users)

    # update leaderboard (use best score overall)
    leaderboard[username] = max(s["score"] for s in users[username]["scores"])
    save_data(LEADERBOARD_FILE, leaderboard)

    st.subheader("🏆 Leaderboard (Top 5)")
    for i, (u, sc) in enumerate(sorted(leaderboard.items(), key=lambda x: x[1], reverse=True)[:5], 1):
        st.write(f"{i}. **{u}** — {sc} points")

    st.markdown("### 📊 Your Past Scores:")
    for entry in users[username]["scores"]:
        st.write(f"🕒 {entry['date']} — **{entry['score']} / {entry['total']}** ({entry['category']} / {entry['difficulty']})")

    if st.button("🔁 Restart Quiz"):
        for k in ["category", "difficulty", "page", "score", "quiz", "answers", "start_time"]:
            if k in st.session_state: del st.session_state[k]
        st.rerun()
    st.stop()

# show question
q = quiz[page]
st.markdown(f"### Q{page+1}. {q['question']}")

# compute remaining time
elapsed = int(time.time() - st.session_state.get("start_time", time.time()))
remaining = max(0, timer_limit - elapsed)

# client-side countdown and auto-next
js = f"""
<div class='timer'>⏳ Time Left: <span id='cd'>{remaining}</span> seconds</div>
<script>
  let t={remaining};
  const el=document.getElementById('cd');
  const interval=setInterval(()=>{{ t--; if(t<=0){{ clearInterval(interval); const url=new URL(window.location.href); url.searchParams.set('auto_next','1'); window.location.href=url.toString(); }} el.innerText=t;}},1000);
</script>
"""
components.html(js, height=70)

# options
choice = st.radio("Choose an answer:", q["options"], key=f"q{page}")

if st.button("Next ➡️"):
    # record answer
    st.session_state.answers[page] = choice
    if choice == q["answer"]:
        st.session_state.score = st.session_state.get("score", 0) + 1
        # small visual feedback
        st.success("✅ Correct!")
    else:
        st.error(f"❌ Wrong! Correct answer: {q['answer']}")
    # advance
    st.session_state.page = page + 1
    st.session_state.start_time = time.time()
    st.rerun()


